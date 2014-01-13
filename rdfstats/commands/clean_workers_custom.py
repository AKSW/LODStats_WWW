import pdb
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

from rdfstats.model.meta import Session
from rdfstats import model

dataset_id = 1440

class DoCleanWorkers(Command):
    # Parser configuration
    summary = "Administration functions for LODStats"
    usage = "paster-2.6 --plugin=Rdfstats admin"
    group_name = "rdfstats"
    parser = Command.standard_parser(verbose=False)
    
    def command(self):

        rdfdoc_to_do = Session.query(model.RDFDoc).filter(model.RDFDoc.id == dataset_id).with_lockmode('update')\
                    .order_by(model.RDFDoc.last_updated).first()
        if rdfdoc_to_do is None:
            return 0

        print rdfdoc_to_do.reset_current_stats_and_worker()
        #for entry in rdfdoc:
            #entry.worked_on = False
        
        #worker_proc = Session.query(model.WorkerProc).all()
        #print worker_proc    

        #for wp in worker_proc:
            #Session.delete(wp)

        #Session.commit()
