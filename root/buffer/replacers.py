from ..globals import *

class SequencialReplacer():

    def __init__(self):
        super().__init__()
        self.frames = range(BUFFERSIZE)

    def chooseEvicted(self):
        chosen = self.frames.pop(0)
        self.frames.append(chosen)
        return chosen