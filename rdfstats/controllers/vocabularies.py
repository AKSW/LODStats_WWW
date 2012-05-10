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

class VocabulariesController(BaseController):
    """REST Controller styled on the Atom Publishing Protocol"""
    # To properly map this controller, ensure your config/routing.py
    # file has a resource setup:
    #     map.resource('vocabulary', 'vocabularies')

    def index(self, format='html'):
        """GET /vocabularies: All items in the collection"""
        # url('vocabularies')
        vocabs = Session.query(model.Vocab.uri, model.Vocab.id, func.sum(model.RDFVocabStat.count),
                                func.count(model.StatResult.id))\
                                .join(model.RDFVocabStat).join(model.StatResult)\
                                .filter(model.StatResult.current_of!=None)\
                                .group_by(model.Vocab.uri, model.Vocab.id)
        c.query_string = '?'
        # optional search
        c.search = ''
        if request.GET.has_key('search'):
            vocabs = vocabs.filter(model.Vocab.uri.ilike("%%%s%%" % request.GET['search']))
            c.query_string += 'search=%s&' % request.GET['search']
            c.search = request.GET['search']
        # sort results
        c.sort_order = request.GET.get('sort')
        if request.GET.has_key('sort'):
            if request.GET['sort'] == 'uri':
                c.vocabs = vocabs.order_by(model.Vocab.uri)
            elif request.GET['sort'] == 'overall':
                c.vocabs = vocabs.order_by(desc(func.sum(model.RDFVocabStat.count)),
                                desc(func.count(model.StatResult.id)), model.Vocab.uri)
            elif request.GET['sort'] == 'datasets':
                c.vocabs = vocabs.order_by(desc(func.count(model.StatResult.id)),
                                desc(func.sum(model.RDFVocabStat.count)), model.Vocab.uri)
            else:
                c.vocabs = vocabs.order_by(desc(func.count(model.StatResult.id)),
                                desc(func.sum(model.RDFVocabStat.count)), model.Vocab.uri)
        else:
            c.vocabs = vocabs.order_by(desc(func.count(model.StatResult.id)),
                            desc(func.sum(model.RDFVocabStat.count)), model.Vocab.uri)
        if request.GET.has_key('page'):
            page = request.GET['page']
        else:
            page = 1
        page_url = PageURL_WebOb(request)
        c.vocabs_page = Page(c.vocabs, page=page, items_per_page=50, url=page_url)
        c.count = c.vocabs_page.item_count
        return render('/vocabularies/index.html')

    def create(self):
        """POST /vocabularies: Create a new item"""
        # url('vocabularies')

    def new(self, format='html'):
        """GET /vocabularies/new: Form to create a new item"""
        # url('new_vocabulary')

    def update(self, id):
        """PUT /vocabularies/id: Update an existing item"""
        # Forms posted to this method should contain a hidden field:
        #    <input type="hidden" name="_method" value="PUT" />
        # Or using helpers:
        #    h.form(url('vocabulary', id=ID),
        #           method='put')
        # url('vocabulary', id=ID)

    def delete(self, id):
        """DELETE /vocabularies/id: Delete an existing item"""
        # Forms posted to this method should contain a hidden field:
        #    <input type="hidden" name="_method" value="DELETE" />
        # Or using helpers:
        #    h.form(url('vocabulary', id=ID),
        #           method='delete')
        # url('vocabulary', id=ID)

    def show(self, id, format='html'):
        """GET /vocabularies/id: Show info and current_of-usage about Vocabulary"""
        # url('vocabulary', id=ID)
        if id is None:
            abort(404)
        c.vocab = Session.query(model.Vocab).get(int(id))
        if c.vocab is None:
            abort(404)
        vs=Session.query(model.RDFVocabStat).join(model.StatResult, model.StatResult.current_of).filter(
            and_(
                model.RDFVocabStat.vocab==c.vocab,
                model.StatResult.current_of!=None)).order_by(model.RDFDoc.name).all()
        c.vs = vs
        c.count = len(vs)
        return render('/vocabularies/view.html')

    def edit(self, id, format='html'):
        """GET /vocabularies/id/edit: Form to edit an existing item"""
        # url('edit_vocabulary', id=ID)
