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

class PropertiesController(BaseController):
    """REST Controller styled on the Atom Publishing Protocol"""
    # To properly map this controller, ensure your config/routing.py
    # file has a resource setup:
    #     map.resource('property', 'properties')

    def index(self, format='html'):
        """GET /properties: All items in the collection"""
        # url('properties')
        rdf_properties = Session.query(model.RDFProperty.uri, model.RDFProperty.id,
            func.sum(model.RDFPropertyStat.count), func.count(model.StatResult.id)).join(model.RDFPropertyStat).join(model.StatResult).filter(
            model.StatResult.current_of!=None).group_by(model.RDFProperty.uri, model.RDFProperty.id)
        c.query_string = '?'
        # optional search
        c.search = ''
        if request.GET.has_key('search'):
            rdf_properties = rdf_properties.filter(model.RDFProperty.uri.ilike("%%%s%%" % request.GET['search']))
            c.query_string += 'search=%s&' % request.GET['search']
            c.search = request.GET['search']
        # json
        if format=='json' or 'application/json' in request.headers.get('accept', ''):
            response.content_type = 'application/json'
            json_rdf_properties = []
            for p in rdf_properties:
                json_rdf_properties.append({'uri': p.uri, 'overall_sum': int(p[1]), 'datasets': int(p[2])})
            return json.dumps(json_rdf_properties)
        # sort results
        c.sort_order = request.GET.get('sort')
        if request.GET.has_key('sort'):
            if request.GET['sort'] == 'uri':
                c.rdf_properties = rdf_properties.order_by(model.RDFProperty.uri)
            elif request.GET['sort'] == 'overall':
                c.rdf_properties = rdf_properties.order_by(desc(func.sum(model.RDFPropertyStat.count)),
                                desc(func.count(model.StatResult.id)), model.RDFProperty.uri)
            elif request.GET['sort'] == 'datasets':
                c.rdf_properties = rdf_properties.order_by(desc(func.count(model.StatResult.id)),
                                desc(func.sum(model.RDFPropertyStat.count)), model.RDFProperty.uri)
            else:
                c.rdf_properties = rdf_properties.order_by(desc(func.count(model.StatResult.id)),
                                desc(func.sum(model.RDFPropertyStat.count)), model.RDFProperty.uri)
        else:
            c.rdf_properties = rdf_properties.order_by(desc(func.count(model.StatResult.id)),
                            desc(func.sum(model.RDFPropertyStat.count)), model.RDFProperty.uri)
        if request.GET.has_key('page'):
            page = request.GET['page']
        else:
            page = 1
        page_url = PageURL_WebOb(request)
        c.rdf_properties_page = Page(c.rdf_properties, page=page, items_per_page=50, url=page_url)
        c.count = c.rdf_properties_page.item_count
        return render('/properties/index.html')

    def create(self):
        """POST /properties: Create a new item"""
        # url('properties')

    def new(self, format='html'):
        """GET /properties/new: Form to create a new item"""
        # url('new_property')

    def update(self, id):
        """PUT /properties/id: Update an existing item"""
        # Forms posted to this method should contain a hidden field:
        #    <input type="hidden" name="_method" value="PUT" />
        # Or using helpers:
        #    h.form(url('property', id=ID),
        #           method='put')
        # url('property', id=ID)

    def delete(self, id):
        """DELETE /properties/id: Delete an existing item"""
        # Forms posted to this method should contain a hidden field:
        #    <input type="hidden" name="_method" value="DELETE" />
        # Or using helpers:
        #    h.form(url('property', id=ID),
        #           method='delete')
        # url('property', id=ID)

    def show(self, id, format='html'):
        """GET /properties/id: Show a specific item"""
        # url('property', id=ID)
        if id is None:
            abort(404)
        c.prop = Session.query(model.RDFProperty).get(int(id))
        if c.prop is None:
            abort(404)
        ps=Session.query(model.RDFPropertyStat).join(model.StatResult, model.StatResult.current_of).filter(
            and_(
                model.RDFPropertyStat.rdf_property==c.prop,
                model.StatResult.current_of!=None)).order_by(model.RDFDoc.name).all()
        c.ps = ps
        c.count = len(ps)
        return render('/properties/view.html')

    def edit(self, id, format='html'):
        """GET /properties/id/edit: Form to edit an existing item"""
        # url('edit_property', id=ID)
