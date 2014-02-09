from twisted.web.server import Site, NOT_DONE_YET
from twisted.web.resource import Resource
from twisted.internet import reactor
from twisted.python import log
import settings


class Serve(Resource):
    #isLeaf = True #if True, the render will be called

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
            request.write("<!DOCTYPE html>\n")
            request.write("<html>\n")
            request.write("<head>\n")
            request.write("<meta charset=\"utf-8\">\n")
            request.write("<title></title>\n")
            request.write("<meta name=\"description\" content=\"\">\n")
            request.write("</head>\n")
            request.write("<body>\n")
            request.write("<h1>HELLO WORLD</h1>\n")
            request.write('<form method = "get">')
            request.write('<p> RADIO: <input type="radio" name="ra", value="rad1", checked="checked" />ra1')
            request.write('<input type="radio" name="ra", value="rad2" /> ra2 </p>')
            request.write('<p><input type="submit" name="submit" value="GET!"></form>')

            request.write('<form method = "post">')
            request.write('<p> RADIO: <input type="radio" name="ra", value="rad1", checked="checked" />ra1')
            request.write('<input type="radio" name="ra", value="rad2" /> ra2 </p>')
            request.write('<p><input type="submit" name="submit" value="POST!"></form>')
            request.write("</body>\n")
            request.write("</html>\n")
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
