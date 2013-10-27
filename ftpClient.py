import os, struct, socket, sys

def main(host,port,inputfile):
	#prepare the racket to be sent
	with open(inputfile, 'rb') as file:
		data = file.read()
		
	#get the size of the image and pack it to 4-byte
	size = struct.pack("<I", os.path.getsize(inputfile))
	#format the filename to 30-byte and encode it
	if "/" in inputfile:
		inputfile = inputfile.split("/")[-1]
	filename = inputfile.rjust(30).encode()
	
	#packed all the bytes, 4-byte size, 30-byte filename, rest of image data
	packet = size + filename + data
	
	#create client socket
	client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	#connect client socket to server
	client.connect((host, port))
	#send packet 1024 at a time
	client.sendall(packet)
	#properly shutdown the client
	client.shutdown(socket.SHUT_RDWR)
	#close the client socket
	client.close()
	
	
if __name__ == "__main__":
	if len(sys.argv) < 4:
		print "Usage : python ftpClient.py remote-IP remote-Port fileName"
		sys.exit(1)

	main(sys.argv[1], int(sys.argv[2]), sys.argv[3])
