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
from lodstats.stats import lodstats_old as lodstats_stats
from lodstats.exceptions import NotModified

class DoStats(Command):
    # Parser configuration
    summary = "compute stats for RDF data, get URI from DB"
    usage = "paster-2.6 --plugin=Rdfstats rdfstats_runner"
    group_name = "rdfstats"
    parser = Command.standard_parser(verbose=False)

    def callback_stats(self, rdfdocstat):
        no_of_statements = rdfdocstat.get_no_of_triples()
        if no_of_statements > 0:
            # update triples done
            if no_of_statements % 10000 == 0:
                self.stat_result.triples_done = no_of_statements
                self.stat_result.warnings = rdfdocstat.warnings
                Session.commit()

    def callback_function_download(self, rdfdocstat):
        self.stat_result.content_length = rdfdocstat.content_length
        self.stat_result.bytes_downloaded = rdfdocstat.bytes_downloaded
        Session.commit()

    def callback_function_extraction(self, rdfdocstat):
        self.stat_result.bytes = rdfdocstat.bytes_extracted
        Session.commit()

    def term_handler(self, signum, frame):
        log = logging.getLogger(__name__)
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

        # do not spawn more than two workers
        #number_of_workers = Session.query(model.WorkerProc).with_lockmode('read').count()
        #if number_of_workers >= 2:
        #    return 0

        four_weeks_ago = datetime.today()-timedelta(weeks=1)
        #rdfdoc_to_do = Session.query(model.RDFDoc).filter(
                    #and_(
                        #model.RDFDoc.worked_on==False,
                        #model.RDFDoc.in_datahub==True,
                        #or_(model.RDFDoc.last_updated<four_weeks_ago,
                            #model.RDFDoc.last_updated == None))).with_lockmode('update')\
                    #.order_by(model.RDFDoc.last_updated).first()
        rdfdoc_to_do = Session.query(model.RDFDoc).filter(
                    and_(
                        model.RDFDoc.worked_on==False,
                        model.RDFDoc.in_datahub==True)).with_lockmode('update')\
                    .order_by(model.RDFDoc.last_updated).first()
        if rdfdoc_to_do is None:
            log.warning("rdfdoc_to_do is None")
            return 0

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

        log.info(rdfdoc_to_do.format)

        error = None
        modified = True # set True if remote file has been modified
        try:
            rdfdocstats = RDFStats(rdfdoc_to_do.uri, format=rdfdoc_to_do.format, stats=lodstats_stats)
            rdfdocstats.set_callback_function_download(self.callback_function_download)
            rdfdocstats.set_callback_function_extraction(self.callback_function_extraction)
            rdfdocstats.set_callback_function_statistics(self.callback_stats)
            rdfdocstats.start_statistics()
        except NotModified, errorstr:
            log.warning("not modified")
            modified = False
        except Exception, errorstr:
            log.error(errorstr)
            error = errorstr

        if error is None and (modified or rdfdoc_to_do.current_stats is None):
            stat_result.triples = rdfdocstats.get_no_of_triples()
            stat_result.void = rdfdocstats.voidify('turtle')
            stat_result.warnings = rdfdocstats.get_no_of_warnings()
            if stat_result.warnings > 0:
                stat_result.last_warning = unicode(rdfdocstats.last_warning.message, errors='replace')
            stat_result.has_errors = False
            stat_result.errors = None
            stats_results = rdfdocstats.get_stats_results()
            for class_uri,usage_count in stats_results['usedclasses']['usage_count'].iteritems():
                c = Session.query(model.RDFClass).filter(model.RDFClass.uri==class_uri).first()
                if c is None:
                    c = model.RDFClass()
                    c.uri = class_uri
                    Session.add(c)
                rcs = model.RDFClassStat()
                rcs.rdf_class = c
                rcs.stat_result = stat_result
                rcs.count = usage_count
                Session.add(rcs)
            # vocab:
            for base_uri,result in stats_results['vocabularies'].iteritems():
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
            for property_uri,result in stats_results['propertyusage']['usage_count'].iteritems():
                p = Session.query(model.RDFProperty).filter(model.RDFProperty.uri==property_uri).first()
                if p is None:
                    p = model.RDFProperty(uri=property_uri)
                    Session.add(p)
                rps = model.RDFPropertyStat(rdf_property=p, stat_result=stat_result, count=result)
                Session.add(rps)
            # defined classes
            for class_uri,result in stats_results['classesdefined']['usage_count'].iteritems():
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
            stat_result.entities = stats_results['entities']['count']
            stat_result.literals = stats_results['literals']['count']
            stat_result.blanks = stats_results['blanksassubject']['count'] + stats_results['blanksasobject']['count']
            stat_result.blanks_as_subject = stats_results['blanksassubject']['count']
            stat_result.blanks_as_object = stats_results['blanksasobject']['count']
            stat_result.subclasses = stats_results['subclassusage']['count']
            stat_result.typed_subjects = stats_results['typedsubjects']['count']
            stat_result.labeled_subjects = stats_results['labeledsubjects']['count']
            # hierarchy depth
            print stats_results['propertyhierarchydepth']
            if stats_results['classhierarchydepth']['count'] > 0:
                stat_result.class_hierarchy_depth = stats_results['classhierarchydepth']['count'][max(rdfdocstats.stats_results['classhierarchydepth']['count'],
                    key=stats_results['classhierarchydepth']['count'].get)]
            if stats_results['propertyhierarchydepth']['count'] > 0:
                stat_result.property_hierarchy_depth = stats_results['propertyhierarchydepth']['count'][max(stats_results['propertyhierarchydepth']['count'],
                    key=stats_results['propertyhierarchydepth']['count'].get)]
            # averages
            stat_result.properties_per_entity = stats_results['propertiesperentity']['avg']
            stat_result.string_length_typed = stats_results['stringlength']['avg_typed']
            stat_result.string_length_untyped = stats_results['stringlength']['avg_untyped']
            # links
            stat_result.links = stats_results['links']['count']
            # datatypes
            for d_uri,result in stats_results['datatypes'].iteritems():
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
            for code,result in stats_results['languages'].iteritems():
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
            from collections import OrderedDict
            namespacelinks_ordered = OrderedDict(stats_results['links']['namespacelinks'])
            nsl_count = 0
            for link_uri,result in namespacelinks_ordered.iteritems():
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
                nsl_count += 1
                if nsl_count >= 500:
                    break
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


if __name__ == "__main__":
    do_stats = DoStats(None)
    do_stats.command()
