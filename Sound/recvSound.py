import pyaudio
import socket
from threading import Thread

frames = []

def udpStream(stream, CHUNK, CHANNELS):
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp.bind(("127.0.0.1", 12345))
    
    while True:
        soundData, addr = udp.recvfrom(CHUNK*CHANNELS*2)
        if soundData:
            stream.write(soundData, CHUNK)
            
    udp.close()

if __name__ == "__main__":
    FORMAT = pyaudio.paInt16
    CHUNK = 1024
    CHANNELS = 2
    RATE = 44100

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels = CHANNELS,
                    rate = RATE,
                    output = True,
                    frames_per_buffer = CHUNK,
                    )
    udpStream(stream, CHUNK, CHANNELS)
    """
    stream.stopstream()
    stream.close()
    p.terminate()
    """
