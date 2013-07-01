import cgi

from paste.urlparser import PkgResourcesParser
from webhelpers.html.builder import literal
from pylons import tmpl_context as c

from rdfstats.lib.base import BaseController, render

class ErrorController(BaseController):
    """Generates error documents as and when they are required.

    The ErrorDocuments middleware forwards to ErrorController when error
    related status codes are returned from the application.

    This behaviour can be altered by changing the parameters to the
    ErrorDocuments middleware in your config/middleware.py file.

    """
    def document(self):
        """Render the error document"""
        request = self._py_object.request
        resp = request.environ.get('pylons.original_response')
        content = literal(resp.status) or cgi.escape(request.GET.get('message', ''))
        c.prefix = request.environ.get('SCRIPT_NAME', '')
        c.code = cgi.escape(request.GET.get('code', str(resp.status_int)))
        c.message = content
        return render('/error.html')

    def img(self, id):
        """Serve Pylons' stock images"""
        return self._serve_file('/'.join(['media/img', id]))

    def style(self, id):
        """Serve Pylons' stock stylesheets"""
        return self._serve_file('/'.join(['media/style', id]))

    def _serve_file(self, path):
        """Call Paste's FileApp (a WSGI application) to serve the file
        at the specified path
        """
        request = self._py_object.request
        request.environ['PATH_INFO'] = '/%s' % path
        return PkgResourcesParser('pylons', 'pylons')(request.environ, self.start_response)
