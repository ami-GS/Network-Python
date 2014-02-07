from twisted.web import http, proxy
from twisted.internet import reactor, ssl
from twisted.python import log
import sys

#log.startLogging(sys.stdout)

class LoggingProxyRequest(proxy.ProxyRequest):
    def process(self):
        print "Request from %s for %s" % (self.getClientIP(), self.getAllHeaders()['host'])
        try:
            proxy.ProxyRequest.process(self)
        except KeyError:
            print "HTTPS is not supported at the moment!"

class LoggingProxy(proxy.Proxy):
    requestFactory = LoggingProxyRequest

class LoggingProxyFactory(http.HTTPFactory):
    def buildProtocol(self, addr):
        return LoggingProxy()

reactor.listenTCP(8080, LoggingProxyFactory())
reactor.run()
