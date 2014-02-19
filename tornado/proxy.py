import tornado.ioloop
from tornado.web import RequestHandler, Application
from tornado.httpclient import AsyncHTTPClient, HTTPRequest

class MainHandler(RequestHandler):
    #This decorator does not make a method asynchronous; it tells the framework that the method is asynchronous. 
    #If this decorator is given, the response is not finished when the method returns. It is up to the request handler to call self.finish() to finish the HTTP request.)
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
        
        def handle_request(response):
            if response.error:
                print "Error:", response.error
            else:
                self.write(response.body)
            self.finish()
            #Finishes this response, ending the HTTP request.
            #This is used with @tornado.web.asynchronous

        request = self.request
        req = HTTPRequest(url=request.uri, method=request.method, 
                          headers=request.headers, body=request.body,
                          allow_nonstandard_methods = True,)
                          #proxy_host = "ami_GS_Proxy") #this is not supported

        http_client = AsyncHTTPClient()

        http_client.fetch(req, handle_request)
        


if __name__ == "__main__":
    
    application = Application([
        (r".*",MainHandler)
    ])

    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
