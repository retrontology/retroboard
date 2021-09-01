import av
import numpy as np

class AVBuffer():

    def __init__(self, path):
        self.path = path
        self.exhausted = False
        self.init_buffer()
    
    def init_buffer(self):
        self._container = av.open(self.path)
        self._frames = self._container.decode(audio=0)
        frame = self._frames.__next__()
        self.channels = len(frame.layout.channels)
        self.sample_rate = frame.sample_rate
        frame = frame.to_ndarray()
        self.dtype = frame.dtype
        self._buffer = np.transpose(frame)

    def read(self, size=0):
        if self.exhausted:
            raise Exception('The file has already been read!')
        while size > len(self._buffer) or size == 0:
            try: 
                self._buffer = np.append(self._buffer, np.transpose(self._frames.__next__().to_ndarray()), 0)
            except StopIteration as e:
                self.exhausted = True
                self._container.close()
                break
        if size > len(self._buffer):
            size = len(self._buffer)
        out = self._buffer[:size]
        self._buffer = self._buffer[size:]
        return out
