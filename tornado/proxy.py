import tornado.ioloop
from tornado.web import RequestHandler, Application
from tornado.httpclient import AsyncHTTPClient, HTTPRequest
from tornado.httpserver import HTTPServer
import os, sys
import socket
import ssl


class HTTPSHandler(RequestHandler):
    SUPPORTED_METHODS = ("GET", "HEAD", "POST", "DELETE", "PATCH", "PUT", "OPTIONS", "CONNECT")
    
    @tornado.web.asynchronous
    def handler(self):
        print self.request.supports_http_1_1()
        print self.request.host, self.request.method
        def handle_request(response):
            if response.error:
                self.set_status(500)
                self.write("Internal server error")
                print "Error:", response.error
            else:
                self.set_status(response.code)#200 and so on
                self.write(response.body)
            self.finish(" ")#in case of response.body == None(may be)

        request = self.request
        req = HTTPRequest(url=request.uri, method=request.method, 
                          headers=request.headers, body=request.body,
                          allow_nonstandard_methods = True, follow_redirects = False,
                          validate_cert=True)

        http_client = AsyncHTTPClient()
        try:
            http_client.fetch(req, handle_request)
        except Exception as e:
            print e

    @tornado.web.asynchronous
    def get(self):
        return self.handler()
    @tornado.web.asynchronous    
    def post(self):
        return self.handler()
    @tornado.web.asynchronous    
    def head(self):
        return self.handler()#same as GET, but it returns only HTTP header
    @tornado.web.asynchronous    
    def delete(self):
        return self.handler()#delete file located in  server by specifing URI
    @tornado.web.asynchronous    
    def patch(self):
        return self.handler()#same as put, but it changes only difference 
    @tornado.web.asynchronous    
    def put(self):
        return self.handler()#replace file located in server by specifing URI
    @tornado.web.asynchronous    
    def options(self):
        return self.handler()#notification of trasfer option
    @tornado.web.asynchronous
    def connect(self):
        host, port = self.request.uri.split(':')
        client = self.request.connection.stream#tornado.iostream.IOStream
        def read_from_client(data):
            upstream.write(data)
            #write the given daga to this stream

        def read_from_upstream(data):
            client.write(data)

        def client_close(data=None):
            if upstream.closed():
                return
            if data:
                upstream.write(data)
            upstream.close()
            #Close this stream

        def upstream_close(data=None):
            if client.closed():
                return
            if data:
                client.write(data)
            client.close()

        def start_tunnel():
            #Reads all data from the socket until it is closed
            upstream.read_until_close(upstream_close, client.write)#upstream -> client
            client.read_until_close(client_close, upstream.write)#client -> upstream
            if self.request.supports_http_1_1():
                client.write(b'HTTP/1.1 200 Connection established\r\n\r\n')
            else:
                client.write(b'HTTP/1.0 200 Connection established\r\n\r\n')

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)#make CONNECT client
        upstream = tornado.iostream.IOStream(s)
        """
        ssl.wrap_socket(s, do_handshake_on_connect = False)
        upstream = tornado.iostream.SSLIOStream(s,  ssl_options = {
            "certfile": os.path.join(os.getcwd(), "server.crt"),
            "keyfile": os.path.join(os.getcwd(), "server.key"),})
        """
        #Connect the socket to a remote address without blocking
        #callback is called when connection is completed
        upstream.connect((host, int(port)), start_tunnel)
        

if __name__ == "__main__":
    app = Application([
        (r".*", HTTPSHandler),
            ])
    
    proxyServer = HTTPServer(app, ssl_options = {
            "certfile": os.path.join(os.getcwd(), "server.crt"),
            "keyfile": os.path.join(os.getcwd(), "server.key"),
            })

    proxyServer.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
