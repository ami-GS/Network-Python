import tornado.ioloop
import tornado.web
import tornado.websocket
from tornado.options import define, options, parse_command_line
import wsaccel
wsaccel.patch_tornado()
import time


define("port", default = 8080, help = "run on the given port", type = int)

class SendWebSocket(tornado.websocket.WebSocketHandler):
    #on_message -> receive data
    #write_message -> send data
    def open(self):
        self.s = time.time()
        print "WebSocket opend"

    def on_message(self, message):
        self.write_message(message)
#        print message
        if int(message) == 999999:
            self.on_close()



    def on_close(self):
        print time.time() - self.s
        print "WebSocket closed"

app = tornado.web.Application([
    (r"/echo", SendWebSocket),
])

if __name__ == "__main__":
    parse_command_line()
    app.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
