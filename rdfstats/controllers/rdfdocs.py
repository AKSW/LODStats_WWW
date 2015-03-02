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
import tempfile
import zipfile

from pylons import request, response, session, tmpl_context as c, url, config
from pylons.controllers.util import abort, redirect

from rdfstats.lib.base import BaseController, render, Session

from rdfstats import model

from pylons.decorators.rest import restrict

from sqlalchemy import func, and_, or_, desc

from webhelpers.paginate import Page, PageURL_WebOb

log = logging.getLogger(__name__)

class RdfdocsController(BaseController):
    """REST Controller styled on the Atom Publishing Protocol"""
    # To properly map this controller, ensure your config/routing.py
    # file has a resource setup:
    #     map.resource('rdfdoc', 'rdfdocs')

    def index(self, format='html'):
        """GET /rdfdocs: All items in the collection"""
        # url('rdfdocs')
        rdfdocs = Session.query(model.RDFDoc).filter(model.RDFDoc.active==True).join(model.RDFDoc.current_stats)
        c.query_string = '?'
        c.search = ''
        if request.GET.has_key('search'):
            rdfdocs = rdfdocs.filter(model.RDFDoc.name.ilike("%%%s%%" % request.GET['search']))
            c.query_string += 'search=%s&' % request.GET['search']
            c.search = request.GET['search']
        if request.GET.has_key('errors'):
            rdfdocs = rdfdocs.filter(model.StatResult.errors!=None)
            c.query_string += 'errors=1&'
        if request.GET.has_key('valid'):
            rdfdocs = rdfdocs.filter(model.StatResult.errors==None)
            c.query_string += 'valid=1&'
        if request.GET.has_key('sparql'):
            rdfdocs = rdfdocs.filter(model.RDFDoc.format=='sparql')
            c.query_string += 'sparql=1&'
        if request.GET.has_key('dumps'):
            rdfdocs = rdfdocs.filter(model.RDFDoc.format!='sparql')
            c.query_string += 'dumps=1&'
        c.sort_order = request.GET.get('sort')
        if request.GET.has_key('sort'):
            if request.GET['sort'] == 'triples':
                c.rdfdocs = rdfdocs.order_by(desc(func.coalesce(model.StatResult.triples, '0')))
            elif request.GET['sort'] == 'warnings':
                c.rdfdocs = rdfdocs.order_by(desc(func.coalesce(model.StatResult.warnings, '0')))
            elif request.GET['sort'] == 'format':
                c.rdfdocs = rdfdocs.order_by(func.coalesce(model.RDFDoc.format, '0'))
            elif request.GET['sort'] == 'issue':
                c.rdfdocs = rdfdocs.order_by(model.StatResult.errors)
            elif request.GET['sort'] == 'update':
                c.rdfdocs = rdfdocs.order_by(model.RDFDoc.last_updated.desc())
            else:
                c.rdfdocs = rdfdocs.order_by(model.RDFDoc.worked_on.desc(), model.RDFDoc.name, model.RDFDoc.last_updated.desc())
        else:
            c.rdfdocs = rdfdocs.order_by(model.RDFDoc.worked_on.desc(), model.RDFDoc.name, model.RDFDoc.last_updated.desc())
        if request.GET.has_key('page'):
            page = request.GET['page']
        else:
            page = 1
        page_url = PageURL_WebOb(request)
        c.rdfdocs_page = Page(c.rdfdocs, page=page, items_per_page=50, url=page_url)
        c.rdfdoc_count = c.rdfdocs.count()
        c.workers = Session.query(model.WorkerProc).order_by(model.WorkerProc.started.desc()).all()
        if format=='json' or 'application/json' in request.headers.get('accept', ''):
            response.content_type = 'application/json'
            json_rdfdocs = []
            for r in rdfdocs:
                json_rdfdocs.append(r.name)
            return json.dumps(json_rdfdocs)
        return render('/rdfdoc/index.html')

    def valid_and_available(self):
        c.rdfdocs = Session.query(model.RDFDoc).filter(model.RDFDoc.active==True).join(model.RDFDoc.current_stats).filter(and_(model.StatResult.triples > 0, model.RDFDoc.format != 'sparql')).all()
        response.content_type = 'text/plain'
        return render('/rdfdoc/txtlist.txt')

    def void(self):
        """send VoID of every dataset in a ZIP file"""
        rdfdocs = Session.query(model.RDFDoc).filter(model.RDFDoc.active==True).join(model.RDFDoc.current_stats).filter(and_(model.StatResult.triples > 0, model.RDFDoc.format != 'sparql'))
        zip_temp_file = tempfile.NamedTemporaryFile(prefix='lodstatswww_voidzip')
        zip_temp = zipfile.ZipFile(zip_temp_file, 'w', zipfile.ZIP_DEFLATED)
        for r in rdfdocs:
            zip_temp.writestr("%s.ttl" % r.name, r.current_stats.void)
        zip_temp.close()
        zip_temp_file.seek(0)
        response.content_type = 'application/zip'
        response.headers['Content-Disposition'] = "filename=LODStats_all_void.zip"
        # FIXME: use paste.fileapp if this ever gets too large
        for data in zip_temp_file:
            response.write(data)

    def show(self, id=None, format='html'):
        if id is None:
            abort(404)
        try:
            c.rdfdoc = Session.query(model.RDFDoc).get(int(id))
        except ValueError, e:
            c.rdfdoc = Session.query(model.RDFDoc).filter(model.RDFDoc.name==id).first()
        if c.rdfdoc is None:
            abort(404)
        c.oldstats = Session.query(model.StatResult).filter(
                                    and_(
                                        model.StatResult.rdfdoc==c.rdfdoc,
                                        model.StatResult.current_of==None)
                                    ).order_by(desc(model.StatResult.last_updated)).all()
        if(c.rdfdoc.ckan_catalog=="datahubio"):
            c.ckan_base = config['ckan.base']
        elif(c.rdfdoc.ckan_catalog=="datagov"):
            c.ckan_base = "http://catalog.data.gov/"
        elif(c.rdfdoc.ckan_catalog=="pdeu"):
            c.ckan_base = "http://publicdata.eu/"
        if format=='json' or 'application/json' in request.headers.get('accept', ''):
            response.content_type = 'application/json'
            json_rdfdoc = {}
            json_rdfdoc['name'] = c.rdfdoc.name
            json_rdfdoc['resource_uri'] = c.rdfdoc.uri
            json_rdfdoc['source'] = "http://stats.lod2.eu/rdfdocs/%s" % c.rdfdoc.name
            json_rdfdoc['quality_score'] = 3
            json_rdfdoc['quality_details'] = 3
            json_rdfdoc['category'] = 'lod2-stats'
            json_rdfdoc['format'] = c.rdfdoc.format
            if c.rdfdoc.current_stats is not None:
                json_rdfdoc['statistics'] = c.rdfdoc.current_stats.json_dict()
            else:
                json_rdfdoc['statistics'] = None
            return json.dumps(json_rdfdoc)
        return render('/rdfdoc/view.html')

    def new(self):
        """GET /rdfdocs/new: Form to create a new item"""
        # url('new_rdfdoc')
        abort(403)
        c.rdfdoc_f = model.RDFDoc_fa
        c.rdfdoc_f.configure(include=[c.rdfdoc_f.uri, c.rdfdoc_f.name, c.rdfdoc_f.format])
        return render('/rdfdoc/new.html')

    @restrict('POST')
    def create(self):
        """POST /rdfdocs: Create a new item"""
        # url('rdfdocs')
        abort(403)
        rdfdoc_f = model.RDFDoc_fa.bind(data=request.POST)
        rdfdoc_f.configure(include=[rdfdoc_f.uri, rdfdoc_f.name, rdfdoc_f.format])
        if rdfdoc_f.validate():
            rdfdoc_f.sync()
            Session.add(rdfdoc_f.model)
            Session.commit()
            redirect(url('rdfdoc', id=rdfdoc_f.model.id))
        else:
            c.rdfdoc_f = rdfdoc_f
            return render('/rdfdoc/new.html')

    def update(self, id):
        """PUT /rdfdocs/id: Update an existing item"""
        # Forms posted to this method should contain a hidden field:
        #    <input type="hidden" name="_method" value="PUT" />
        # Or using helpers:
        #    h.form(url('rdfdoc', id=ID),
        #           method='put')
        # url('rdfdoc', id=ID)

    def edit(self, id=None):
        """GET /rdfdocs/id/edit: Form to edit an existing item"""
        # url('edit_rdfdoc', id=ID)
        abort(403)
        if id is None:
            abort(404)
        rdfdoc_q = Session.query(model.RDFDoc)
        c.rdfdoc = rdfdoc_q.get(int(id))
        if c.rdfdoc is None:
            abort(404)
        c.rdfdoc_f = model.RDFDoc_fa.bind(c.rdfdoc)
        return render('/rdfdoc/edit.html')

    def delete(self, id):
        """DELETE /rdfdocs/id: Delete an existing item"""
        # Forms posted to this method should contain a hidden field:
        #    <input type="hidden" name="_method" value="DELETE" />
        # Or using helpers:
        #    h.form(url('rdfdoc', id=ID),
        #           method='delete')
        # url('rdfdoc', id=ID)
