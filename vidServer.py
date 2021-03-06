import cv2.cv as cv
import cv2
import numpy
import socket
import zlib

if __name__ == "__main__":
    cv.NamedWindow("serverCAM", 1)

    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp.bind(("127.0.0.1", 12345))

    buff = 1024
    split = 30
    imstr = [""] * split
    while True:
        for i in range(split):
            imstr[i], addr = udp.recvfrom(buff * 32)

        jpgstring = "".join(imstr)
        #try:
        #    jpgstring = zlib.decompress(jpgstring)
        #except Exception as e:
        #    print "error"
        narray = numpy.fromstring(jpgstring, dtype="uint8")
        decimg = cv2.imdecode(narray, 1)

        try:
            cv2.imshow("serverCAM", decimg)
        except Exception as e:
            print "show error"
            continue
        if cv.WaitKey(10) == 27:
            break

    cv.DestroyAllWindows()
    udp.close()
