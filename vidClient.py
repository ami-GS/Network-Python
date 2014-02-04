import cv2.cv as cv
import cv2
import socket
import zlib

if __name__ == "__main__":
	udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	
	split = 10
	splittedstr = [""]*split
	cv.NamedWindow("ClientCAM", 1)
	capture = cv.CaptureFromCAM(0)
	cv.SetCaptureProperty(capture,cv.CV_CAP_PROP_FRAME_WIDTH,480)
	cv.SetCaptureProperty(capture,cv.CV_CAP_PROP_FRAME_HEIGHT,360)  

	while True:
		img = cv.QueryFrame(capture)
		jpgstring = cv.EncodeImage(".jpeg", img).tostring()
#		cv.ShowImage("ClientCAM", img)
		jpgstring = zlib.compress(jpgstring)

		jpglen = len(jpgstring)
		for i in range(split-1):
			splittedstr[i] = jpgstring[jpglen/split*i:jpglen/split*(i+1)]
		splittedstr[split-1] = jpgstring[jpglen/split*(split-1):]

		for i in range(split):
			udp.sendto(splittedstr[i], ("127.0.0.1", 12345))

		if cv.WaitKey(10) == 27:
			break
	
	cv.DestroyAllWindows()
	udp.close()
