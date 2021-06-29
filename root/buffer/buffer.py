from ..globals import *
from .replacers import sequentialReplaceWith
from .frame import Frame
from ..storage.disk import Disk

class Buffer():

    def __init__(self, disk: Disk, replacewith=sequentialReplaceWith):
        super().__init__()
        self.replacewith = replacewith
        self.disk = disk
        self.framearray = [Frame(bytearray(PAGESIZE), -1, False, False)]*BUFFERSIZE
        self.pagereads = 0
        self.diskreads = 0
        self.diskwrites = 0

    def requestFrame(self, pageno: int):
        self.pagereads += 1

        if (frame := self.findFrame(pageno)) != None:
            frame.pinned = True
            return frame
        else:
            self.diskreads += 1
            rawbytes = self.disk.readBytes(pageno)
            frame = Frame(rawbytes, pageno, True, False)
            replacedframe = self.replacewith(frame, self.framearray)
            self.evict(replacedframe)
            return frame

    def findFrame(self, pageno: int):
        for frame in self.framearray:
            if frame.pageno == pageno:
                return frame
        else:
            return None

    def evict(self, frame: Frame):
        if frame.dirty:
            #print(frame.pageno, frame.rawbytes)
            self.diskwrites += 1
            self.disk.writeBytes(frame.pageno, frame.rawbytes)

    def flush(self):
        for frame in self.framearray:
            self.evict(frame)

    def close(self):
        self.flush()

