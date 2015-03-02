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

from rdfstats.commands.lodstats_listener import LodstatsListener

try:
    import cPickle as pickle
except:
    import pickle


class SynchronizeCkan(LodstatsListener):
    # Parser configuration
    summary = "Read the /tmp/ckan_catalogs.pickled file and push the new datasets to lodstats"
    usage = "paster-2.6 --plugin=Rdfstats admin"
    group_name = "rdfstats"
    parser = Command.standard_parser(verbose=False)
    
    def command(self):
        ckanCatalogPath = "/tmp/ckan_catalogs.pickled"
        f = open(ckanCatalogPath, 'rU')
        ckanCatalogs = pickle.load(f)
        f.close()
        for catalog in ckanCatalogs:
            prefix = catalog['prefix'] #datagov
            ckanApiUrl = catalog['ckanApiUrl'] #http://catalog.data.gov/api
            packages = catalog['rdfpackages']
            for package in packages:
                rdfPackageName = package['name'] #name is a part of URI http://catalog.data.gov/dataset/name
                #just pickup first resource which is not None
                rdfResource = None
                for resource in package['resources']:
                    if(resource is not None):
                        rdfResource = resource
                        break
                rdfResourceUrl = rdfResource['url']
                rdfResourceFormat = rdfResource['format']

                rdfdoc = Session.query(model.RDFDoc).filter(model.RDFDoc.name==rdfPackageName).first()
                if(rdfdoc):
                    continue
                else:
                    newRdfdoc = model.RDFDoc(name=rdfPackageName, uri=rdfResourceUrl, format=rdfResourceFormat, ckan_catalog=prefix)
                    Session.add(newRdfdoc)
                    Session.commit()

    def normalizeFormat(self):
        #accepted formats:
        #ttl, n3, nt, nq, rdf, sparql, sitemap

        pass
