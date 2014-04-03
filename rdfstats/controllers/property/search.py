import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from rdfstats.lib.base import BaseController, render, Session

from rdfstats import model

import json

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
        searchterms = id.split(' ')
        searchterms = '|'.join(searchterms)
        q = Session.query(model.PropertyLabeled).filter('label_en_index_col ' \
                                                        '@@ to_tsquery(:terms)')
        q = q.params(terms=searchterms)
        q = q.order_by('count DESC')
        q = q.limit(10)
        result = {}
        result['suggestions'] = []
        for row in q:
            object = {'uri': row.uri,
                      'label_en': row.label_en}
            result['suggestions'].append(object)
        return json.dumps(result)

    def edit(self, id, format='html'):
        """GET /property/search/id/edit: Form to edit an existing item"""
        # url('property_edit_searchone', id=ID)
