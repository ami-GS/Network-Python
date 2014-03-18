import sys
import socket

import tornado.httpserver
import tornado.ioloop
import tornado.iostream
import tornado.web
import tornado.httpclient
import redis

__all__ = ['ProxyHandler', 'run_proxy']

r = redis.Redis(host="127.0.0.1", port=6379, db=0)
r.flushall()
class ProxyHandler(tornado.web.RequestHandler):
    SUPPORTED_METHODS = ['GET', 'POST', 'CONNECT']
    @tornado.web.asynchronous
    def returnCache(self):
        pass

    @tornado.web.asynchronous
    def setCache(self, response):
        v = ""
        for header in ('Date', 'Cache-Control', 'Server',
                       'Content-Type', 'Location'):
            v = response.headers.get(header)
        resp = [response.code, v, response.body]
        r.rpush(self.request.uri, response.code)
        r.rpush(self.request.uri, header)
        r.rpush(self.request.uri, v)        
        r.rpush(self.request.uri, response.body)
        r.expire(self.request.uri, 100)
        print "cache !!"

    @tornado.web.asynchronous
    def get(self):

        def handle_response(response):
            print response.code
            if response.code == 599:
                return
            if response.error and not isinstance(response.error,
                    tornado.httpclient.HTTPError):
                self.set_status(500)
                self.write('Internal server error:\n' + str(response.error))
                self.finish()
            else:
                self.set_status(response.code)
                for header in ('Date', 'Cache-Control', 'Server',
                        'Content-Type', 'Location'):
                    v = response.headers.get(header)
                    if v:
                        self.set_header(header, v)
                if response.body:
                    self.write(response.body)
                self.finish()

                if not r.exists(self.request.uri):
                    self.setCache(response)

        def my_handler(response):
            self.set_status(int(response[0]))
            if response[2]:
                self.set_header(response[1], response[2])
            if response[3]:
                self.write(response[3])
            self.finish()

        if r.exists(self.request.uri):
            print "return cache !!"
            my_handler(r.lrange(self.request.uri,0,-1))
        else:
            req = tornado.httpclient.HTTPRequest(
                url=self.request.uri,
                method=self.request.method, body=self.request.body,
                headers=self.request.headers, follow_redirects=False,
                allow_nonstandard_methods=True)
            client = tornado.httpclient.AsyncHTTPClient()
            try:
                client.fetch(req, handle_response)
            except tornado.httpclient.HTTPError as e:
                if hasattr(e, 'response') and e.response:
                    handle_response(e.response)
                else:
                    self.set_status(500)
                    self.write('Internal server error:\n' + str(e))
                    self.finish()

    @tornado.web.asynchronous
    def post(self):
        return self.get()

    @tornado.web.asynchronous
    def connect(self):
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
            client.write(b'HTTP/1.1 200 Connection established\r\n\r\n')

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        upstream = tornado.iostream.IOStream(s)
        upstream.connect((host, int(port)), start_tunnel)

 

def run_proxy(port, start_ioloop=True):
    """
    Run proxy on the specified port. If start_ioloop is True (default),
    the tornado IOLoop will be started immediately.
    """
    app = tornado.web.Application([
        (r'.*', ProxyHandler),
    ])
    app.listen(port)
    ioloop = tornado.ioloop.IOLoop.instance()
    if start_ioloop:
        ioloop.start()

if __name__ == '__main__':
    port = 8888
    if len(sys.argv) > 1:
        port = int(sys.argv[1])

    print ("Starting HTTP proxy on port %d" % port)
    run_proxy(port)
