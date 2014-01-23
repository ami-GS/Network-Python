import pyaudio
import socket
from pylab import *
import numpy as np


frames = []

if __name__ == "__main__":
    FORMAT = pyaudio.paInt16
    CHUNK  = 1024
    CHANNELS = 2
    RATE = 44100
    RECORD_SECONDS = 10

    p = pyaudio.PyAudio()
    
    stream = p.open(format = FORMAT,
                    channels = CHANNELS,
                    rate = RATE,
                    input = True,
                    frames_per_buffer = CHUNK,
                    )

    for i in range(int(RATE / CHUNK * RECORD_SECONDS)):
        frames.append(stream.read(CHUNK))

    print "finish recording", RECORD_SECONDS, "sec" ,

    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    for frame in frames:
        udp.sendto(frame,("127.0.0.1", 12345))

    dataBefore = "".join(frames)
    result = np.frombuffer(dataBefore, dtype = "int16") / float(2**15)
    print " ", len(result), "samples"
    
    x = arange(0, RECORD_SECONDS, float(RECORD_SECONDS) / len(result))
    plot(x,result)
    autoscale(enable = True, axis = "both", tight = "True")
    grid(True, "major", "both")
    title("Before")
    show()



    
