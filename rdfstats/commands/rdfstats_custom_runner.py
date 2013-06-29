"""
Copyright 2012 Jan Demter <jan@demter.de>

This file is part of LODStatsWWW.

LODStats is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

LODStats is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with LODStats.  If not, see <http://www.gnu.org/licenses/>.
"""
from paste.script.command import Command

from paste.deploy import appconfig
from rdfstats.config.environment import load_environment

config_file = 'production.ini'
conf = appconfig('config:%s' % config_file, relative_to='.')
load_environment(conf.global_conf, conf.local_conf)

from datetime import date, datetime, timedelta

from rdfstats.model.meta import Session
from rdfstats import model
from sqlalchemy import and_, or_
import sys
import signal
import os
import logging

from lodstats import RDFStats
from lodstats.stats import lodstats as lodstats_stats
from lodstats.exceptions import NotModified 

class DoStats(Command):
    # Parser configuration
    summary = "compute stats for RDF data, get URI from DB"
    usage = "paster-2.6 --plugin=Rdfstats rdfstats_runner"
    group_name = "rdfstats"
    parser = Command.standard_parser(verbose=False)
    
    def callback_stats(self, rdfdocstat):
        if rdfdocstat.no_of_statements > 0:
            # update triples done
            if rdfdocstat.no_of_statements % 10000 == 0:
                self.stat_result.triples_done = rdfdocstat.no_of_statements
                self.stat_result.warnings = rdfdocstat.warnings
                Session.commit()
    
    def callback_parse(self, rdfdocstat):
        self.stat_result.content_length = rdfdocstat.content_length
        self.stat_result.bytes_download = rdfdocstat.bytes_download
        self.stat_result.bytes = rdfdocstat.bytes
        Session.commit()
        
    def term_handler(self, signum, frame):
        log.debug("exiting through term handler")
        Session.rollback()
        if self.rdfdoc_to_do is None or self.rdfdoc_to_do.worked_on == False:
            if self.worker_proc != None:
                Session.delete(self.worker_proc)
                Session.commit()
            sys.exit(0)
        else:
            self.rdfdoc_to_do.worked_on = False
            Session.delete(self.stat_result)
            Session.delete(self.worker_proc)
            Session.commit()
            sys.exit(0)

    def command(self):
        
        self.logging_file_config(config_file)
        log = logging.getLogger(__name__)
        
        self.worker_proc = None
        self.rdfdoc_to_do = None
        
        signal.signal(signal.SIGINT, self.term_handler)
        signal.signal(signal.SIGTERM, self.term_handler)
        
        ## do not spawn more than two workers
        #number_of_workers = Session.query(model.WorkerProc).with_lockmode('read').count()
        #if number_of_workers >= 2:
            #return 0
        
        update_name = "europeana-lod_75b5bafaee382a7fda709b0614ef3b3a"
        rdfdoc_to_do = Session.query(model.RDFDoc).filter(
                and_(model.RDFDoc.name == update_name,
                     model.RDFDoc.worked_on==False)).with_lockmode('update')\
                    .order_by(model.RDFDoc.last_updated).first()
        if rdfdoc_to_do is None:
            return 0

        rdfdoc_to_do.reset_current_stats_and_worker()
        
        # register this worker
        self.worker_proc = model.WorkerProc()
        self.worker_proc.pid = os.getpid()
        self.worker_proc.rdfdoc = rdfdoc_to_do
        Session.add(self.worker_proc)
        rdfdoc_to_do.worked_on = True
        self.rdfdoc_to_do = rdfdoc_to_do
        log.debug("worker %i working on %i" % (self.worker_proc.pid, self.rdfdoc_to_do.id))
        
        if rdfdoc_to_do.current_stats and rdfdoc_to_do.current_stats.errors == 'broken':
            rdfdoc_to_do.worked_on = False
            rdfdoc_to_do.last_updated = datetime.now()
            Session.delete(self.worker_proc)
            Session.commit()
            sys.exit(0)
        
        last_stat_result = rdfdoc_to_do.current_stats
        stat_result = model.StatResult()
        self.stat_result = stat_result
        rdfdoc_to_do.stats.append(stat_result)
        rdfdoc_to_do.current_stats = stat_result
        stat_result.triples_done = None
        stat_result.content_length = None
        stat_result.bytes_download = None
        stat_result.bytes = None
        stat_result.warnings = None
        stat_result.last_warning = None
        Session.commit()
        
        error = None
        modified = True # set True if remote file has been modified
        try:
            if rdfdoc_to_do.format is None:
                rdfdocstats = RDFStats(rdfdoc_to_do.uri, stats=lodstats_stats)
            else:
                rdfdocstats = RDFStats(rdfdoc_to_do.uri, format=rdfdoc_to_do.format, stats=lodstats_stats)
            rdfdocstats.parse(callback_fun=self.callback_parse, if_modified_since = rdfdoc_to_do.file_last_modified)
            rdfdocstats.do_stats(callback_fun=self.callback_stats)
        except NotModified, errorstr:
            modified = False
        except Exception, errorstr:
            error = errorstr

        print error
        
        if error is None and (modified or rdfdoc_to_do.current_stats is None):
            stat_result.triples = rdfdocstats.no_of_triples()
            stat_result.void = rdfdocstats.voidify('turtle')
            stat_result.warnings = rdfdocstats.warnings
            if rdfdocstats.warnings > 0:
                stat_result.last_warning = unicode(rdfdocstats.last_warning.message, errors='replace')
            stat_result.has_errors = False
            stat_result.errors = None
            for class_uri,result in rdfdocstats.stats_results['classes']['distinct'].iteritems():
                c = Session.query(model.RDFClass).filter(model.RDFClass.uri==class_uri).first()
                if c is None:
                    c = model.RDFClass()
                    c.uri = class_uri
                    Session.add(c)
                rcs = model.RDFClassStat()
                rcs.rdf_class = c
                rcs.stat_result = stat_result
                rcs.count = result
                Session.add(rcs)
            # vocab:
            for base_uri,result in rdfdocstats.stats_results['vocabularies'].iteritems():
                if result > 0:
                    v = Session.query(model.Vocab).filter(model.Vocab.uri==base_uri).first()
                    if v is None:
                        v = model.Vocab()
                        v.uri = base_uri
                        Session.add(v)
                    rvs = model.RDFVocabStat()
                    rvs.vocab = v
                    rvs.stat_result = stat_result
                    rvs.count = result
                    Session.add(rvs)
            # props
            for property_uri,result in rdfdocstats.stats_results['propertiesall']['distinct'].iteritems():
                p = Session.query(model.RDFProperty).filter(model.RDFProperty.uri==property_uri).first()
                if p is None:
                    p = model.RDFProperty(uri=property_uri)
                    Session.add(p)
                rps = model.RDFPropertyStat(rdf_property=p, stat_result=stat_result, count=result)
                Session.add(rps)
            # defined classes
            for class_uri,result in rdfdocstats.stats_results['classesdefined']['histogram'].iteritems():
                c = Session.query(model.DefinedClass).filter(model.DefinedClass.uri==class_uri).first()
                if c is None:
                    c = model.DefinedClass()
                    c.uri = class_uri
                    Session.add(c)
                rcs = model.DefinedClassStat()
                rcs.defined_class = c
                rcs.stat_result = stat_result
                rcs.count = result
                Session.add(rcs)
            # basics
            stat_result.entities = rdfdocstats.stats_results['entities']['count']
            stat_result.literals = rdfdocstats.stats_results['literals']['count']
            stat_result.blanks = rdfdocstats.stats_results['blanks']['count']
            stat_result.blanks_as_subject = rdfdocstats.stats_results['blanks']['s']
            stat_result.blanks_as_object = rdfdocstats.stats_results['blanks']['o']
            stat_result.subclasses = rdfdocstats.stats_results['subclasses']['count']
            stat_result.typed_subjects = rdfdocstats.stats_results['typedsubjects']['count']
            stat_result.labeled_subjects = rdfdocstats.stats_results['labeledsubjects']['count']
            # hierarchy depth
            if len(rdfdocstats.stats_results['classhierarchy']) > 0:
                stat_result.class_hierarchy_depth = rdfdocstats.stats_results['classhierarchy'][max(rdfdocstats.stats_results['classhierarchy'],
                    key=rdfdocstats.stats_results['classhierarchy'].get)]
            if len(rdfdocstats.stats_results['propertyhierarchy']) > 0:
                stat_result.property_hierarchy_depth = rdfdocstats.stats_results['propertyhierarchy'][max(rdfdocstats.stats_results['propertyhierarchy'],
                    key=rdfdocstats.stats_results['propertyhierarchy'].get)]
            # averages
            stat_result.properties_per_entity = rdfdocstats.stats_results['propertiesperentity']['avg']
            stat_result.string_length_typed = rdfdocstats.stats_results['stringlength']['avg_typed']
            stat_result.string_length_untyped = rdfdocstats.stats_results['stringlength']['avg_untyped']
            # links
            stat_result.links = rdfdocstats.stats_results['links']['count']
            # datatypes
            for d_uri,result in rdfdocstats.stats_results['datatypes'].iteritems():
                d = Session.query(model.RDFDatatype).filter(model.RDFDatatype.uri==d_uri).first()
                if d is None:
                    d = model.RDFDatatype()
                    d.uri = d_uri
                    Session.add(d)
                ds = model.RDFDatatypeStat()
                ds.rdf_datatype = d
                ds.stat_result = stat_result
                ds.count = result
                Session.add(ds)
            # languages
            for code,result in rdfdocstats.stats_results['languages'].iteritems():
                l = Session.query(model.Language).filter(model.Language.code==code).first()
                if l is None:
                    l = model.Language()
                    l.code = code
                    Session.add(l)
                ls = model.LanguageStat()
                ls.language = l
                ls.stat_result = stat_result
                ls.count = result
                Session.add(ls)
            # namespacelinks
            for link_uri,result in rdfdocstats.stats_results['links']['namespacelinks'].iteritems():
                c = Session.query(model.Link).filter(model.Link.code==link_uri).first()
                if c is None:
                    c = model.Link()
                    c.code = link_uri
                    Session.add(c)
                rcs = model.LinkStat()
                rcs.link = c
                rcs.stat_result = stat_result
                rcs.count = result
                Session.add(rcs)
        elif not modified:
            rdfdoc_to_do.current_stats = last_stat_result
            Session.delete(stat_result)
        else:
            stat_result.triples = None
            stat_result.void = None
            stat_result.has_errors = True
            stat_result.errors = unicode(error)
        
        rdfdoc_to_do.worked_on = False
        rdfdoc_to_do.last_updated = datetime.now()
        rdfdoc_to_do.file_last_modified = rdfdocstats.last_modified
        stat_result.last_updated = datetime.now()
        Session.delete(self.worker_proc)
        Session.commit()