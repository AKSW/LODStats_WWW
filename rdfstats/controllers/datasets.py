import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from rdfstats.lib.base import BaseController, render, Session
from rdfstats import model

import json

from rdfstats.lib import helpers as h

log = logging.getLogger(__name__)

class DatasetsController(BaseController):
    """REST Controller styled on the Atom Publishing Protocol"""
    # To properly map this controller, ensure your config/routing.py
    # file has a resource setup:
    #     map.resource('dataset', 'datasets')

    def index(self, format='html'):
        """GET /datasets: All items in the collection"""
        # url('datasets')

    def create(self):
        """POST /datasets: Create a new item"""
        # url('datasets')

    def new(self, format='html'):
        """GET /datasets/new: Form to create a new item"""
        # url('new_dataset')

    def update(self, id):
        """PUT /datasets/id: Update an existing item"""
        # Forms posted to this method should contain a hidden field:
        #    <input type="hidden" name="_method" value="PUT" />
        # Or using helpers:
        #    h.form(url('dataset', id=ID),
        #           method='put')
        # url('dataset', id=ID)

    def delete(self, id):
        """DELETE /datasets/id: Delete an existing item"""
        # Forms posted to this method should contain a hidden field:
        #    <input type="hidden" name="_method" value="DELETE" />
        # Or using helpers:
        #    h.form(url('dataset', id=ID),
        #           method='delete')
        # url('dataset', id=ID)

    def show(self, id, format='html'):
        """GET /datasets/id: Show a specific item"""
        # url('dataset', id=ID)
        import re
        id = re.sub("http:/", "http://", id)
        try:
            dataset = Session.query(model.RDFDoc).filter(model.RDFDoc.uri==id).one()
            output_url = h.url(controller="rdfdocs", action="show", id=dataset.id, qualified=True)
            return json.dumps(output_url)
        except:
            return json.dumps('')

    def edit(self, id, format='html'):
        """GET /datasets/id/edit: Form to edit an existing item"""
        # url('edit_dataset', id=ID)
