from twisted.web import http, proxy
from twisted.internet import reactor, ssl
from twisted.python import log
import sys

#log.startLogging(sys.stdout)

class LoggingProxyRequest(proxy.ProxyRequest):
    def process(self):
        print "Request from %s for %s" % (self.getClientIP(), self.getAllHeaders()['host'])
        #print "getAllHeader", self.getAllHeaders()
        #print "getRequestHostname", self.getRequestHostname()
#        print "getHost", self.getHost()#infomation of proxy server itself
#        print "getClient", self.getClient()#connecting client e.g.) ~~no-Mac-Book-Pro
#        print "getPassword", self.getPassword()#no output
#        print "getHeader", self.getHeader()#this need key argument
#        print "getCookie", self.getCookie()#this need key argument
#        print "parseCookies", self.parseCookies()#only None
#        print "getUser", self.getUser()#no output
#        self.redirect("www.Google.com")#does not work well(I don't know how to use this)
        
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
