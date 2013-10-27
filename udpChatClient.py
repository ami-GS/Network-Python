import socket
import sys

def main(Host, Port):
	addr = (Host, Port)
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	
	while True:
		message = raw_input(">> ")
		if message == "exit" or message == "quit":
			sock.close()
			sys.exit(1)
		
		sock.sendto(message, addr)


if __name__ == "__main__":
	if len(sys.argv) < 3:
		print "Usage : python this.py Host Port"
		sys.exit(1)
	main(sys.argv[1], int(sys.argv[2]))
