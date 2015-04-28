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

import RDF
import urllib

class ExportRdf(LodstatsListener):
    # Parser configuration
    summary = "Read the /tmp/ckan_catalogs.pickled file and push the new datasets to lodstats"
    usage = "paster-2.6 --plugin=Rdfstats admin"
    group_name = "rdfstats"
    parser = Command.standard_parser(verbose=False)
    
    def command(self):
        print("Loading RDF database...")
        rdfStorage = RDF.FileStorage("lodstatsrdf")
        rdfModel = RDF.Model(rdfStorage)
        print("Finished!")

        ckanCatalogPath = "/tmp/ckan_catalogs.pickled"
        print("Reading " + ckanCatalogPath)
        f = open(ckanCatalogPath, 'rU')
        ckanCatalogs = pickle.load(f)
        f.close()
        print("Finished!")
        #Fetch the all rdfdocs from the DB
        print("Fetching the data from DB...")
        rdfdocs = Session.query(model.RDFDoc).all()
        print("Fetched the data from DB!")
        overall = len(rdfdocs)
        for num, rdfdoc in enumerate(rdfdocs):
            print("Processing %d out of %d" % (num, overall))
            try:
                self.generateRdfForRdfDoc(rdfdoc, rdfModel, ckanCatalogs)
            except BaseException as e:
                print("Oops, exception occured: "+str(e))

        serializer = RDF.Serializer(name="ntriples")
        serializer.serialize_model_to_file("lodstats.nt", rdfModel, base_uri=None)

    def generateRdfForRdfDoc(self, rdfdoc, rdfModel, ckanCatalogs):
        rdfdocName = rdfdoc.name
        ckanEntry = self.lookupCkanEntryByName(rdfdocName, ckanCatalogs)

        if(ckanEntry == '' or ckanEntry == None):
            return 0
        ckanUrl = ckanEntry.get('ckan_url', '')
        rdfdocUriNode = RDF.Node(RDF.Uri(ckanEntry['ckan_url']))
        rdfdocUriNodeOrig = RDF.Node(RDF.Uri("http://lodstats.aksw.org/rdfdocs/"+str(rdfdoc.id)))
        
        # generic
        rdf = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
        rdfTypeProperty = RDF.Node(RDF.Uri(rdf + "type"))
        rdfs = "http://www.w3.org/2000/01/rdf-schema#"
        rdfsLabelProperty = RDF.Node(RDF.Uri(rdfs + "label"))
        rdfsCommentProperty = RDF.Node(RDF.Uri(rdfs + "comment"))
    
        # Datatypes
        xsd = "http://www.w3.org/2001/XMLSchema#"
        xsdDateTimeDatatype = RDF.Node(RDF.Uri(xsd + "dateTime"))
        xsdStringDatatype = RDF.Node(RDF.Uri(xsd + "string"))

        dct = "http://purl.org/dc/terms/"
        dctPublisherProperty = RDF.Node(RDF.Uri(dct + "publisher"))
        dctCreatedProperty = RDF.Node(RDF.Uri(dct + "created"))

        foaf = "http://xmlns.com/foaf/0.1/"
        foafOrganizationNode = RDF.Node(RDF.Uri(foaf + "Organization"))
        foafLogoProperty = RDF.Node(RDF.Uri(foaf + "logo"))
        foafMboxProperty = RDF.Node(RDF.Uri(foaf + "mbox"))
        # Publisher related properties and classes
        if(rdfdoc.ckan_catalog=="datagov"):
            ckanBase = "http://catalog.data.gov/"
        elif(rdfdoc.ckan_catalog=="pdeu"):
            ckanBase = "http://publicdata.eu/"
        else:
            ckanBase = "http://datahub.io/"
        organizationBase = ckanBase + "organization/"
        organizationName = ''
        organization = ckanEntry.get('organization', '')
        if(organization != '' and organization != None):
            organizationName = organization.get('name', '')
        if(organization != '' and organizationName != ''):
            publisherUri = organizationBase + ckanEntry['organization']['name']
            publisherUriNode = RDF.Node(RDF.Uri(publisherUri))

            publisherLogo = organization.get('image_url') or 'http://example.com/nologo'
            publisherLogoNode = RDF.Node(RDF.Uri(publisherLogo))
            publisherTitle = ckanEntry['organization']['title']
            publisherTitleNode = RDF.Node(literal=publisherTitle)
            publisherDescription = ckanEntry['organization']['description']
            publisherDescriptionNode = RDF.Node(literal=publisherDescription)
            publisherCreated = ckanEntry['organization']['created']
            publisherCreatedNode = RDF.Node(literal=publisherCreated)
            publisherEmailNode = RDF.Node(literal=ckanEntry['author_email'])

            #Publisher triples
            rdfModel.append(RDF.Statement(rdfdocUriNode, dctPublisherProperty, publisherUriNode))
            rdfModel.append(RDF.Statement(publisherUriNode, rdfTypeProperty, foafOrganizationNode))
            rdfModel.append(RDF.Statement(publisherUriNode, foafLogoProperty, publisherLogoNode))
            rdfModel.append(RDF.Statement(publisherUriNode, rdfsLabelProperty, publisherTitleNode))
            rdfModel.append(RDF.Statement(publisherUriNode, rdfsCommentProperty, publisherDescriptionNode))
            rdfModel.append(RDF.Statement(publisherUriNode, dctCreatedProperty, publisherCreatedNode))
            rdfModel.append(RDF.Statement(publisherUriNode, foafMboxProperty, publisherEmailNode))

        #License
        dctLicenseProperty = RDF.Node(RDF.Uri(dct + "license"))
        licenseUrl = ckanEntry.get('license_url', '')
        if(licenseUrl != '' and licenseUrl != None): 
            licenseUrlNode = RDF.Node(RDF.Uri(licenseUrl))
            #License triples
            rdfModel.append(RDF.Statement(rdfdocUriNode, dctLicenseProperty, licenseUrlNode))
        
        #other stuff
        dctIssued = dct + "issued"
        dctIssuedProperty = RDF.Node(RDF.Uri(dctIssued))
        ckanEntryMetadataCreatedNode = RDF.Node(literal=ckanEntry['metadata_created'])

        dctModifiedProperty = RDF.Node(RDF.Uri(dct + "modified"))
        ckanEntryMetadataModifiedNode = RDF.Node(literal=ckanEntry['metadata_modified'])

        ckanEntryComment = RDF.Node(literal=ckanEntry['notes'])

        dcat = "http://www.w3.org/ns/dcat#"
        dcatKeywordProperty = RDF.Node(RDF.Uri(dcat + "keyword"))

        ckanEntryTitleNode = RDF.Node(literal=ckanEntry['title'])

        schema = "http://schema.org/"
        schemaAggregateRatingProperty = RDF.Node(RDF.Uri(schema + "aggregateRating"))
        schemaReviewCount = RDF.Node(RDF.Uri(schema + "reviewCount"))
        ckanRatingAverageNode = RDF.Node(literal=str(ckanEntry['ratings_average']))
        ckanReviewCountNode = RDF.Node(literal=str(ckanEntry['ratings_count']))

        ckanType = RDF.Node(literal=ckanEntry['type'])
        owl = "http://www.w3.org/2002/07/owl#"
        owlSameAsProperty = RDF.Node(RDF.Uri(owl + "sameAs"))

        #other stuff triples
        rdfModel.append(RDF.Statement(rdfdocUriNode, dctIssuedProperty, ckanEntryMetadataCreatedNode))
        rdfModel.append(RDF.Statement(rdfdocUriNode, dctModifiedProperty, ckanEntryMetadataModifiedNode))
        rdfModel.append(RDF.Statement(rdfdocUriNode, rdfsCommentProperty, ckanEntryComment))
        rdfModel.append(RDF.Statement(rdfdocUriNode, rdfsLabelProperty, ckanEntryTitleNode))
        rdfModel.append(RDF.Statement(rdfdocUriNode, schemaAggregateRatingProperty, ckanRatingAverageNode))
        rdfModel.append(RDF.Statement(rdfdocUriNode, schemaReviewCount, ckanReviewCountNode))
        rdfModel.append(RDF.Statement(rdfdocUriNode, rdfTypeProperty, ckanType))
        rdfModel.append(RDF.Statement(rdfdocUriNode, owlSameAsProperty, rdfdocUriNodeOrig))

        #tags
        for tag in ckanEntry['tags']:
            tagNode = RDF.Node(literal=tag)
            tagStatement = RDF.Statement(rdfdocUriNode, dcatKeywordProperty, tagNode)
            rdfModel.append(tagStatement)

        #extras
        #define a lodstats namespace for this right
        lodstatsExtras = "http://lodstats.aksw.org/ontology/extras/"
        for extra in ckanEntry['extras']:
            extraStr = unicode(ckanEntry['extras'][extra])
            extraNode = RDF.Node(literal=extraStr)
            extraProperty = RDF.Node(RDF.Uri(lodstatsExtras + urllib.quote(extra)))
            extraStatement = RDF.Statement(rdfdocUriNode, extraProperty, extraNode)
            rdfModel.append(extraStatement)

    def lookupCkanEntryByName(self, rdfdocName, ckanCatalogs):
        ckanEntry = None
        for catalog in ckanCatalogs:
            for package in catalog['rdfpackages']:
                if(package['name'] == rdfdocName):
                    ckanEntry = package
                    break
            if(ckanEntry != None):
                break
        return ckanEntry
