import pyaudio
import socket
from threading import Thread


def udpStream(stream, CHUNK):
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)    
    while True:
        udp.sendto(stream.read(CHUNK), ("127.0.0.1", 12345))
    udp.close()


if __name__ == "__main__":
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100

    p = pyaudio.PyAudio()

    stream = p.open(format = FORMAT,
                    channels = CHANNELS,
                    rate = RATE,
                    input = True,
                    frames_per_buffer = CHUNK,
                    )

    udpStream(stream, CHUNK)
    """
    stream.stop_stream()
    stream.close()
    p.terminate()
    """
