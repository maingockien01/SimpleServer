import socket
import sys
import io
from HTTPRequest import HTTPRequest
import email

class Server (object):

    def __init__ (self, server_address):
        self.config  = {
            'address_family' : socket.AF_INET,
            'socket_type' : socket.SOCK_STREAM,
            'buff_size' : 1024,
            'request_queue_size' : 1,
            'wsgi_version' : (1,0),
            'wsgi_multithread' : False,
            'wsgi_multiprocess': False,
            'wsgi_run_once' : False,
            'wsgi_error' : sys.stderr,
            }

        self.enc, self.esc = sys.getfilesystemencoding(), 'surrogateescape'

       
        self.listen_socket = self.create_socket(server_address)

        host, port = self.listen_socket.getsockname()[:2]
        server_name = socket.getfqdn(host)
        server_port = port
        config_set = {
                'server_name' : server_name,
                'server_port' : server_port,
                }
        self.config_server(config_set)

    def config_server (self, config_set):
        self.config.update(config_set)

    def create_socket (self, server_address):
        listen_socket = socket.socket(self.config['address_family'], self.config['socket_type'])
        listen_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR, 1)

        listen_socket.bind(server_address)
        listen_socket.listen(self.config['request_queue_size'])

        return listen_socket


    def set_app (self, application):
        self.application = application

    def run (self):
        #TODO: find the efficient way to listen for connections

        while True:
            client_connection, client_address = self.listen_socket.accept()
            
            request_data = client_connection.recv(self.config['buff_size'])
            print(request_data)

            httpRequest = HTTPRequest(request_data)
            env = httpRequest.get_env(self.config)

            self.handle_request(env, client_connection)
            client_connection.close()

    def handle_request (self, env, client_connection):
        headers = []

        def start_response (status, response_headers, exc_info = None):
            nonlocal headers
            headers = [status, response_headers]

        result = self.application(env, start_response)
        
        status, response_headers = headers

        server_header = [
                ('Date', email.utils.formatdate(usegmt = True)),
                ('Server', self.config['server_name'])
                ]

        def finish_response (status, server_header, response_headers, result):
            status_line = f'HTTP/1.1 {status}\r\n'
            header_line = ""
            for header in server_header + response_headers:
                header_line += '{0}: {1}\r\n'.format(*header)

            self.write(status_line.encode(), client_connection)
            self.write(header_line.encode(), client_connection)
            self.write('\r\n'.encode(), client_connection)
            
            for data in result:
                self.write(data, client_connection)

        finish_response(status, server_header, response_headers, result)
        

    def write (self, data, client_connection):
        if not client_connection:
            print('Unable to send data due to unvalid client connection!')
        else:
            client_connection.send(data)

    def unicode_to_wsgi (self, u):

        return u.endcode(enc, esc).decode('iso-8859-1')

    def wsgi_to_bytes (self, s):

        return s.encode('iso-8859-1')


SERVER_ADDRESS = (HOST, PORT) = '', 8888

def make_server (server_address, application):
    server = Server (server_address)
    server.set_app(application)

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

