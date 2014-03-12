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

class LanguagesController(BaseController):
    """REST Controller styled on the Atom Publishing Protocol"""
    # To properly map this controller, ensure your config/routing.py
    # file has a resource setup:
    #     map.resource('language', 'languages')

    def index(self, format='html'):
        """GET /languages: All items in the collection"""
        # url('languages')
        c.languages = Session.query(model.Language).join(model.LanguageStat).join(model.StatResult).filter(
            model.StatResult.current_of!=None).order_by(model.Language.code).all()
        c.count = len(c.languages)

        languages = Session.query(model.Language.code, model.Language.id, func.sum(model.LanguageStat.count),
                                    func.count(model.StatResult.id))\
                                .join(model.LanguageStat).join(model.StatResult)\
                                .filter(model.StatResult.current_of!=None)\
                                .group_by(model.Language.code, model.Language.id)
        c.query_string = '?'
        # optional search
        c.search = ''
        if request.GET.has_key('search'):
            languages = languages.filter(model.Language.code.ilike("%%%s%%" % request.GET['search']))
            c.query_string += 'search=%s&' % request.GET['search']
            c.search = request.GET['search']
        # sort results
        c.sort_order = request.GET.get('sort')
        if request.GET.has_key('sort'):
            if request.GET['sort'] == 'uri':
                c.languages = languages.order_by(model.Language.code)
            elif request.GET['sort'] == 'overall':
                c.languages = languages.order_by(desc(func.sum(model.LanguageStat.count)),
                                desc(func.count(model.StatResult.id)), model.Language.code)
            elif request.GET['sort'] == 'datasets':
                c.languages = languages.order_by(desc(func.count(model.StatResult.id)),
                                desc(func.sum(model.LanguageStat.count)), model.Language.code)
            else:
                c.languages = languages.order_by(desc(func.count(model.StatResult.id)),
                                desc(func.sum(model.LanguageStat.count)), model.Language.code)
        else:
            c.languages = languages.order_by(desc(func.count(model.StatResult.id)),
                            desc(func.sum(model.LanguageStat.count)), model.Language.code)
        if request.GET.has_key('page'):
            page = request.GET['page']
        else:
            page = 1
        page_url = PageURL_WebOb(request)
        c.languages_page = Page(c.languages, page=page, items_per_page=50, url=page_url)
        c.count = c.languages_page.item_count
        return render('/languages/index.html')

    def create(self):
        """POST /languages: Create a new item"""
        # url('languages')

    def new(self, format='html'):
        """GET /languages/new: Form to create a new item"""
        # url('new_language')

    def update(self, id):
        """PUT /languages/id: Update an existing item"""
        # Forms posted to this method should contain a hidden field:
        #    <input type="hidden" name="_method" value="PUT" />
        # Or using helpers:
        #    h.form(url('language', id=ID),
        #           method='put')
        # url('language', id=ID)

    def delete(self, id):
        """DELETE /languages/id: Delete an existing item"""
        # Forms posted to this method should contain a hidden field:
        #    <input type="hidden" name="_method" value="DELETE" />
        # Or using helpers:
        #    h.form(url('language', id=ID),
        #           method='delete')
        # url('language', id=ID)

    def show(self, id, format='html'):
        """GET /languages/id: Show a specific item"""
        # url('language', id=ID)
        if id is None:
            abort(404)
        try:
            c.language = Session.query(model.Language).get(int(id))
        except ValueError, e:
            abort(404)
        if c.language is None:
            abort(404)
        ls=Session.query(model.LanguageStat).join(model.StatResult).join(model.StatResult.current_of).filter(
            and_(
                model.LanguageStat.language==c.language,
                model.StatResult.current_of!=None)).order_by(model.RDFDoc.name).all()
        c.ls = ls
        c.count = len(ls)
        return render('/languages/view.html')

    def edit(self, id, format='html'):
        """GET /languages/id/edit: Form to edit an existing item"""
        # url('edit_language', id=ID)
