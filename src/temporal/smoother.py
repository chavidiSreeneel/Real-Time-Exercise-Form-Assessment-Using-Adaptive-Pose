from collections import deque
import numpy as np

class TemporalSmoother:
    def __init__(self, window_size=5):
        self.window_size = window_size
        self.buffers = {}

    def smooth(self, key, value):
        if key not in self.buffers:
            self.buffers[key] = deque(maxlen=self.window_size)

        self.buffers[key].append(value)
        return float(np.mean(self.buffers[key]))

    def reset(self):
        self.buffers.clear()
