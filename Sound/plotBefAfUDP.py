__author__ = 'daiki'

import socket
import threading
import pyaudio
import numpy as np
from pylab import *
import time
import zlib

event = threading.Event()

class UDP():
    def __init__(self):
        self.frames = []
        self.udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def getFrames(self):
        return self.frames
    def getJoinedData(self):
        return "".join(self.frames)
    def getData(self):
        return np.frombuffer(self.getJoinedData(), dtype = "int16") / float(2**15)



class Server(threading.Thread, UDP):
    def __init__(self, CHUNK):
        threading.Thread.__init__(self)
        UDP.__init__(self)
        self.setDaemon(True)
        self.udp.bind(("127.0.0.1", 12345))
        self.CHUNK = CHUNK*4
        self.moveFlag = True

    def run(self):
        while True:
            try:
                recv, addr = self.udp.recvfrom(self.CHUNK)
                self.frames.append(zlib.decompress(recv))
                if self.moveFlag:
                    self.udp.settimeout(1)
                    self.moveFlag = False
            except socket.error, msg:
                break
        
        event.set()
        event.clear()


class Client(threading.Thread, UDP):
    def __init__(self, stream, CHUNK, recTime):
        threading.Thread.__init__(self)
        UDP.__init__(self)
        self.setDaemon(True)
        self.CHUNK = CHUNK
        self.stream = stream
        self.recTime = recTime

    def run(self):
        for i in range(int(self.stream._rate / self.CHUNK * self.recTime)):
            self.frames.append(self.stream.read(self.CHUNK))

        event.set()
        event.clear()

        for frame in self.frames:
            self.udp.sendto(zlib.compress(frame), ("127.0.0.1", 12345))


if __name__ == "__main__":
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
#    RATE = 8000#phone
    CHUNK = 1024
    RECORD_SECONDS = 20

    p = pyaudio.PyAudio()

    stream = p.open(format = FORMAT,
                    channels = CHANNELS,
                    rate = RATE,
                    input = True,
                    frames_per_buffer = CHUNK,
                    )

    client = Client(stream, CHUNK, RECORD_SECONDS)

    server = Server(CHUNK)

    server.start()
    client.start()


    event.wait()
    Cresult = client.getData()
    event.wait()
    Sresult = server.getData()

    print "Before sample:", len(Cresult)
    print "After sample:", len(Sresult)
    print float(len(Sresult))/len(Cresult)*100, "% data could be send"

 
    x = arange(0, RECORD_SECONDS, float(RECORD_SECONDS) / len(Cresult))
    subplot(211)
    plot(x, Cresult)
    autoscale(enable = True, axis = "both", tight = "True")
    grid(True, "major", "both")
    title("Before")

    subplot(212)
    plot(Sresult)
    autoscale(enable = True, axis = "both", tight = "True")
    grid(True, "major", "both")
    title("After")

    show()

