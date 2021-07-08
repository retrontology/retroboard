import pydub
import sounddevice
import numpy
from threading import Thread
from functools import partial

class AudioEntry():
    
    def __init__(self, path:str, parent, gain=0):
        self.parent = parent
        self.path = path
        self.gain = gain
        self.frame_index = dict()
        self.segment = None
        self.frame_count = None
        self.streams = dict()
    
    def load_audio(self):
        self.segment = pydub.AudioSegment.from_file(self.path)
        self.detect_max_channels()

    def detect_max_channels(self):
        device_indexes = self.parent.get_devices()
        max_channels = sounddevice.query_devices(device_indexes[0])['max_output_channels']
        for index in device_indexes:
            c = sounddevice.query_devices(index)['max_output_channels']
            if c < max_channels:
                max_channels = c
        if max_channels < self.segment.channels:
            self.segment = self.segment.set_channels(max_channels)
    
    def clear_audio(self):
        self.segment = None
    
    def playback_callback(self, device_index, outdata, frame_count, time_info, status):
        if status:
            print(status)
        remainder = int(self.segment.frame_count()) - self.frame_index[device_index]
        if remainder < 1:
            raise sounddevice.CallbackStop
        valid_frames = frame_count if remainder >= frame_count else remainder
        data = numpy.array(self.segment.get_sample_slice(start_sample=self.frame_index[device_index], end_sample=self.frame_index[device_index]+valid_frames).get_array_of_samples())
        outdata[:valid_frames] = data.reshape(valid_frames, self.segment.channels)[:valid_frames]
        outdata[valid_frames:] = 0
        self.frame_index[device_index] += valid_frames
    
    def playback_finished(self, device_index):
        self.streams.pop(device_index)
        self.frame_index.pop(device_index)
        if len(self.streams) == 0:
            if self in self.parent.playing:
                self.parent.playing.remove(self)
            self.clear_audio()
            del self

    def play(self):
        self.stop()
        self.playback_thread = Thread(target=self._play)
        self.playback_thread.start()

    def _play(self):
        if not self.segment:
            self.load_audio()
        device_index = 0
        for device in self.parent.get_devices():
            self.frame_index[device_index] = 0
            try:
                output = sounddevice.OutputStream(callback=partial(self.playback_callback, device_index), finished_callback=partial(self.playback_finished, device_index), device=device, samplerate=self.segment.frame_rate, channels=self.segment.channels, dtype=self.segment.array_type)
                self.streams[device_index] = output
                output.start()
                device_index += 1
            except Exception as e:
                self.parent.error(e)

    def stop(self):
        for i in range(len(self.streams)):
            self.streams[i].stop()