import socket
import sys
import datetime, time
import threading

buff = 1024
class serThread(threading.Thread):
	
	def __init__(self, sock, sock2, tarAddr, function):
		threading.Thread.__init__(self)
		self.setDaemon(True)
		self.sock = sock
		self.sock2 = sock2
		self.tarAddr = tarAddr
		self.function = function
	
		
	def run(self):
		if self.function == "c2s":		
			while True:
				message, a = self.sock.recvfrom(buff)
				if message == "kill server":
					break
				self.sock2.sendto(message, self.tarAddr)
					
		elif self.function == "s2s":
			while True:
				message, a = self.sock2.recvfrom(buff)
				self.d = datetime.datetime.today()
				print message, '%sh%sm%s.%ss' % (self.d.hour, self.d.minute, self.d.second, self.d.microsecond)
				
def main(Host, c2sPort, s2sPort, target):
	c2sAddr = (Host, c2sPort)
	s2sAddr = (Host, s2sPort)
	tarAddr = (Host, target)
	
	c2sSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	c2sSock.bind(c2sAddr)
	
	s2sSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s2sSock.bind(s2sAddr)
		
	c2sThread = serThread(c2sSock, s2sSock, tarAddr,"c2s")
	s2sThread = serThread(c2sSock, s2sSock, tarAddr,"s2s")
	
	s2sThread.start()
	c2sThread.start()
	
	time.sleep(200)
	
	

if __name__ == "__main__":
	if len(sys.argv) < 5:
		print "Usage : python this.py Host c2sPort s2sPort targetPort"
		sys.exit(1)
	main(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]))
