import cv2.cv as cv
import cv2
import numpy
import zlib
import threading

from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor

class VideoClientDatagramProtocol(DatagramProtocol):
    def __init__(self, video):
        DatagramProtocol.__init__(self)
        self.video = video

    def datagramReceived(self, datagram, addr):
        #stop editting here
        pass

class videoShow(threading):
    def __init__(self):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.frames = []
        self.split = 10
        self.imstr = [""]*self.split
        cv.NamedWindow("clientCAM", 1)

    def run(self):

    def show(self):
        img =


def main():
    video = videoShow()
    protocol = VideoClientDatagramProtocol(video)
    t = reactor.listenUDP(0, protocol)
    reactor.run()

if __name__ == "__main__":
    main()