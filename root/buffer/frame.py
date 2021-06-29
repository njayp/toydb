from ..globals import *

class Frame():

    def __init__(self, rawbytes: bytearray, pageno:int, pinned: bool, dirty: bool):
        super().__init__()
        self.dirty = dirty
        self.pinned = pinned
        self.pageno = pageno
        self.rawbytes = rawbytes
