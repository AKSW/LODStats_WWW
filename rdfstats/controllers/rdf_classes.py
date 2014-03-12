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
import json

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from rdfstats.lib.base import BaseController, render, Session

from rdfstats import model
from sqlalchemy import and_, func, desc

from webhelpers.paginate import Page, PageURL_WebOb

log = logging.getLogger(__name__)

class RdfClassesController(BaseController):
    """REST Controller styled on the Atom Publishing Protocol"""
    # To properly map this controller, ensure your config/routing.py
    # file has a resource setup:
    #     map.resource('rdf_class', 'rdf_classes')

    def index(self, format='html'):
        """GET /rdf_classes: All items in the collection"""
        # url('rdf_classes')
        rdf_classes = Session.query(model.RDFClass.uri, model.RDFClass.id, func.sum(model.RDFClassStat.count),
                                    func.count(model.StatResult.id))\
                                    .join(model.RDFClassStat).join(model.StatResult)\
                                    .filter(model.StatResult.current_of!=None)\
                                    .group_by(model.RDFClass.uri, model.RDFClass.id)
        c.query_string = '?'
        # optional search
        c.search = ''
        if request.GET.has_key('search'):
            rdf_classes = rdf_classes.filter(model.RDFClass.uri.ilike("%%%s%%" % request.GET['search']))
            c.query_string += 'search=%s&' % request.GET['search']
            c.search = request.GET['search']
        # json
        if format=='json' or 'application/json' in request.headers.get('accept', ''):
            response.content_type = 'application/json'
            json_rdf_classes = []
            for cl in rdf_classes:
                json_rdf_classes.append({'uri': cl.uri, 'overall_sum': int(cl[1]), 'datasets': int(cl[2])})
            return json.dumps(json_rdf_classes)
        # sort results
        c.sort_order = request.GET.get('sort')
        if request.GET.has_key('sort'):
            if request.GET['sort'] == 'uri':
                c.rdf_classes = rdf_classes.order_by(model.RDFClass.uri)
            elif request.GET['sort'] == 'overall':
                c.rdf_classes = rdf_classes.order_by(desc(func.sum(model.RDFClassStat.count)),
                                desc(func.count(model.StatResult.id)), model.RDFClass.uri)
            elif request.GET['sort'] == 'datasets':
                c.rdf_classes = rdf_classes.order_by(desc(func.count(model.StatResult.id)),
                                desc(func.sum(model.RDFClassStat.count)), model.RDFClass.uri)
            else:
                c.rdf_classes = rdf_classes.order_by(desc(func.count(model.StatResult.id)),
                                desc(func.sum(model.RDFClassStat.count)), model.RDFClass.uri)
        else:
            c.rdf_classes = rdf_classes.order_by(desc(func.count(model.StatResult.id)),
                            desc(func.sum(model.RDFClassStat.count)), model.RDFClass.uri)
        if request.GET.has_key('page'):
            page = request.GET['page']
        else:
            page = 1
        page_url = PageURL_WebOb(request)
        c.rdf_classes_page = Page(c.rdf_classes, page=page, items_per_page=50, url=page_url)
        c.count = c.rdf_classes_page.item_count
        return render('/rdf_classes/index.html')

    def create(self):
        """POST /rdf_classes: Create a new item"""
        # url('rdf_classes')

    def new(self, format='html'):
        """GET /rdf_classes/new: Form to create a new item"""
        # url('new_rdf_class')

    def update(self, id):
        """PUT /rdf_classes/id: Update an existing item"""
        # Forms posted to this method should contain a hidden field:
        #    <input type="hidden" name="_method" value="PUT" />
        # Or using helpers:
        #    h.form(url('rdf_class', id=ID),
        #           method='put')
        # url('rdf_class', id=ID)

    def delete(self, id):
        """DELETE /rdf_classes/id: Delete an existing item"""
        # Forms posted to this method should contain a hidden field:
        #    <input type="hidden" name="_method" value="DELETE" />
        # Or using helpers:
        #    h.form(url('rdf_class', id=ID),
        #           method='delete')
        # url('rdf_class', id=ID)

    def show(self, id, format='html'):
        """GET /rdf_classes/id: Show a specific item"""
        # url('rdf_class', id=ID)
        if id is None:
            abort(404)
        try:
            c.rdf_class = Session.query(model.RDFClass).get(int(id))
        except ValueError, e:
            abort(404)
        if c.rdf_class is None:
            abort(404)
        c.cs=Session.query(model.RDFClassStat).join(model.StatResult).join(model.StatResult.current_of).filter(
            and_(
                model.RDFClassStat.rdf_class==c.rdf_class,
                model.StatResult.current_of!=None)).order_by(model.RDFDoc.name).all()
        c.count = len(c.cs)
        return render('/rdf_classes/view.html')

    def edit(self, id, format='html'):
        """GET /rdf_classes/id/edit: Form to edit an existing item"""
        # url('edit_rdf_class', id=ID)
