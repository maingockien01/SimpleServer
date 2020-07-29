import io
try:
    from http_parser.parser import HttpParser
except:
    from http_parser.pyparser import HttpParser

class HTTPRequest(object):
    def __init__ (self, request_text):
        self.parser = HttpParser()
        self.parser.execute(request_text, len(request_text))

    def get_body (self):
        if self.parser.is_partial_body():
            return self.parser.recv_body()
        return None

    def get_headers (self):
        if self.parser.is_headers_complete():
            return self.parser.get_headers()
        return None

    def get_request_method (self):
        return self.parser.get_method()

    def get_request_path (self):
        return self.parser.get_path()

    def get_env (self, server_config):
        try:
            return self.env
        except AttributeError:
            env = {}
            #WSGI required variable
            env['wsgi.version'] = server_config['wsgi_version']
            env['wsgi.input'] = io.StringIO(self.get_body())
            env['wsgi.error'] = server_config['wsgi_error']
            env['wsgi.multithread'] = server_config['wsgi_multithread']
            env['wsgi.multiprocess'] = server_config['wsgi_multiprocess']
            env['wsgi.run_once'] = server_config['wsgi_run_once']

            #CGI
            env['SERVER_NAME'] = server_config['server_name']
            env['SERVER_PORT'] = server_config['server_port']
            env['SERVER_PROTOCOL'] : 'HTTP/1.1'
            env['REQUEST_METHOD'] = self.get_request_method()
            env['PATH_INFO'] = self.get_request_path()

            for header, value in self.get_headers().items():
                env[f'HTTP_{header}'] = value
            
            self.env = env
            return env
