import cv2.cv as cv
import zlib
import threading
import time

from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor

status = False
class VideoServer(DatagramProtocol):
    def __init__(self, video):
        global status
        status = True
        self.video = video

    def startProtocol(self):
        self.transport.connect("127.0.0.1", 12345)
        self.sendDatagram()

    def sendDatagram(self):
        while True:
            if len(self.video.frames):
                datagram = self.video.frames.pop(0)
                for i in range(self.video.split):
                    self.transport.write(datagram[i])
            else:
                continue

class videoStore(threading.Thread):
    def __init__(self, capture):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.capture = capture
        self.frames = []
        self.split = 10
        self.splittedStr = [""]*self.split

    def run(self):
        global status
        split = self.split
        while True:
            time.sleep(0.3)
            while status:
                self.takePic(split)

    def takePic(self, split):
        img = cv.QueryFrame(self.capture)
        jpgstring = cv.EncodeImage(".jpg", img).tostring()
#        jpgstring = zlib.compress(jpgstring)

        jpglen = len(jpgstring)
        for i in range(split-1):
            self.splittedStr[i] = jpgstring[jpglen/split*i:jpglen/split*(i+1)]
        self.splittedStr[split-1] = jpgstring[jpglen/split*(split-1):]
        cv.WaitKey(30)

        self.frames.append(self.splittedStr)

    def stop(self):
        cv.DestroyAllWindows()


def main():
    capture = cv.CaptureFromCAM(0)
    cv.SetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_WIDTH, 240)
    cv.SetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_HEIGHT, 180)

    video = videoStore(capture)
    video.start()
    time.sleep(1)
    server = VideoServer(video)
    reactor.listenUDP(0, server)

if __name__ == '__main__':
    main()
