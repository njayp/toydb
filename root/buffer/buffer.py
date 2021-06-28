from ..globals import *
from .replacers import SequencialReplacer
from .frame import (FrameArray, Frame)
from ..storage.disk import Disk
from ..page.basepage import BasePage

class Buffer():

    def __init__(self, disk: Disk, manager=SequencialReplacer):
        super().__init__()
        self.manager = manager()
        self.disk = disk

    def requestPageBytes(self, pageno: int, pinned: bool=False):
        if (frame := self.manager.findFrame(pageno)) != None:
            frame.pinned = pinned
            return frame.rawbytes
        else:
            return self.loadPage(pageno, pinned)

    def loadPage(self, pageno: int, pinned: bool=False):
        rawbytes = self.disk.readPage(pageno)
        self.evict(self.manager.replacer(rawbytes, pageno, pinned, False))
        return rawbytes

    def createPage(self, rawbytes: bytearray, pageno: int, pinned: bool=False):
        self.evict(self.manager.replacer(rawbytes, pageno, pinned, True))

    def setPageBytes(self, rawbytes: bytearray, pageno: int, pinned: bool=False):
        if (frame := self.manager.findFrame(pageno)) != None:
            frame.setDirty(True)
            frame.setRawBytes(rawbytes)
        else:
            frameno = self.createPage(rawbytes, pageno, pinned, True)

    def evict(self, frame: Frame):
        if frame.dirty:
            #print(frame.pageno, frame.rawbytes)
            self.disk.writePage(frame.pageno, frame.rawbytes)

    def flush(self):
        for frame in self.manager.framearray:
            self.evict(frame)

    def close(self):
        self.flush()

