import pyaudio
import socket
from pylab import *
import numpy as np
import time


frames = []
CHUNK = 1024


def Receive():
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp.bind(("127.0.0.1", 12345))

    moveFlag = True

    while True:
#        print len(frames)
        try:
            recv, addr = udp.recvfrom(CHUNK)
            frames.append(recv)
            if moveFlag:
                udp.settimeout(1)
                moveFlag = False

        except socket.error, msg:
            break

    dataAfter = "".join(frames)
    result = np.frombuffer(dataAfter, dtype = "int16") / float(2**15)

    plot(result)
    autoscale(enable = True, axis = "both", tight = "True")
    grid(True, "major", "both")
    title("After")

    show()
    
    udp.close()

if __name__ == "__main__":
    Receive()
