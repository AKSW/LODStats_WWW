"""
Copyright 2015 Ivan Ermilov <iermilov@informatik.uni-leipzig.de>

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
from paste.deploy import appconfig
from rdfstats.config.environment import load_environment

config_file = '../production.ini'
conf = appconfig('config:%s' % config_file, relative_to='.')
load_environment(conf.global_conf, conf.local_conf)

from rdfstats.model.meta import Session
from rdfstats import model

#Messaging - using module from csv2rdf-wiki
import codecs
import json
import rdflib
import re

class GetVoid(object):
    def getVoid(self):
        #Join on rdfdoc here (!) replace uri of the dataset with the http://lodstats.aksw.org/stat_result/6702.void
        statResults = Session.query(model.StatResult, model.RDFDoc).\
                              filter(model.StatResult.rdfdoc_id==model.RDFDoc.id).\
                              all()
        void = [];
        for statResult, rdfdoc in statResults:
            if(statResult.void is not None):
                try:
                    statResultUri = "http://lodstats.aksw.org/stat_result/"+str(statResult.id)+".void"
                    if(re.search("<http://stats.lod2.eu/rdf/void/.source.*>" , statResult.void)):
                        replacedVoid = re.sub("<http...stats.lod2.eu.rdf.void..source.*>", "<"+statResultUri+">", statResult.void)
                        f = codecs.open("./void/"+str(statResult.id)+".ttl", 'w', 'utf-8')
                        f.write(replacedVoid)
                        f.close()
                    else:
                        g=rdflib.Graph()
                        g.parse(data=statResult.void, format='turtle')
                        result = g.update("""
                                INSERT 
                                   {<"""+statResultUri+"""> ?p ?o} 
                                WHERE 
                                   {
                                     ?s ?p ?o . 
                                     ?s <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://rdfs.org/ns/void#dataset> 
                                   }
                                """)
                        g.commit()
                        result = g.query("""
                                SELECT 
                                   DISTINCT ?s ?p ?o 
                                WHERE {
                                  ?s ?p ?o . 
                                  ?s <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://rdfs.org/ns/void#dataset> . 
                                  FILTER(?s != <"""+statResultUri+""">)
                                  }
                                """)
                        subjToDelete = "";
                        for res in result: subjToDelete = res.s; break;
                        g.remove((subjToDelete, None, None))
                        g.commit()
                        f = codecs.open("./void/"+str(statResult.id)+".nt", 'w', 'utf-8')
                        f.write(g.serialize(format="nt"))
                        f.close()
                except BaseException as e:
                    print str(e)

if __name__ == "__main__":
    getVoid = GetVoid()
    getVoid.getVoid()

