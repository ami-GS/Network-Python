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
        self.imstr = []
        self.video = video


    def datagramReceived(self, datagram, addr):
        self.imstr.append(datagram)
        if len(self.imstr) == self.video.split:
            self.video.frames.append("".join(self.imstr))
            self.imstr = []


class videoShow(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.frames = []
        self.split = 10
        self.cont = True

    def run(self):
        while self.cont:
            self.show()


    def show(self):
        if len(self.frames):
            jpgstring = self.frames.pop(0)
#            try:
#                jpgstring = zlib.decompress(jpgstring)
#            except Exception as e:
#                print e
            narray = numpy.fromstring(jpgstring, dtype = "uint8")
            decimage = cv2.imdecode(narray, 1)#Sometimes this returns None value
            if isinstance(decimage, type(None)):
                print "None"
                return
            cv2.imshow("clientCAM", decimage)
            if cv.WaitKey(30) == 27:
                return

def main():
    cv.NamedWindow("clientCAM", 1)
    video = videoShow()
    video.start()
    time.sleep(1)
    protocol = VideoClientDatagramProtocol(video)

    t = reactor.listenUDP(12345, protocol)
    reactor.run()

if __name__ == "__main__":
    main()
