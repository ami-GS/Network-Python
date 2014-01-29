import cv2.cv as cv
import cv2
import socket
import zlib

if __name__ == "__main__":
	udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	
#	cv.NamedWindow("ClientCAM", 1)
	capture = cv.CaptureFromCAM(0)
	cv.SetCaptureProperty(capture,cv.CV_CAP_PROP_FRAME_WIDTH,160)
	cv.SetCaptureProperty(capture,cv.CV_CAP_PROP_FRAME_HEIGHT,120)  
	while True:
		img = cv.QueryFrame(capture)
		jpgstring = cv.EncodeImage(".jpeg", img).tostring()
#		cv.ShowImage("ClientCAM", img)
		jpgstring = zlib.compress(jpgstring)
		udp.sendto(jpgstring, ("127.0.0.1", 12345))
		if cv.WaitKey(10) == 27:
			break
	
	cv.DestroyAllWindows()
	udp.close()
