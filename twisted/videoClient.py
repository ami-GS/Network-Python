import cv2.cv as cv
import cv2
import numpy
import zlib
import threading
import time

from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor

class VideoClientDatagramProtocol(DatagramProtocol):
    def __init__(self, video):
        #DatagramProtocol.__init__(self)
        self.imstr = []
        self.video = video


    def datagramReceived(self, datagram, addr):
        self.imstr.append(datagram)
        print len(datagram)
        if len(self.imstr) == 10:
            self.video.frames.append("".join(self.imstr))
            self.imstr = []
#        self.video.frames.append(datagram)


class videoShow(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.frames = []
        self.split = 10
        #self.imstr = [""]*self.split
        cv.NamedWindow("clientCAM", 1)

    def run(self):
        while True:
            self.show()


    def show(self):
        if len(self.frames):
            jpgstring = zlib.decompress(self.frames.pop(0))
            narray = numpy.fromstring(jpgstring, dtype = "uint8")
            decimage = cv2.imdecode(narray,1)
            cv2.imshow("clientCAM", decimage)



def main():
    video = videoShow()
    video.start()
    time.sleep(1)
    protocol = VideoClientDatagramProtocol(video)

    t = reactor.listenUDP(12345, protocol)
    reactor.run()

if __name__ == "__main__":
    main()