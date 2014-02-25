import tornado.ioloop
from tornado.web import RequestHandler, Application
from tornado.httpclient import AsyncHTTPClient, HTTPRequest
from tornado.httpserver import HTTPServer

class HTTPHandler(RequestHandler):
    #This decorator does not make a method asynchronous; it tells the framework that the method is asynchronous.     #If this decorator is given, the response is not finished when the method returns. It is up to the request handler to call self.finish() to finish the HTTP request.)
    @tornado.web.asynchronous
    def get(self):
#        print self.request.arguments
#        print self.request.body
#        print self.request.body_arguments
#        print self.request.connection
#        print self.request.headers#header
#        print self.request.method#GET/POST
#        print self.request.path#/
#        print self.request.protocol#http
#        print self.request.remote_ip#127.0.0.1
#        print self.request.uri#/
#        print self.request.host#127.0.0.1:8888
        print self.request.host, self.request.method

        def handle_request(response):
            if response.error and not isinstance(response.error, tornado.httpclient.HTTPError):
                print "Error:", response.error
            else:
                #self.set_status(response.code)#200 and so on
                self.write(response.body)
            self.finish(" ")#in case of response.body == None(may be)
            #Finishes this response, ending the HTTP request.
            #This is used with @tornado.web.asynchronous

        request = self.request
        req = HTTPRequest(url=request.uri, method=request.method, 
                          headers=request.headers, body=request.body,
                          allow_nonstandard_methods = True, follow_redirects = False,)
#                          validate_cert=False)
                          #proxy_host = "ami_GS_Proxy") #this is not supported
        http_client = AsyncHTTPClient()
        try:
            http_client.fetch(req, handle_request)
        except tornado.httpclient.HTTPError as e:
            print "AMIAMIAMIAMIAMIAMIA", e


    @tornado.web.asynchronous    
    def post(self):
        return self.get()
    @tornado.web.asynchronous    
    def head(self):
        return self.get()#same as GET, but it returns only HTTP header
    @tornado.web.asynchronous    
    def delete(self):
        return self.get()#delete file located in  server by specifing URI
    @tornado.web.asynchronous    
    def patch(self):
        return self.get()#same as put, but it changes only difference 
    @tornado.web.asynchronous    
    def put(self):
        return self.get()#replace file located in server by specifing URI
    @tornado.web.asynchronous    
    def options(self):
        return self.get()#notification of trasfer option

    @tornado.web.asynchronous
    def connect(self):
        print self.request.uri.split(":"), "-------connect--------"        
        """
        host, port = self.request.uri.split(':')
        client = self.request.connection.stream

        def read_from_client(data):
            upstream.write(data)

        def read_from_upstream(data):
            client.write(data)

        def client_close(data=None):
            if upstream.closed():
                return
            if data:
                upstream.write(data)
            upstream.close()

        def upstream_close(data=None):
            if client.closed():
                return
            if data:
                client.write(data)
            client.close()

        def start_tunnel():
            client.read_until_close(client_close, read_from_client)
            upstream.read_until_close(upstream_close, read_from_upstream)
            client.write(b'HTTP/1.0 200 Connection established\r\n\r\n')

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        upstream = tornado.iostream.IOStream(s)
        upstream.connect((host, int(port)), start_tunnel)
        """


class HTTPSHandler(RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        print self.request.host, self.request.method
        print "aaa"
        def handle_request(response):
            if response.error and not isinstance(response.error, tornado.httpclient.HTTPError):
                print "Error:", response.error
            else:
                #self.set_status(response.code)#200 and so on
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
#        except tornado.httpclient.HTTPError as e:
#            print "AMIAMIAMIAMIAMIAMIA", e


    @tornado.web.asynchronous    
    def post(self):
        return self.get()
    @tornado.web.asynchronous    
    def head(self):
        return self.get()#same as GET, but it returns only HTTP header
    @tornado.web.asynchronous    
    def delete(self):
        return self.get()#delete file located in  server by specifing URI
    @tornado.web.asynchronous    
    def patch(self):
        return self.get()#same as put, but it changes only difference 
    @tornado.web.asynchronous    
    def put(self):
        return self.get()#replace file located in server by specifing URI
    @tornado.web.asynchronous    
    def options(self):
        return self.get()#notification of trasfer option
    @tornado.web.asynchronous
    def connect(self):
        print self.request.uri.split(":"), "-------connect--------"        



if __name__ == "__main__":
    
    app1 = Application([
        (r"http:.*", HTTPHandler),
    ])

    app2 = Application([
            (r"https:.*", HTTPSHandler),
            ])
    
    httpServer = HTTPServer(app1)
    httpsServer = HTTPServer(app2, ssl_options = {
            "certfile": "./server.crt",
            "keyfile": "./server.key",
            })

    app1.listen(8888)
    app2.listen(444)

    tornado.ioloop.IOLoop.instance().start()
