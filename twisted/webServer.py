from twisted.web.server import Site, NOT_DONE_YET
from twisted.web.resource import Resource
from twisted.internet import reactor
from twisted.python import log
import settings

class Serve(Resource):
    isLeaf = True #if True, the render will be called and children are called based on requested name

    def getChile(self, name, request):
        if name == "":
            return self
        print name, request
        return Resource.getChild(self, name, request)
    
    def render(self, request):
        print request.prepath
        print request.postpath
        print request.method
        if request.method == "POST":
            self.headers = request.getAllHeaders()
            return "POST"

        elif request.method == "GET":
            msg = """
            <!DOCTYPE html>
            <html>
            <head>
            <meta name=\"description\" content=\"\">
            </head>
            <body>
            <h1>HELLO TWISTED</h1>
            <form method = "get">
            <p> RADIO: <input type="radio" name="ra", value="rad1", checked="checked" /> ra1
            <input type="radio" name="ra", value="rad2" /> ra2 </p>
            <p><input type="submit" name="submit" value="GET!"></form>

            <form method = "post">
            <p> RADIO: <input type="radio" name="ra", value="rad1", checked="checked" /> ra1
            <input type="radio" name="ra", value="rad2" /> ra2 </p>
            <p><input type="submit" name="submit" value="POST!"></form>
            </body>
            </html>
            """
            request.write(msg)
            request.finish()#send data to browser  
        return NOT_DONE_YET

class hoge():
    isLeaf = True
    def render(self, request):
        return "hoge"

class fuga():
    isLeaf = True
    def render(self, request):
        return "fuga"



import sys
log.startLogging(sys.stdout)

server = Serve()
#server.putChild("", server)
server.putChild("hoge", hoge())
server.putChild("fuga", fuga())
site = Site(server)

reactor.listenTCP(settings.port, site)
reactor.run()
