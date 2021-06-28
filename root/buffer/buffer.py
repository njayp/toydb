from ..globals import *
from .replacers import SequentialReplacer
from .frame import (FrameArray, Frame)
from ..storage.disk import Disk

class Buffer():

    def __init__(self, disk: Disk, manager=SequentialReplacer):
        super().__init__()
        self.manager = manager()
        self.disk = disk

    def requestFrame(self, pageno: int, pinned: bool=False):
        if (frame := self.manager.findFrame(pageno)) != None:
            frame.pinned = pinned
            return frame
        else:
            return self.loadBytes(pageno, pinned)

    def loadBytes(self, pageno: int, pinned: bool=False):
        rawbytes = self.disk.readBytes(pageno)
        frame = Frame(rawbytes, pageno, pinned, False)
        replacedframe = self.manager.replacer(frame)
        self.evict(replacedframe)
        return frame

    def setPageBytes(self, rawbytes: bytearray, pageno: int, pinned: bool=False):
        if (frame := self.manager.findFrame(pageno)) != None:
            frame.dirty = True
            frame.pinned = pinned
            frame.rawbytes = rawbytes
        else:
            frame = Frame(rawbytes, pageno, pinned, True)
            self.createPage(frame)

    def createPage(self, frame: Frame):
        replacedframe = self.manager.replacer(frame)
        self.evict(replacedframe)

    def evict(self, frame: Frame):
        if frame.dirty:
            #print(frame.pageno, frame.rawbytes)
            self.disk.writeBytes(frame.pageno, frame.rawbytes)

    def flush(self):
        for frame in self.manager.framearray:
            self.evict(frame)

    def close(self):
        self.flush()

