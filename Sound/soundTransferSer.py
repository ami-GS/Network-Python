import pyaudio
import socket
from threading import Thread

frames = []

def udpStream(CHUNK, CHANNELS):
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp.bind(("127.0.0.1", 12345))
    
    while True:
        soundData, addr = udp.recvfrom(CHUNK*CHANNELS*2)
        if soundData:
            frames.append(soundData)

    udp.close()

def play(stream, CHUNK):

    
    while True:
            if len(frames) == 10:
                while True:
                    if len(frames) > 0:
                        stream.write(frames.pop(0), CHUNK)


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

    Ts = Thread(target = udpStream, args=(CHUNK, CHANNELS,))
    Tp = Thread(target = play, args=(stream, CHUNK,))
    Ts.setDaemon(True)
    Tp.setDaemon(True)
    Ts.start()
    Tp.start()
    Ts.join()
    Tp.join()
    """
    stream.stopstream()
    stream.close()
    p.terminate()
    """
