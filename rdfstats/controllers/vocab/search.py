import logging
import json

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from rdfstats.lib.base import BaseController, render, Session

log = logging.getLogger(__name__)

class SearchController(BaseController):
    """REST Controller styled on the Atom Publishing Protocol"""
    # To properly map this controller, ensure your config/routing.py
    # file has a resource setup:
    #     map.resource('search', 'search', controller='vocabulary/search',
    #         path_prefix='/vocabulary', name_prefix='vocabulary_')

    def index(self, format='html'):
        """GET /vocab/search: All items in the collection"""
        # url('vocabulary_search')

    def create(self):
        """POST /vocab/search: Create a new item"""
        # url('vocabulary_search')

    def new(self, format='html'):
        """GET /vocab/search/new: Form to create a new item"""
        # url('vocabulary_new_search')

    def update(self, id):
        """PUT /vocabulary/search/id: Update an existing item"""
        # Forms posted to this method should contain a hidden field:
        #    <input type="hidden" name="_method" value="PUT" />
        # Or using helpers:
        #    h.form(url('vocabulary_search', id=ID),
        #           method='put')
        # url('vocabulary_search', id=ID)

    def delete(self, id):
        """DELETE /vocabulary/search/id: Delete an existing item"""
        # Forms posted to this method should contain a hidden field:
        #    <input type="hidden" name="_method" value="DELETE" />
        # Or using helpers:
        #    h.form(url('vocabulary_search', id=ID),
        #           method='delete')
        # url('vocabulary_search', id=ID)

    def show(self, id, format='html'):
        """GET /vocabulary/search/id: Show a specific item"""
        # url('vocabulary_search', id=ID)
        import re
        id = re.sub("http:/", "http://", id)
        query = """
            SELECT DISTINCT rdfdoc.id, rdfdoc.uri
            FROM rdfdoc, stat_result, rdf_property_stat, rdf_property
            WHERE rdf_property.uri='%s' AND
            rdf_property.id=rdf_property_stat.rdf_property_id AND
            rdf_property_stat.stat_result_id=stat_result.id AND
            stat_result.rdfdoc_id=rdfdoc.id
            ORDER BY rdfdoc.id;
        """ % (id)
        try:
            datasets = []
            result = Session.execute(query)
            for row in result:
                obj = {"id": row[0],
                    "uri": row[1]}
                datasets.append(obj)
            return json.dumps(datasets)
        except:
            return json.dumps('')

    def edit(self, id, format='html'):
        """GET /vocabulary/search/id/edit: Form to edit an existing item"""
        # url('vocabulary_edit_search', id=ID)
