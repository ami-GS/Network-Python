import time
import tornado.ioloop
import tornado.web
import tornado.websocket
from tornado.ioloop import PeriodicCallback

from tornado.options import define, options, parse_command_line


define("port", default = 8080, help = "run on the given port", type = int)

class IndexHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        self.write("This is your response")
        self.finish()


class SendWebSocket(tornado.websocket.WebSocketHandler):
    #on_message -> receive data
    #write_message -> send data
    def open(self):
        self.callback = PeriodicCallback(self._send_message, 400)
        self.callback.start()
        print "WebSocket opend"

    def on_message(self, message):
        print message


    def _send_message(self):
#        self.i += 1
#        print i, self.i
        self.write_message("test")

    def on_close(self):
        self.callback.stop()
        print "WebSocket closed"

app = tornado.web.Application([
    (r"/", IndexHandler),
    (r"/ws", SendWebSocket),
])

if __name__ == "__main__":
    parse_command_line()
    app.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
