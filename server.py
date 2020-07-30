import socket
import sys
import io
from http_request import HttpRequest
import email

class Server (object):

    def __init__ (self, server_address, gateway):
        self.__config  = {
            'address_family' : socket.AF_INET,
            'socket_type' : socket.SOCK_STREAM,
            'buff_size' : 1024,
            'request_queue_size' : 1,
           }

        self.enc, self.esc = sys.getfilesystemencoding(), 'surrogateescape'

        self.__gateway = gateway

       
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
        self.__config.update(config_set)

    def create_socket (self, server_address):
        listen_socket = socket.socket(self.__config['address_family'], self.__config['socket_type'])
        listen_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR, 1)

        listen_socket.bind(server_address)
        listen_socket.listen(self.__config['request_queue_size'])

        return listen_socket

    def run (self):
        #TODO: find the efficient way to listen for connections

        while True:
            client_connection, client_address = self.listen_socket.accept()
            print('Connection is accepted')

            request_data = client_connection.recv(self.__config['buff_size'])
            print('Data is recevied')

            httpRequest = HttpRequest(request_data, self.__config)

            self.handle_request(httpRequest, client_connection)
            print('Request is handled')

            client_connection.close()
            print('Connection is closed')

    def handle_request (self,http_request, client_connection):
       http_response = self.__gateway.process(http_request)
       print('Response is created')

       self.write(http_response.get_response().encode(), client_connection)
       print('Response is sent')

    def write (self, data, client_connection):
        if not client_connection:
            print('Unable to send data due to unvalid client connection!')
        else:
            client_connection.send(data)

    def unicode_to_wsgi (self, u):

        return u.endcode(enc, esc).decode('iso-8859-1')

    def wsgi_to_bytes (self, s):

        return s.encode('iso-8859-1')


