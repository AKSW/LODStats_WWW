"""
Copyright 2014 Ivan Ermilov <iermilov@informatik.uni-leipzig.de>

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

from rdfstats.model.meta import Session
from rdfstats import model

#Messaging - using module from csv2rdf-wiki
from csv2rdf.messaging import Messaging
import json

class ProcessById(Command):
    # Parser configuration
    summary = "Administration functions for LODStats"
    usage = "paster-2.6 --plugin=Rdfstats admin"
    group_name = "rdfstats"
    parser = Command.standard_parser(verbose=False)
    
    def command(self):
        id = self.args[0]
        exchange = "lodstats_datasets_exchange"
        queue = "lodstats_datasets_queue"
        message_broker = Messaging()
        message_broker.declareDirectExchange(exchange)
        message_broker.declareQueue(queue)
        message_broker.bindExchangeToQueue(exchange, queue)
        rdfdoc = Session.query(model.RDFDoc).filter(model.RDFDoc.in_datahub==True, model.RDFDoc.id==id).one()
        dataset = {
                'id': rdfdoc.id,
                }
        message = json.dumps(dataset)
        message_broker.sendMessageToQueue(queue, message)
