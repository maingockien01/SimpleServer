from server import Server
from gateway import WSGI
import sys

#Runnable script for webser

SERVER_ADDRESS = (HOST, PORT) = '', 8888

def make_server (server_address, application):
    gateway = WSGI(application)
    server = Server (server_address, gateway)

    return server

if __name__ == '__main__':
    print('start')
    if len(sys.argv) < 2:
        sys.exit('Invalide format: module:callable')
    app_path = sys.argv[1]
    module, application = app_path.split(':')
    module = __import__(module)
    application = getattr(module, application)
    httpd = make_server(SERVER_ADDRESS, application)
    print(f'WSGIServer: Serving HTTP on port {PORT} ...\n')
    httpd.run()

