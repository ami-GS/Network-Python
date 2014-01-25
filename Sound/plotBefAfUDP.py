
__author__ = 'daiki'

import socket
from threading import Thread
import pyaudio
import numpy as np
from pylab import *
import time


class Server(Thread):

    def __init__(self, CHUNK):
        Thread.__init__(self)
        self.setDaemon(True)
        self.udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp.bind(("127.0.0.1", 12345))
        self.CHUNK = CHUNK
        self.frames = []
        self.finRecv = False
        self.moveFlag = True



    def run(self):
        while True:
            try:
                recv, addr = self.udp.recvfrom(self.CHUNK)
                self.frames.append(recv)
                if self.moveFlag:
                    self.udp.settimeout(1)
                    self.moveFlag = False
            except socket.error, msg:
                break

        self.finRecv = True


    def getFrames(self):
        return self.frames

    def getJoinedData(self):
        return "".join(self.frames)

    def getData(self):
        return np.frombuffer(self.getJoinedData(), dtype = "int16") / float(2**15)


class Client(Thread):
    def __init__(self, stream, CHUNK, recTime):
        Thread.__init__(self)
        self.setDaemon(True)
        self.udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.CHUNK = CHUNK
        self.stream = stream
        self.frames = []
        self.recTime = recTime
        self.finRec = False

    def run(self):
        for i in range(int(self.stream._rate / self.CHUNK * self.recTime)):
            self.frames.append(self.stream.read(self.CHUNK))

        self.finRec = True

        for frame in self.frames:
            self.udp.sendto(frame,("127.0.0.1", 12345))

    def getFrames(self):
        return self.frames

    def getJoinedData(self):
        return "".join(self.frames)

    def getData(self):
        return np.frombuffer(self.getJoinedData(), dtype = "int16") / float(2**15)

if __name__ == "__main__":
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
#    RATE = 8000#phone
    CHUNK = 1024
    RECORD_SECONDS = 3

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


    while not client.finRec:
        time.sleep(0.1)
    else:
        Cresult = client.getData()

    while not server.finRecv:
        time.sleep(0.1)
    else:
        Sresult = server.getData()


    print "Before sample:", len(Cresult)
    print "After sample:", len(Sresult)
    print float(len(Sresult))/len(Cresult)*100, "% data could be send"

    """
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
    """