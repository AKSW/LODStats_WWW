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

import ckanclient

class DoUpdate(Command):
    # Parser configuration
    summary = "get/update RDF packages from CKAN"
    usage = "paster-2.6 --plugin=Rdfstats rdf_ckan_update"
    group_name = "rdfstats"
    parser = Command.standard_parser(verbose=False)
    
    def term_handler(self, signum, frame):
        Session.rollback()
        sys.exit(0)

    def command(self):
        
        self.logging_file_config(config_file)
        log = logging.getLogger(__name__)
        
        self.worker_proc = None
        self.rdfdoc_to_do = None
        
        signal.signal(signal.SIGINT, self.term_handler)
        signal.signal(signal.SIGTERM, self.term_handler)
        
        # do not spawn more than two workers
        number_of_workers = Session.query(model.WorkerProc).with_lockmode('read').count()
        if number_of_workers >= 2:
            return 0
        
        ckan = ckanclient.CkanClient(base_location=conf['ckan.base']+'api', api_key=conf['ckan.api_key'])
        
        error = None
        try:
            package_list = ckan.package_register_get()
        except Exception, errorstr:
            log.error(str(errorstr))
            sys.exit(23)
        
        # check for orphaned local pkgs
        all_local_pkgs = Session.query(model.RDFDoc).all()
        for pkg in all_local_pkgs:
            if pkg.name not in package_list:
                log.debug("%s is gone and will be deleted" % pkg.name)
                Session.delete(pkg)
                Session.commit()
            
        for package_name in package_list:
            try:
                package = ckan.package_entity_get(package_name)
            except Exception, errorstr:
                log.debug("ERROR with %s: %s" % (package_name, errorstr))
                continue
            
            rdfdoc = Session.query(model.RDFDoc).filter(model.RDFDoc.name==package['name']).first()
            if rdfdoc is None:
                rdfdoc = model.RDFDoc()
                Session.add(rdfdoc)
                rdfdoc.name = package['name']
                        
            class BreakIt:
                pass

            try:    
                for resource in package['resources']:
                    if resource['format'].lower() in ["application/x-ntriples", "nt", "gzip:ntriples"]:
                        rdfdoc.format = "nt"
                        rdfdoc.uri = resource['url']
                        raise BreakIt
                for resource in package['resources']:
                    if resource['format'].lower() in ["application/x-nquads", "nquads"]:
                        rdfdoc.format = "nq"
                        rdfdoc.uri = resource['url']
                        raise BreakIt
                for resource in package['resources']:
                    if resource['format'].lower() in ["application/rdf+xml", "rdf"]:
                        rdfdoc.format = "rdf"
                        rdfdoc.uri = resource['url']
                        raise BreakIt
                for resource in package['resources']:
                    if resource['format'].lower() in ["text/turtle", "rdf/turtle", "ttl"]:
                        rdfdoc.format = "ttl"
                        rdfdoc.uri = resource['url']
                        raise BreakIt
                for resource in package['resources']:
                    if resource['format'].lower() in ["text/n3", "n3"]:
                        rdfdoc.format = "n3"
                        rdfdoc.uri = resource['url']
                        raise BreakIt
                for resource in package['resources']:
                    if resource['format'].lower() in ["api/sparql", "sparql"]:
                        # prefer a sitemap.xml over sparql, if any
                        for sitemap_resource in package['resources']:
                            if sitemap_resource['format'].lower() in ["meta/sitemap"]:
                                rdfdoc.format = "sitemap"
                                rdfdoc.uri = sitemap_resource['url']
                                raise BreakIt
                        rdfdoc.format = "sparql"
                        rdfdoc.uri = resource['url']
            except BreakIt:
                pass
            if rdfdoc.format is not None:
                Session.commit()
            else:
                Session.rollback()
