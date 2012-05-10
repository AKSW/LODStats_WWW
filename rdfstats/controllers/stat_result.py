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
import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from rdfstats.lib.base import BaseController, render, Session

from rdfstats import model

log = logging.getLogger(__name__)

class StatResultController(BaseController):
    """REST Controller styled on the Atom Publishing Protocol"""
    # To properly map this controller, ensure your config/routing.py
    # file has a resource setup:
    #     map.resource('stat_result', 'stat_result')

    def index(self, format='html'):
        """GET /stat_result: All items in the collection"""
        # url('stat_result')

    def create(self):
        """POST /stat_result: Create a new item"""
        # url('stat_result')

    def new(self, format='html'):
        """GET /stat_result/new: Form to create a new item"""
        # url('new_stat_result')

    def update(self, id):
        """PUT /stat_result/id: Update an existing item"""
        # Forms posted to this method should contain a hidden field:
        #    <input type="hidden" name="_method" value="PUT" />
        # Or using helpers:
        #    h.form(url('stat_result', id=ID),
        #           method='put')
        # url('stat_result', id=ID)

    def delete(self, id):
        """DELETE /stat_result/id: Delete an existing item"""
        # Forms posted to this method should contain a hidden field:
        #    <input type="hidden" name="_method" value="DELETE" />
        # Or using helpers:
        #    h.form(url('stat_result', id=ID),
        #           method='delete')
        # url('stat_result', id=ID)

    def show(self, id, format='html'):
        """GET /stat_result/id: Show a specific item"""
        # url('stat_result', id=ID)
        if id is None:
            abort(404)
        c.stats = Session.query(model.StatResult).get(int(id))
        if c.stats is None:
            abort(404)
        if format=='void':
            response.content_type = 'text/plain'
            return render('/stat_result/void.txt')
        if format=='json' or 'application/json' in request.headers.get('accept', ''):
            import json
            response.content_type = 'application/json'
            return json.dumps(c.stats.json_dict())
        return render('/stat_result/view.html')

    def edit(self, id, format='html'):
        """GET /stat_result/id/edit: Form to edit an existing item"""
        # url('edit_stat_result', id=ID)
