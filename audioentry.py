import sounddevice
import numpy as np
from threading import Thread
from functools import partial
from avbuffer import AVBuffer

class AudioEntry():
    
    def __init__(self, path:str, parent):
        self.parent = parent
        self.gain = dict()
        self.frame_index = dict()
        self.streams = dict()
        self.stop = False
        self.buffer = AVBuffer(path)
    
    def __del__(self):
        del self.buffer
    
    def playback_callback(self, device_index, outdata, frame_count, time_info, status):
        if status:
            print(status)
        if self.stop:
            raise sounddevice.CallbackStop
        
        data = self.buffer.read(frame_count)
        if len(data) < frame_count:
            frame_count = len(data)
            self.stop = True
        gain = self.gain[device_index].get()
        data = np.vectorize(lambda x: apply_gain(x, gain))(data)
        outdata[:frame_count] = data[:frame_count]
        outdata[frame_count:] = 0
    
    def playback_finished(self, device_index):
        self.streams.pop(device_index)
        self.frame_index.pop(device_index)
        if len(self.streams) == 0:
            if self in self.parent.playing:
                self.parent.playing.remove(self)
            del self

    def play(self):
        self.playback_thread = Thread(target=self._play, daemon=True)
        self.playback_thread.start()

    def _play(self):
        device_index = 0
        for device, gain in self.parent.get_devices():
            self.gain[device_index] = gain
            self.frame_index[device_index] = 0
            try:
                output = sounddevice.OutputStream(callback=partial(self.playback_callback, device_index), finished_callback=partial(self.playback_finished, device_index), device=device, channels=self.buffer.channels, samplerate=self.buffer.sample_rate, dtype=self.buffer.dtype)
                self.streams[device_index] = output
                output.start()
                device_index += 1
            except Exception as e:
                self.parent.error(e)

def apply_gain(input, gain):
    return 10**(gain/10)*input