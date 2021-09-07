import sounddevice
import numpy as np
from threading import Thread
from functools import partial
from avbuffer import AVBuffer

class AudioEntry():
    
    def __init__(self, path:str, item:str, parent):
        self.path = path
        self.item = item
        self.parent = parent
        self.gain = dict()
        self.streams = dict()
        self.stop = False
        self.buffer = dict()
    
    def playback_callback(self, device_index, outdata, frame_count, time_info, status):
        if status:
            print(status)
        if self.stop:
            raise sounddevice.CallbackStop
        
        data = self.buffer[device_index].read(frame_count)
        if len(data) < frame_count:
            frame_count = len(data)
            self.stop = True
        gain = self.gain[device_index].get()
        if gain != 0:
            data = np.vectorize(lambda x: apply_gain(x, gain))(data)
        outdata[:frame_count] = data[:frame_count]
        outdata[frame_count:] = 0
    
    def playback_finished(self, device_index):
        self.streams.pop(device_index).close()
        self.buffer.pop(device_index).close()
        self.gain.pop(device_index)
        if self in self.parent.playing:
            self.parent.playing.remove(self)
        del self

    def play(self):
        self.playback_thread = Thread(target=self._play, daemon=True)
        self.playback_thread.start()

    def _play(self):
        device_index = 0
        for device, sample_rate, max_channels, gain in self.parent.get_devices():
            self.gain[device_index] = gain
            self.buffer[device_index] = AVBuffer(self.path, sample_rate, max_channels)
            try:
                output = sounddevice.OutputStream(callback=partial(self.playback_callback, device_index), finished_callback=partial(self.playback_finished, device_index), device=device, channels=self.buffer[device_index].channels, samplerate=self.buffer[device_index].sample_rate, dtype=self.buffer[device_index].dtype)
                self.streams[device_index] = output
                output.start()
                device_index += 1
            except Exception as e:
                self.parent.error(e)

def apply_gain(input, gain):
    return 10**(gain/10)*input