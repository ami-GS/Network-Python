#server that receive the file
import socket, struct, sys

def main(port):
	#create new server socket
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	#bind port
	server.bind(("127.0.0.1", port))
	#ser max accept rate to 5 connections
	server.listen(5)
	#server socket accept the client
	client, address = server.accept()
	#get 4-byte packet
	size_bytes = client.recv(4)
	#unpack 4-byte packet that determine the size of image
	size = struct.unpack("<I", size_bytes)[0]
	#decode the 30-byte that determine the filename and strip the space
	filename = client.recv(30).decode().lstrip()
	#get the remaining image bytes from client
	get_bytes(client, size, filename)
	#Shutdown the socket and close the server connection
	client.close()
	server.close()
	print "Server has received the data from the client! "
	
#method to get the image bytes from client to the sever
def get_bytes(sock, size, filename):
	packet = bytearray()
	i = 0
	while len(packet) < size:
		#store the btes in the buffer
		buffer = sock.recv(size - len(packet))
		if not buffer:
			#throw an exception if could not get all the data
			raise EOFError("Could not receive all expected data!")
		#append buffer into packet
		packet.extend(buffer)
		print len(packet), size, i
		i += 1
		#immediately write the bytes received to the file in current server directory
	with open(filename, "wb") as file:
		file.write(packet)


if __name__ == "__main__":
	if len(sys.argv) < 2:
		print "Usage : python ftpServer.py Port"
		sys.exit(1)
	main(int(sys.argv[1]))
	
	
