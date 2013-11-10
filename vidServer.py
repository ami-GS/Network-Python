import cv2.cv as cv
import cv2
import numpy
import socket

if __name__ == "__main__":
	cv.NamedWindow("serverCAM", 1)
	
	udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	udp.bind(("127.0.0.1", 12345))
	
	buff = 1024
	while True:
		jpgstring, addr = udp.recvfrom(buff*64)
		narray = numpy.fromstring(jpgstring, dtype = "uint8")
		decimg = cv2.imdecode(narray,1)
                
		cv2.imshow("serverCAM", decimg)
		if cv.WaitKey(10) == 27:
			break
	
	cv.DestroyAllWindows()
	udp.close()
