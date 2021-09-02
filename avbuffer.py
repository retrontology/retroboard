import av
import numpy as np

class AVBuffer():

    def __init__(self, path, sample_rate, max_channels):
        self.path = path
        self.max_channels = max_channels
        self.sample_rate = sample_rate
        self.exhausted = False
        self.init_buffer()
    
    def init_buffer(self):
        self._container = av.open(self.path)
        self._frames = self._container.decode(audio=0)
        frame = self._frames.__next__()
        if self.max_channels < len(frame.layout.channels):
            self.channels = self.max_channels
        else:
            self.channels = len(frame.layout.channels)
        self.resampler = av.audio.resampler.AudioResampler(format=None, layout=av.audio.layout.AudioLayout(self.channels), rate=self.sample_rate)
        frame.pts = None
        frame = self.resampler.resample(frame)
        frame = frame.to_ndarray()
        self.dtype = frame.dtype
        self._buffer = np.transpose(frame)

    def read(self, size=0):
        if self.exhausted:
            raise Exception('The file has already been read!')
        while size > len(self._buffer) or size == 0:
            try:
                frame = self._frames.__next__()
                frame.pts = None
                frame = np.transpose(self.resampler.resample(frame).to_ndarray())
                self._buffer = np.append(self._buffer, frame, 0)
            except StopIteration as e:
                self.exhausted = True
                self.close()
                break
        if size > len(self._buffer):
            size = len(self._buffer)
        out = self._buffer[:size]
        self._buffer = self._buffer[size:]
        return out
    
    def close(self):
        self._container.close()
