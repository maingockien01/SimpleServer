import io
try:
    from http_parser.parser import HttpParser
except:
    from http_parser.pyparser import HttpParser

class HttpRequest(object):
    __cgi_config = None
    def __init__ (self, request_text, server_config):
        self.__parser = HttpParser()
        self.__parser.execute(request_text, len(request_text))
        self.__server_config = server_config

    def get_body (self):
        if self.__parser.is_partial_body():
            return self.__parser.recv_body()
        return None

    def get_headers (self):
        return self.__parser.get_headers()

    def get_request_method (self):
        return self.__parser.get_method()

    def get_request_path (self):
        return self.__parser.get_path()

    def get_cgi_config (self):
        if self.__cgi_config is None:
            __cgi_config = {}
            #WSGI required variable
            #__cgi_config['wsgi.input'] = io.StringIO(self.get_body())

            #CGI
            __cgi_config['SERVER_NAME'] = self.__server_config['server_name']
            __cgi_config['SERVER_PORT'] = self.__server_config['server_port']
            __cgi_config['SERVER_PROTOCOL'] : 'HTTP/1.1'
            __cgi_config['REQUEST_METHOD'] = self.get_request_method()
            __cgi_config['PATH_INFO'] = self.get_request_path()

            for header, value in self.get_headers().items():
                __cgi_config[f'HTTP_{header}'] = value
            
            self.__cgi_config = __cgi_config
        return self.__cgi_config
