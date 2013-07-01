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

class LinksController(BaseController):
    """REST Controller styled on the Atom Publishing Protocol"""
    # To properly map this controller, ensure your config/routing.py
    # file has a resource setup:
    #     map.resource('link', 'links')

    def index(self, format='html'):
        """GET /links: All items in the collection"""
        # url('links')
        links = Session.query(model.Link.code, model.Link.id, func.sum(model.LinkStat.count),
                                    func.count(model.StatResult.id))\
                                .join(model.LinkStat).join(model.StatResult)\
                                .filter(model.StatResult.current_of!=None)\
                                .group_by(model.Link.code, model.Link.id)
        c.query_string = '?'
        # optional search
        c.search = ''
        if request.GET.has_key('search'):
            links = links.filter(model.Link.code.ilike("%%%s%%" % request.GET['search']))
            c.query_string += 'search=%s&' % request.GET['search']
            c.search = request.GET['search']
        # sort results
        c.sort_order = request.GET.get('sort')
        if request.GET.has_key('sort'):
            if request.GET['sort'] == 'uri':
                c.links = links.order_by(model.Link.code)
            elif request.GET['sort'] == 'overall':
                c.links = links.order_by(desc(func.sum(model.LinkStat.count)),
                                desc(func.count(model.StatResult.id)), model.Link.code)
            elif request.GET['sort'] == 'datasets':
                c.links = links.order_by(desc(func.count(model.StatResult.id)),
                                desc(func.sum(model.LinkStat.count)), model.Link.code)
            else:
                c.links = links.order_by(desc(func.count(model.StatResult.id)),
                                desc(func.sum(model.LinkStat.count)), model.Link.code)
        else:
            c.links = links.order_by(desc(func.count(model.StatResult.id)),
                            desc(func.sum(model.LinkStat.count)), model.Link.code)
        if request.GET.has_key('page'):
            page = request.GET['page']
        else:
            page = 1
        page_url = PageURL_WebOb(request)
        c.links_page = Page(c.links, page=page, items_per_page=50, url=page_url)
        c.count = c.links_page.item_count
        return render('/links/index.html')

    def create(self):
        """POST /links: Create a new item"""
        # url('links')

    def new(self, format='html'):
        """GET /links/new: Form to create a new item"""
        # url('new_link')

    def update(self, id):
        """PUT /links/id: Update an existing item"""
        # Forms posted to this method should contain a hidden field:
        #    <input type="hidden" name="_method" value="PUT" />
        # Or using helpers:
        #    h.form(url('link', id=ID),
        #           method='put')
        # url('link', id=ID)

    def delete(self, id):
        """DELETE /links/id: Delete an existing item"""
        # Forms posted to this method should contain a hidden field:
        #    <input type="hidden" name="_method" value="DELETE" />
        # Or using helpers:
        #    h.form(url('link', id=ID),
        #           method='delete')
        # url('link', id=ID)

    def show(self, id, format='html'):
        """GET /links/id: Show a specific item"""
        # url('link', id=ID)
        if id is None:
            abort(404)
        try:
            c.link = Session.query(model.Link).get(int(id))
        except ValueError, e:
            abort(404)
        if c.link is None:
            abort(404)
        c.ls=Session.query(model.LinkStat).join(model.StatResult, model.StatResult.current_of).filter(
            and_(
                model.LinkStat.link==c.link,
                model.StatResult.current_of!=None)).order_by(model.RDFDoc.name).all()
        c.count = len(c.ls)
        return render('/links/view.html')

    def edit(self, id, format='html'):
        """GET /links/id/edit: Form to edit an existing item"""
        # url('edit_link', id=ID)
