import email


class HttpResponse:
    # Constructor
    # Parameters:
    # status: 
    #
    # response_headers
    #
    # response_body: 
    # 
    # env 
    def __init__ (self, status, response_headers, response_body, env):
        self.__status = status
        self.__response_headers = response_headers
        self.__response_body = response_body
        self.__server_headers = [
                ('Date', email.utils.formatdate(usegmt = True)),
                ('Server', env['SERVER_NAME'])
                ]

    def get_response (self):
        status_line = f'HTTP/1.1 {self.__status}\r\n'
        header_line = ''
        for header in self.__server_headers + self.__response_headers:
            header_line += '{0}: {1}\r\n'.format(*header)

        body = ''
        for data in self.__response_body:
            body += data.decode('utf-8')

        response = status_line + header_line + '\r\n' + body

        return response
