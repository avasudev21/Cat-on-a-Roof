##Stores framework for pyaudio functions as well as threading functions

##Module manager code taken from:
##https://raw.githubusercontent.com/CMU15-112/module-manager/master/module_manager.py
import module_manager
module_manager.review()
import os
import wave
import threading
import sys
import pyaudio

##adapted from https://abhgog.gitbooks.io/pyaudio-manual/sample-project.html
def record(outputFile):
    CHUNK = 1024 
    FORMAT = pyaudio.paInt16
    CHANNELS = 2 
    RATE = 44100 
    RECORD_SECONDS = 2 

    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("* recording")

    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("* done recording")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(outputFile, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()


##adapted from https://gist.github.com/THeK3nger/3624478
class WavePlayerLoop(threading.Thread) : 
  CHUNK = 1024

  def __init__(self,filepath,loop=True) :
    super(WavePlayerLoop, self).__init__()
    self.filepath = os.path.abspath(filepath)
    self.loop = loop

  def run(self):
    # Open Wave File and start play!
    wf = wave.open(self.filepath, 'rb')
    player = pyaudio.PyAudio()

    # Open Output Stream (basen on PyAudio tutorial)
    stream = player.open(format = player.get_format_from_width(wf.getsampwidth()),
        channels = wf.getnchannels(),
        rate = wf.getframerate(),
        output = True)

    # PLAYBACK LOOP
    data = wf.readframes(self.CHUNK)
    while self.loop :
      stream.write(data)
      data = wf.readframes(self.CHUNK)
      if data == '' : # If file is over then rewind.
        wf.rewind()
        data = wf.readframes(self.CHUNK)

    stream.close()
    player.terminate()
    
  def play(self) :
    self.start()

  def stop(self) :
    self.loop = False

 