import cv2.cv as cv
import zlib
import threading
import time

from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor

class VideoServer(DatagramProtocol):
    def __init__(self, video):
        #DatagramProtocol.__init__(self)
        self.video = video

    def startProtocol(self):
        self.transport.connect("127.0.0.1", 12345)
        self.sendDatagram()

    def sendDatagram(self):
        if len(self.video.frames):
            while len(self.video.frames):
                datagram = self.video.frames.pop(0)
                for i in range(self.video.split):
                    self.transport.write(datagram[i])
        else:
            reactor.stop()
            self.video.stop()

class videoStore(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.frames = []
        self.capture = cv.CaptureFromCAM(0)
        self.split = 2
        self.splittedStr = [""]*self.split
        cv.NamedWindow("ServerCAM",1)
        cv.SetCaptureProperty(self.capture, cv.CV_CAP_PROP_FRAME_WIDTH, 24)
        cv.SetCaptureProperty(self.capture, cv.CV_CAP_PROP_FRAME_HEIGHT, 18)

    def run(self):
        split = self.split
        while True:
            self.takePic(split)

    def takePic(self, split):
        img = cv.QueryFrame(self.capture)
        jpgstring = cv.EncodeImage(".jpeg", img).tostring()
        jpgstring = zlib.compress(jpgstring)

        jpglen = len(jpgstring)
        for i in range(split-1):
            self.splittedStr[i] = jpgstring[jpglen/split*i:jpglen/split*(i+1)]
        self.splittedStr[split-1] = jpgstring[jpglen/split*(split-1):]

        self.frames.append(self.splittedStr)

    def stop(self):
        cv.DestroyAllWindows()


def main():
    video = videoStore()
    video.start()
    time.sleep(1)
    reactor.listenUDP(0, VideoServer(video))
    reactor.run()

if __name__ == '__main__':
    main()
