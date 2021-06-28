from ..globals import *
from .frame import (FrameArray, Frame)



class SequencialReplacer(FrameArray):

    def __init__(self):
        super().__init__()

    def replacer(self, rawbytes: bytearray, pageno: int, pinned: bool=False, dirty: bool=False):
        # TODO replace with for-else that throws exception
        while (chosen := self.framearray.pop(0)).pinned:
            self.framearray.append(chosen)
        
        self.framearray.append(Frame(rawbytes, pageno, pinned, dirty))
        return chosen
        