import pydub
import sounddevice
import numpy

class AudioEntry():
    
    def __init__(self, path:str, devices:list, gain=0):
        self.path = path
        self.devices = devices.copy()
        self.gain = gain
        self.frame_index = 0
        self.segment = None
        self.data = None
    
    def load_audio(self):
        self.segment = pydub.AudioSegment.from_file(self.path)
        data = numpy.array(self.segment.get_array_of_samples())
        self.data = data.reshape(int(len(data)/self.segment.channels), self.segment.channels)
    
    def play(self):
        if not self.segment or not self.data:
            self.load_audio()
        for device in self.devices:
            sounddevice.play(self.data, self.segment.frame_rate, device=device)