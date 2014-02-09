from twisted.web.server import Site, NOT_DONE_YET
from twisted.web.resource import Resource
from twisted.internet import reactor
from twisted.python import log


class Serve(Resource):
    isLeaf = True
    
    def render(self, request):
        if request.method == "POST":
            self.headers == request.getAllHeaders()
            return "HELLO"

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
            if request.uri == "/hoge":
                request.write("<strong>hoge!</strong>")
            request.write("</body>\n")
            request.write("</html>\n")
            request.finish()#send data to browser  
        return NOT_DONE_YET


import sys
log.startLogging(sys.stdout)

server = Serve()
server.putChild("", server)
site = Site(server)

reactor.listenTCP(8008, site)
reactor.run()
