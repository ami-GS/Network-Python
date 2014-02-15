from ws4py.client.tornadoclient import TornadoWebSocketClient
from tornado import ioloop
import wsaccel
wsaccel.patch_tornado()

class MyClient(TornadoWebSocketClient):
    def opened(self):
        self.N = 1000000
        for i in range(self.N):
            self.send(str(i))

    def received_message(self, m):
        pass
#        print m


    def closed(self, code, reason=None):
        ioloop.IOLoop.instance().stop()

ws = MyClient("ws://localhost:8080/echo", protocols=["http-only", "chat"])
ws.connect()

ioloop.IOLoop.instance().start()
