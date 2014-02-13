import tornado.ioloop
import tornado.web
import tornado.websocket

from tornado.options import define, options, parse_command_line

define("port", default = 8080, help = "run on the given port", type = int)

clients = dict()

class IndexHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        self.write("This is your response")
        self.finish()

class EchoWebSocket(tornado.websocket.WebSocketHandler):
    #on_message -> receive data
    #write_message -> send data
    def open(self):
        #self.receive_message(self.on_message)
        print "WebSocket opend"

    def on_message(self, message):
        #self.write_message(u'You said:' + message)

#    def write_message(self):
        i  = 0
        while i < 20:
            self.write_message(str(i) + " \n")
            i += 1

    def on_close(self):
        print "WebSocket closed"

app = tornado.web.Application([
    (r"/", IndexHandler),
    (r"/ws", EchoWebSocket),
])

if __name__ == "__main__":
    parse_command_line()
    app.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
