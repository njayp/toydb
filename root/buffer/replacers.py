from ..globals import *
from .frame import (FrameArray, Frame)



class SequentialReplacer(FrameArray):

    def __init__(self):
        super().__init__()


    def replacer(self, frame: Frame):
        for i in range(BUFFERSIZE):
            if not (chosen := self.framearray.pop(0)).pinned:
                break
            else:
                self.framearray.append(chosen)

        else:
            raise Exception("All buffer frames pinned")
        
        self.framearray.append(frame)
        return chosen


class FIFOReplacer(FrameArray):

    def __init__(self):
        super().__init__()

    def replacer(self, frame: Frame):
        pass