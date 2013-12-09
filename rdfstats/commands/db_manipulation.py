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
import subprocess
import logging

from lodstats import RDFStats
from lodstats.stats import lodstats as lodstats_stats
from lodstats.exceptions import NotModified 

class DoDB(Command):
    # Parser configuration
    summary = "Administration functions for LODStats"
    usage = "paster-2.6 --plugin=Rdfstats db_manipulation"
    group_name = "rdfstats"
    parser = Command.standard_parser(verbose=False)

    def command(self):
        self.logging_file_config(config_file)
        log = logging.getLogger(__name__)

        rdfdocs = Session.query(model.RDFDoc).all()
        warn = 0
        for rdfdoc in rdfdocs:
            script_path = "/home/lodstats/.virtualenvs/thedatahub/src/CSV2RDF-WIKI/csv2rdf/scripts/generate_resource_name.py"
            (output, error) = subprocess.Popen([script_path, "-r", str(rdfdoc.uri)], stdout=subprocess.PIPE).communicate()
            print rdfdoc.name, rdfdoc.uri, output.strip()

    def get_rdfdoc_by_name(self, name):
        return Session.query(model.RDFDoc).filter(model.RDFDoc.name==name).first()

    def get_rdfdoc_by_id(self, id):
        return Session.query(model.RDFDoc).filter(model.RDFDoc.id==id).first()
        
    def get_stats_by_id(self, id):
        return Session.query(model.StatResult).filter(model.StatResult.id==id).first()
