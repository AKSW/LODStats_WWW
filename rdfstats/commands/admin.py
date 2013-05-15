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

class DoAdmin(Command):
    # Parser configuration
    summary = "Administration functions for LODStats"
    usage = "paster-2.6 --plugin=Rdfstats admin"
    group_name = "rdfstats"
    parser = Command.standard_parser(verbose=False)

    def callback_stats(self, rdfdocstat):
        #print rdfdocstat
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
    
    def command(self):
        self.logging_file_config(config_file)
        log = logging.getLogger(__name__)
        
        self.worker_proc = None
        self.rdfdoc_to_do = None
        
        #rdfdoc = Session.query(model.RDFDoc).filter(model.RDFDoc.worked_on==True).all()
        #small and faulty rdf dump
        #rdfdoc = Session.query(model.RDFDoc).filter(model.RDFDoc.name=="dbpedia_topical_concepts_en").first()
        rdfdoc = model.RDFDoc()
        rdfdoc.name = 'dbpedia_labels_en'
        rdfdoc.format = 'nt'
        Session.add(rdfdoc)
        print rdfdoc
        rdfdoc.file_last_modified = None
        path_to_file = '/home/ivan/.virtualenvs/lodstats/dumps/rdf/labels_en.nt'
        rdfdoc.uri = 'file://' + path_to_file

        self.worker_proc = model.WorkerProc()
        self.worker_proc.pid = os.getpid()
        self.worker_proc.rdfdoc = rdfdoc
        Session.add(self.worker_proc)
        rdfdoc.worked_on = True
        self.rdfdoc = rdfdoc

        last_stat_result = rdfdoc.current_stats
        self.stat_result = model.StatResult()
        rdfdoc.stats.append(self.stat_result)
        rdfdoc.current_stats = self.stat_result
        self.stat_result.triples_done = None
        self.stat_result.content_length = None
        self.stat_result.bytes_download = None
        self.stat_result.bytes = None
        self.stat_result.warnings = None
        self.stat_result.last_warning = None
        Session.commit()

        print rdfdoc.format


        try:
            if rdfdoc.format is None:
                rdfdocstats = RDFStats(rdfdoc.uri, stats=lodstats_stats)
                #print rdfstats
            else:
                rdfdocstats = RDFStats(rdfdoc.uri, format=rdfdoc.format, stats=lodstats_stats)
            rdfdocstats.parse(callback_fun=self.callback_parse, if_modified_since = rdfdoc.file_last_modified)
            rdfdocstats.do_stats(callback_fun=self.callback_stats)
        except NotModified, errorstr:
            modified = False
        except Exception, errorstr:
            error = errorstr

        #from pprint import pprint
        #pprint (vars(rdfdocstats))
        #try:
        #    print modified
        #    print error
        #except:
        #    pass
                
        print "adding triples"
        self.stat_result.triples = rdfdocstats.no_of_triples()
        print "voidify!"
        self.stat_result.void = rdfdocstats.voidify('turtle')
        print "writing warning"
        self.stat_result.warnings = rdfdocstats.warnings
        if rdfdocstats.warnings > 0:
            self.stat_result.last_warning = unicode(rdfdocstats.last_warning.message, errors='replace')
        self.stat_result.has_errors = False
        self.stat_result.errors = None
        print "Adding new classes to the DB"
        print len(rdfdocstats.stats_results['classes']['distinct'])
        for class_uri,result in rdfdocstats.stats_results['classes']['distinct'].iteritems():
            c = Session.query(model.RDFClass).filter(model.RDFClass.uri==class_uri).first()
            if c is None:
                c = model.RDFClass()
                c.uri = class_uri
                Session.add(c)
            rcs = model.RDFClassStat()
            rcs.rdf_class = c
            rcs.stat_result = self.stat_result
            rcs.count = result
            Session.add(rcs)
        # vocab:
        print "adding new vocabularies to DB"
        print len(rdfdocstats.stats_results['vocabularies'])
        for base_uri,result in rdfdocstats.stats_results['vocabularies'].iteritems():
            if result > 0:
                v = Session.query(model.Vocab).filter(model.Vocab.uri==base_uri).first()
                if v is None:
                    v = model.Vocab()
                    v.uri = base_uri
                    Session.add(v)
                rvs = model.RDFVocabStat()
                rvs.vocab = v
                rvs.stat_result = self.stat_result
                rvs.count = result
                Session.add(rvs)
        # props
        print "Adding new properties to DB"
        print len(rdfdocstats.stats_results['propertiesall']['distinct'])
        for property_uri,result in rdfdocstats.stats_results['propertiesall']['distinct'].iteritems():
            p = Session.query(model.RDFProperty).filter(model.RDFProperty.uri==property_uri).first()
            if p is None:
                p = model.RDFProperty(uri=property_uri)
                Session.add(p)
            rps = model.RDFPropertyStat(rdf_property=p, stat_result=self.stat_result, count=result)
            Session.add(rps)
        # defined classes
        print "Adding new classes to DB"
        print len(rdfdocstats.stats_results['classesdefined']['histogram'])
        for class_uri,result in rdfdocstats.stats_results['classesdefined']['histogram'].iteritems():
            c = Session.query(model.DefinedClass).filter(model.DefinedClass.uri==class_uri).first()
            if c is None:
                c = model.DefinedClass()
                c.uri = class_uri
                Session.add(c)
            rcs = model.DefinedClassStat()
            rcs.defined_class = c
            rcs.stat_result = self.stat_result
            rcs.count = result
            Session.add(rcs)
        # basics
        self.stat_result.entities = rdfdocstats.stats_results['entities']['count']
        self.stat_result.literals = rdfdocstats.stats_results['literals']['count']
        self.stat_result.blanks = rdfdocstats.stats_results['blanks']['count']
        self.stat_result.blanks_as_subject = rdfdocstats.stats_results['blanks']['s']
        self.stat_result.blanks_as_object = rdfdocstats.stats_results['blanks']['o']
        self.stat_result.subclasses = rdfdocstats.stats_results['subclasses']['count']
        self.stat_result.typed_subjects = rdfdocstats.stats_results['typedsubjects']['count']
        self.stat_result.labeled_subjects = rdfdocstats.stats_results['labeledsubjects']['count']
        # hierarchy depth
        if len(rdfdocstats.stats_results['classhierarchy']) > 0:
            self.stat_result.class_hierarchy_depth = rdfdocstats.stats_results['classhierarchy'][max(rdfdocstats.stats_results['classhierarchy'],
                key=rdfdocstats.stats_results['classhierarchy'].get)]
        if len(rdfdocstats.stats_results['propertyhierarchy']) > 0:
            self.stat_result.property_hierarchy_depth = rdfdocstats.stats_results['propertyhierarchy'][max(rdfdocstats.stats_results['propertyhierarchy'],
                key=rdfdocstats.stats_results['propertyhierarchy'].get)]
        # averages
        self.stat_result.properties_per_entity = rdfdocstats.stats_results['propertiesperentity']['avg']
        self.stat_result.string_length_typed = rdfdocstats.stats_results['stringlength']['avg_typed']
        self.stat_result.string_length_untyped = rdfdocstats.stats_results['stringlength']['avg_untyped']
        # links
        self.stat_result.links = rdfdocstats.stats_results['links']['count']
        # datatypes
        print "Adding datatypes to the DB"
        print len(rdfdocstats.stats_results['datatypes'])
        for d_uri,result in rdfdocstats.stats_results['datatypes'].iteritems():
            d = Session.query(model.RDFDatatype).filter(model.RDFDatatype.uri==d_uri).first()
            if d is None:
                d = model.RDFDatatype()
                d.uri = d_uri
                Session.add(d)
            ds = model.RDFDatatypeStat()
            ds.rdf_datatype = d
            ds.stat_result = self.stat_result
            ds.count = result
            Session.add(ds)
        # languages
        print "Adding languages to DB"
        print len(rdfdocstats.stats_results['languages'])
        for code,result in rdfdocstats.stats_results['languages'].iteritems():
            l = Session.query(model.Language).filter(model.Language.code==code).first()
            if l is None:
                l = model.Language()
                l.code = code
                Session.add(l)
            ls = model.LanguageStat()
            ls.language = l
            ls.stat_result = self.stat_result
            ls.count = result
            Session.add(ls)
        # namespacelinks
        print "Adding namespacelinks to DB"
        print len(rdfdocstats.stats_results['links']['namespacelinks'])
        iterator = 0
        for link_uri,result in rdfdocstats.stats_results['links']['namespacelinks'].iteritems():
            if(iterator % 1000 == 0):
                print iterator
            c = Session.query(model.Link).filter(model.Link.code==link_uri).first()
            if c is None:
                c = model.Link()
                c.code = link_uri
                Session.add(c)
            rcs = model.LinkStat()
            rcs.link = c
            rcs.stat_result = self.stat_result
            rcs.count = result
            Session.add(rcs)
            iterator = iterator + 1

        rdfdoc.worked_on = False
        rdfdoc.last_updated = datetime.now()
        rdfdoc.file_last_modified = rdfdocstats.last_modified
        self.stat_result.last_updated = datetime.now()
        Session.delete(self.worker_proc)
        Session.commit()
        
