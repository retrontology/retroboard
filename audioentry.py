import av
import sounddevice
import numpy as np
from threading import Thread
from functools import partial
from errorwindow import ErrorWindow

class AudioEntry():
    
    def __init__(self, path:str, parent):
        self.parent = parent
        self.path = path
        self.gain = dict()
        self.frame_index = dict()
        self.streams = dict()
        self.stop = False
        self.audio_container = av.open(self.path)
        self.frames = None
    
    def load_audio(self):
        self.frames = []
        for frame in self.audio_container.decode(audio=0):
            self.frames.append(frame)
        self.get_channels()
        #self.detect_max_channels()
    
    def get_channels(self):
        self.channels = len(self.frames[0].layout.channels)

    def get_audio_stream(self):
        return self.audio_container.streams.get(audio=0)[0]

    """ def detect_max_channels(self):
        device_indexes = self.parent.get_devices()
        max_channels = self.audio_container.
        for index, gain in device_indexes:
            c = sounddevice.query_devices(index)['max_output_channels']
            if c < max_channels:
                max_channels = c
        if max_channels < self.segment.channels:
            self.segment = self.segment.set_channels(max_channels) """
    
    def clear_audio(self):
        self.frames = None
    
    def playback_callback(self, device_index, outdata, frame_count, time_info, status):
        if status:
            print(status)
        if self.stop:
            raise sounddevice.CallbackStop
        remainder = len(self.frames) - self.frame_index[device_index]
        if remainder < 1:
            raise sounddevice.CallbackStop
        gain = self.gain[device_index].get()
        valid_frames = frame_count if remainder >= frame_count else remainder
        
        data = self.frames[self.frame_index[device_index]].to_ndarray()
        if remainder > 1:
            for frame in self.frames[self.frame_index[device_index]+1:self.frame_index[device_index]+valid_frames]:
                data = np.append(data, frame.to_ndarray(), 1)
        data = np.transpose(data)

        data = np.vectorize(lambda x: apply_gain(x, gain))(data)
        outdata[:valid_frames] = data[:valid_frames]
        outdata[valid_frames:] = 0
        self.frame_index[device_index] += valid_frames
        print(outdata)
    
    def playback_finished(self, device_index):
        self.streams.pop(device_index)
        self.frame_index.pop(device_index)
        if len(self.streams) == 0:
            if self in self.parent.playing:
                self.parent.playing.remove(self)
            self.clear_audio()
            del self

    def play(self):
        self.playback_thread = Thread(target=self._play, daemon=True)
        self.playback_thread.start()

    def _play(self):
        if not self.frames:
            self.load_audio()
        device_index = 0
        for device, gain in self.parent.get_devices():
            self.gain[device_index] = gain
            self.frame_index[device_index] = 0
            try:
                print(self.frames[0].sample_rate)
                output = sounddevice.OutputStream(callback=partial(self.playback_callback, device_index), finished_callback=partial(self.playback_finished, device_index), device=device, channels=self.channels, samplerate=self.frames[0].sample_rate, dtype=self.frames[0].to_ndarray().dtype)
                self.streams[device_index] = output
                output.start()
                device_index += 1
            except Exception as e:
                self.parent.error(e)

def apply_gain(input, gain):
    return 10**(gain/10)*input