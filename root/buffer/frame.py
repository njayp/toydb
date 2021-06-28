from ..globals import *

class FrameArray():

    def __init__(self):
        super().__init__()
        self.framearray = [Frame(bytearray(PAGESIZE))]*BUFFERSIZE

    def findFrame(self, pageno: int):
        for frame in self.framearray:
            if frame.pageno == pageno:
                return frame
        else:
            return None

class Frame():

    def __init__(self, rawbytes: bytearray, pageno:int=-1, pinned: bool=False, dirty: bool=False):
        super().__init__()
        self.dirty = dirty
        self.pinned = pinned
        self.pageno = pageno
        self.rawbytes = rawbytes
