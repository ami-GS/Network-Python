from ws4py.client.tornadoclient import TornadoWebSocketClient
from tornado import ioloop
import wsaccel
wsaccel.patch_tornado()

class MyClient(TornadoWebSocketClient):
    def opened(self):
        for i in range(0, 200, 25):
            self.send("*" * i)

    def received_message(self, m):
        print m
        if len(m) == 175:
            self.close(reason="aiueo")
     

    def closed(self, code, reason=None):
        print reason
        ioloop.IOLoop.instance().stop()

ws = MyClient("ws://localhost:8080/echo", protocols=["http-only", "chat"])
ws.connect()

ioloop.IOLoop.instance().start()
