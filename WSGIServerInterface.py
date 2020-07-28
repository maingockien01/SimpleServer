import io
import socket
import sys
import zope.interface

class WSGIServerInterface(zope.interface.Interface):

    enc, esc = sys.getfilesystemencoding(), 'surrogateescape'

    def start_response (self, status, response_headers, exc_info = None):
        pass

    def write (data):
        pass

    def send_status(status):
        pass

    def send_headers (headers):
        pass

    def unicode_to_wsgi (u):
        # Convert an environment variable to WSGI "bytes as unicode" string
        return u.encode(enc, esc).decode('iso-8859-1')

    def wsgi_to_bytes (s):
        return s.encode('iso-8859-1')

    def get_environment ():
        environ = {k: unicode_to_wsgi(v) for k,v in os.environ.items()}

        # WSGI environ
        environ['wsgi.input'] = 
        environ['wsgi.errors'] = 
        environ['wsgi.version'] = (1,0)
        environ['wsgi.multithread'] = False
        environ['wsgi.multiprocess'] = False
        environ['wsgi.run_once'] = False

        if environ.get('HTTPS', 'off') in ('on', '1'):
            environ['wsgi.url_scheme'] = 'https'
        else: 
            environ['wsgi.url_scheme'] = 'http'

        # CGI environ
        environ['REQUEST_METHOD'] = 
        environ['SERVER_NAME'] = 
        environ['SERVER_PORT']
        environ['PATH_INFO'] = 


