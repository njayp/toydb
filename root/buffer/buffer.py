from ..globals import *
from .replacers import SequencialReplacer
from ..storage.disk import Disk
from ..page.basepage import BasePage

class Buffer():

    def __init__(self, disk: Disk, replacer=SequencialReplacer):
        super().__init__()
        self.replacer = replacer()
        self.frames = [bytearray(PAGESIZE) for i in range(BUFFERSIZE)]
        self.disk = disk

    def requestPageBytes(self, pageno: int, pinned: bool=False):
        if (frameno := self.replacer.findFrameNo(pageno)):
            self.replacer.setPinned(frameno, pinned)
            return self.frames[frameno]
        else:
            frameno = self.loadPage(pageno, pinned)
            return self.frames[frameno]

    def loadPage(self, pageno: int, pinned: bool=False):
        frameno = self.chooseAndEvict(pageno)
        self.frames[frameno] = self.disk.readPage(pageno)
        self.replacer.replaceFrameData(frameno, pageno, pinned)
        return frameno

    def createPage(self, rawbytes: bytearray, pageno: int, pinned: bool=False):
        frameno = self.chooseAndEvict(pageno)
        self.frames[frameno] = rawbytes
        self.replacer.replaceFrameData(frameno, pageno, pinned)
        return frameno

    def setPage(self, rawbytes: bytearray, pageno: int):
        frameno = self.replacer.findFrameNo(pageno)
        self.frames[frameno] = rawbytes
        self.replacer.setDirty(frameno, True)


    def chooseAndEvict(self, pageno: int):
        frameno = self.replacer.chooseEvicted()
        self.evict(frameno, pageno)       
        return frameno

    def evict(self, frameno: int, pageno: int):
        if self.replacer.getDirty(frameno):
            self.disk.writePage(pageno, self.frames[frameno])

    def flush(self):
        for fd in self.replacer.fda:
            self.evict(fd.frameno, fd.pageno)

