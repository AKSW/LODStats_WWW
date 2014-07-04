import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from rdfstats.lib.base import BaseController, render, Session

from rdfstats import model

import json

from copy import copy

import cPickle as pickle
import uuid
import os.path

log = logging.getLogger(__name__)

class SearchController(BaseController):
    """REST Controller styled on the Atom Publishing Protocol"""
    # To properly map this controller, ensure your config/routing.py
    # file has a resource setup:
    #     map.resource('searchone', 'search', controller='property/search',
    #         path_prefix='/property', name_prefix='property_')

    def index(self, format='html'):
        """GET /property/search: All items in the collection"""
        # url('property_search')

    def create(self):
        """POST /property/search: Create a new item"""
        # url('property_search')
        #POST here JSON with all the classes extracted
        headers = json.loads(request.params['headers'])
        entities = json.loads(request.params['entities']) 

        headersWithSuggestions = self._getSuggestionsForHeaders(headers)
        rankedHeadersWithSuggestions = self._rankSuggestionsForHeaders(headersWithSuggestions, entities)
        return json.dumps(rankedHeadersWithSuggestions)

    def _rankSuggestionsForHeaders(self, headersWithSuggestions, entities):
        headersWithSuggestionsOut = list()
        for num, header in enumerate(headersWithSuggestions):
            headerName = header.keys()[0]
            headerBody = header[headerName]

            headerWithSuggestionsOut = dict()
            headerWithSuggestionsOut[headerName] = list()
            for headerItem in headerBody:
                headerItemOut = list()
                headerItemOut.append(headerItem[0])
                headerItemOut.append(headerItem[1])
                suggestions = headerItem[2]
                for suggestion in suggestions:
                    suggestion['rank'] = self._rankSuggestionLodstats(suggestion['uri'], entities)
                #sort by rank
                headerItemOut.append(sorted(suggestions, key=lambda k: k['rank'], reverse=True))
                headerWithSuggestionsOut[headerName].append(headerItemOut)
            headersWithSuggestionsOut.append(headerWithSuggestionsOut)

        return headersWithSuggestionsOut

    def _rankSuggestionLodstats(self, suggestionUri, entities):
        #The most time consuming - implement caching here
        #just cache to /tmp for now
        cacheId = uuid.uuid5(uuid.NAMESPACE_URL, suggestionUri.join(sorted(entities)).encode('utf-8'))
        cachePath = '/tmp/'
        cacheNamespace = 'suggestionsCache'
        cacheEntry = str(cachePath) + str(cacheNamespace) + str(cacheId)
        if(os.path.exists(cacheEntry)):
            return pickle.load(open(cacheEntry, 'rb'))

        propertyQuery = """SELECT stat_result_id 
                   FROM rdf_property_stat, rdf_property 
                   WHERE rdf_property.id=rdf_property_stat.rdf_property_id 
                   AND rdf_property.uri='%s';""" % suggestionUri
        q = Session.execute(propertyQuery)
        propertyDatasets = set()
        for row in q:
            propertyDatasets.add(row[0])

        entitiesDatasets = set()
        for entityUrl in entities:
            classQuery = """SELECT stat_result_id
                            FROM rdf_class_stat_result, rdf_class
                            WHERE rdf_class_stat_result.rdf_class_id=rdf_class.id 
                            AND rdf_class.uri='%s';""" % entityUrl
            q = Session.execute(classQuery)
            for row in q:
                entitiesDatasets.add(row[0])
            propertyQuery = """SELECT stat_result_id 
                       FROM rdf_property_stat, rdf_property 
                       WHERE rdf_property.id=rdf_property_stat.rdf_property_id 
                       AND rdf_property.uri='%s';""" % entityUrl
            q = Session.execute(propertyQuery)
            for row in q:
                entitiesDatasets.add(row[0])
                
        common = propertyDatasets.intersection(entitiesDatasets)
        pickle.dump(len(common), open(cacheEntry, 'wb'), protocol=pickle.HIGHEST_PROTOCOL)
        return len(common)

    def _getSuggestionsForHeaders(self, headers):
        suggestions = []        
        for header in headers:
            headerName = header.keys()[0]
            headerBody = header[headerName]
            headerSuggestions = {headerName: []}
            for (num, headerItem) in headerBody:
                headerItemSuggestions = (num, headerItem, [])
                q = self._getProperties(headerItem)
                for row in q:
                    suggestion = {'rdf_property_id': row.rdf_property_id,
                                  'count': row.count,
                                  'uri': row.uri,
                                  'label_en': row.label_en}
                    headerItemSuggestions[2].append(suggestion)
                headerSuggestions[headerName].append(headerItemSuggestions)
            suggestions.append(headerSuggestions)
        return suggestions

    def new(self, format='html'):
        """GET /property/search/new: Form to create a new item"""
        # url('property_new_searchone')

    def update(self, id):
        """PUT /property/search/id: Update an existing item"""
        # Forms posted to this method should contain a hidden field:
        #    <input type="hidden" name="_method" value="PUT" />
        # Or using helpers:
        #    h.form(url('property_searchone', id=ID),
        #           method='put')
        # url('property_searchone', id=ID)

    def delete(self, id):
        """DELETE /property/search/id: Delete an existing item"""
        # Forms posted to this method should contain a hidden field:
        #    <input type="hidden" name="_method" value="DELETE" />
        # Or using helpers:
        #    h.form(url('property_searchone', id=ID),
        #           method='delete')
        # url('property_searchone', id=ID)

    def show(self, id, format='html'):
        """GET /property/search/id: Show a specific item"""
        # url('property_searchone', id=ID)
        response.headers['Access-Control-Allow-Origin'] = "*"
        result = self._getPropertiesJson(id)
        return json.dumps(result)

    def _getPropertiesJson(self, searchString, limit=100):
        q = self._getProperties(searchString, limit)
        result = {}
        result['suggestions'] = []
        for row in q:
            object = {'uri': row.uri,
                      'label_en': row.label_en}
            result['suggestions'].append(object)
        return result

    def _getProperties(self, searchString, limit=100):
        searchterms = searchString.split(' ')
        searchterms = '|'.join(searchterms)
        q = Session.query(model.PropertyLabeled).filter('label_en_index_col ' \
                                                        '@@ to_tsquery(:terms)')
        q = q.params(terms=searchterms)
        q = q.order_by('count DESC')
        q = q.limit(limit)
        return q

    def edit(self, id, format='html'):
        """GET /property/search/id/edit: Form to edit an existing item"""
        # url('property_edit_searchone', id=ID)
