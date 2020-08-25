import sys
import io
from http_response import HttpResponse

# WSGI class
# Adapter between serve and WSGI web app

class WSGI:
    __config = {
            'wsgi.version' : (1,0),
            'wsgi.multithread' : False,
            'wsgi.multiprocess': False,
            'wsgi.run_once' : False,
            'wsgi.error' : sys.stderr,
            }
 
    def __init__ (self, application, config = None):
        if config is not None:
            self.__config.update(config)
        self.__application = application
        
    def process (self, http_request) -> HttpResponse:
        env = http_request.get_cgi_config()

        env.update({**self.__config, 'wsgi.input': io.StringIO(http_request.get_body())})

        headers = []
        def start_response (status, response_headers, exc_info = None):
            nonlocal headers
            headers = [status, response_headers]

        result = self.__application(env, start_response)

        status, response_headers = headers

        return HttpResponse(status, response_headers, result, env)

