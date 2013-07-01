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

from sqlalchemy import and_, func, desc

from webhelpers.paginate import Page, PageURL_WebOb

log = logging.getLogger(__name__)

class DatatypesController(BaseController):
    """REST Controller styled on the Atom Publishing Protocol"""
    # To properly map this controller, ensure your config/routing.py
    # file has a resource setup:
    #     map.resource('datatype', 'datatypes')

    def index(self, format='html'):
        """GET /datatypes: All items in the collection"""
        # url('datatypes')
        # datatypes = Session.query(model.RDFDatatype).join(model.RDFDatatypeStat).join(model.StatResult).filter(
        #     model.StatResult.current_of!=None)
        
        datatypes = Session.query(model.RDFDatatype.uri, model.RDFDatatype.id,
                                    func.sum(model.RDFDatatypeStat.count),
                                    func.count(model.StatResult.id))\
                                    .join(model.RDFDatatypeStat).join(model.StatResult)\
                                    .filter(model.StatResult.current_of!=None)\
                                    .group_by(model.RDFDatatype.uri, model.RDFDatatype.id)
        c.query_string = '?'
        # optional search
        c.search = ''
        if request.GET.has_key('search'):
            datatypes = datatypes.filter(model.RDFDatatype.uri.ilike("%%%s%%" % request.GET['search']))
            c.query_string += 'search=%s&' % request.GET['search']
            c.search = request.GET['search']
        # sort results
        c.sort_order = request.GET.get('sort')
        if request.GET.has_key('sort'):
            if request.GET['sort'] == 'uri':
                c.datatypes = datatypes.order_by(model.RDFDatatype.uri)
            elif request.GET['sort'] == 'overall':
                c.datatypes = datatypes.order_by(desc(func.sum(model.RDFDatatypeStat.count)),
                                desc(func.count(model.StatResult.id)), model.RDFDatatype.uri)
            elif request.GET['sort'] == 'datasets':
                c.datatypes = datatypes.order_by(desc(func.count(model.StatResult.id)),
                                desc(func.sum(model.RDFDatatypeStat.count)), model.RDFDatatype.uri)
            else:
                c.datatypes = datatypes.order_by(desc(func.count(model.StatResult.id)),
                                desc(func.sum(model.RDFDatatypeStat.count)), model.RDFDatatype.uri)
        else:
            c.datatypes = datatypes.order_by(desc(func.count(model.StatResult.id)),
                            desc(func.sum(model.RDFDatatypeStat.count)), model.RDFDatatype.uri)
        if request.GET.has_key('page'):
            page = request.GET['page']
        else:
            page = 1
        page_url = PageURL_WebOb(request)
        c.datatypes_page = Page(c.datatypes, page=page, items_per_page=50, url=page_url)
        c.count = c.datatypes_page.item_count
        return render('/datatypes/index.html')

    def create(self):
        """POST /datatypes: Create a new item"""
        # url('datatypes')

    def new(self, format='html'):
        """GET /datatypes/new: Form to create a new item"""
        # url('new_datatype')

    def update(self, id):
        """PUT /datatypes/id: Update an existing item"""
        # Forms posted to this method should contain a hidden field:
        #    <input type="hidden" name="_method" value="PUT" />
        # Or using helpers:
        #    h.form(url('datatype', id=ID),
        #           method='put')
        # url('datatype', id=ID)

    def delete(self, id):
        """DELETE /datatypes/id: Delete an existing item"""
        # Forms posted to this method should contain a hidden field:
        #    <input type="hidden" name="_method" value="DELETE" />
        # Or using helpers:
        #    h.form(url('datatype', id=ID),
        #           method='delete')
        # url('datatype', id=ID)

    def show(self, id, format='html'):
        """GET /datatypes/id: Show a specific item"""
        # url('datatype', id=ID)
        if id is None:
            abort(404)
        try:
            c.datatype = Session.query(model.RDFDatatype).get(int(id))
        except ValueError, e:
            abort(404)
        if c.datatype is None:
            abort(404)
        ds=Session.query(model.RDFDatatypeStat).join(model.StatResult, model.StatResult.current_of).filter(
            and_(
                model.RDFDatatypeStat.rdf_datatype==c.datatype,
                model.StatResult.current_of!=None)).order_by(model.RDFDoc.name).all()
        c.ds = ds
        c.count = len(ds)
        return render('/datatypes/view.html')

    def edit(self, id, format='html'):
        """GET /datatypes/id/edit: Form to edit an existing item"""
        # url('edit_datatype', id=ID)
