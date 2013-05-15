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

class UpdateFromFile(Command):
    # Parser configuration
    summary = "get/update RDF packages from CKAN"
    usage = "paster-2.6 --plugin=Rdfstats update_from_file"
    group_name = "rdfstats"
    parser = Command.standard_parser(verbose=False)
    
    def term_handler(self, signum, frame):
        Session.rollback()
        sys.exit(0)

    def command(self):

        self.logging_file_config(config_file)
        log = logging.getLogger(__name__)

        import csv
        f = open("rdf_for_lodstats", 'rU')
        list = csv.DictReader(f)
        package_list = []

        for line in list:
            package_list.append(line)
        f.close()

        #print package_list

        package_list_names = []
        for item in package_list:
            package_list_names.append(item['package_name'])
        
        #print package_list_names

        self.worker_proc = None
        self.rdfdoc_to_do = None
        
        signal.signal(signal.SIGINT, self.term_handler)
        signal.signal(signal.SIGTERM, self.term_handler)
        
        # do not spawn more than two workers
        number_of_workers = Session.query(model.WorkerProc).with_lockmode('read').count()
        if number_of_workers >= 2:
            return 0
        
        ## check for orphaned local pkgs
        #all_local_pkgs = Session.query(model.RDFDoc).all()
        #for pkg in all_local_pkgs:
            #if pkg.name not in package_list_names:
                #log.debug("%s is gone and will be deleted" % pkg.name)
                #Session.delete(pkg)
                #Session.commit()
            
        for package in package_list:

            rdfdoc = Session.query(model.RDFDoc).filter(model.RDFDoc.name==package['package_name']).first()
            if rdfdoc is None:
                rdfdoc = model.RDFDoc()
                Session.add(rdfdoc)
                rdfdoc.name = package['package_name']
                        
            rdfdoc.format = package['format']
            rdfdoc.uri = package['rdf_url']

            if rdfdoc.format is not None:
                Session.commit()
            else:
                Session.rollback()
