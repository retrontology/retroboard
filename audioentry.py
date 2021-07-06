import pydub
import sounddevice
import numpy
from threading import Thread

class AudioEntry():
    
    def __init__(self, path:str, parent, gain=0):
        self.parent = parent
        self.path = path
        self.gain = gain
        self.frame_index = 0
        self.segment = None
        self.data = None
        self.frame_count = None
        self.streams = []
    
    def load_audio(self):
        self.segment = pydub.AudioSegment.from_file(self.path)
        data = numpy.array(self.segment.get_array_of_samples())
        self.data = data.reshape(int(len(data)/self.segment.channels), self.segment.channels)
        self.frame_count = len(self.data)
    
    def clear_audio(self):
        self.data = None
        self.segment = None
    
    def playback_callback(self, outdata, frame_count, time_info, status):
        if status:
            print(status)
        remainder = self.frame_count - self.frame_index
        if remainder < 1:
            raise sounddevice.CallbackStop
        valid_frames = frame_count if remainder >= frame_count else remainder
        outdata[:valid_frames] = self.data[self.frame_index:self.frame_index + valid_frames]
        outdata[valid_frames:] = 0
        self.frame_index += valid_frames
    
    def playback_finished(self):
        self.parent.playing.remove(self)
        self.clear_audio()
        del self

    def play(self):
        self.stop()
        self.playback_thread = Thread(target=self._play)
        self.playback_thread.start()

    def _play(self):
        if not self.segment or not self.data:
            self.load_audio()
        for device in self.parent.get_devices():
            try:
                output = sounddevice.OutputStream(callback=self.playback_callback, finished_callback=self.playback_finished, device=device, samplerate=self.segment.frame_rate, channels=self.segment.channels, dtype=self.data.dtype)
                output.start()
                self.streams.append(output)
            except Exception as e:
                self.parent.error(e)

    def stop(self):
        for stream in self.streams:
            stream.stop()
        self.streams.clear()