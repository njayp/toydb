from ..page.basepage import BasePage
from ..globals import *

class FDA():

    def __init__(self):
        super().__init__()
        self.fda = [FrameData(i) for i in range(BUFFERSIZE)]

    def setDirty(self, frameno: int, dirty: bool):
        self.fda[self.findFrameDataIndex(frameno)].dirty = dirty

    def setPinned(self, frameno: int, pinned: bool):
        self.fda[self.findFrameDataIndex(frameno)].pinned = pinned

    def getDirty(self, frameno: int):
        return self.fda[self.findFrameDataIndex(frameno)].dirty

    def getPinned(self, frameno: int):
        return self.fda[self.findFrameDataIndex(frameno)].pinned

    def getDirty(self, frameno: int):
        return self.fda[self.findFrameDataIndex(frameno)].dirty

    def getPinned(self, frameno: int):
        return self.fda[self.findFrameDataIndex(frameno)].pinned

    def findFrameNo(self, pageno: int):
        for fd in self.fda:
            if fd.pageno == pageno:
                return fd.frameno
        else:
            return None

    def findFrameDataIndex(self, frameno: int):
        for i, fd in enumerate(self.fda):
            if fd.frameno == frameno:
                return i
        else:
            return None # throw ex?

    def replaceFrameData(self, frameno: int, pageno:int=-1, pinned: bool=False, dirty: bool=False):
        self.fda[self.findFrameDataIndex(frameno)] = FrameData(frameno, pageno, pinned, dirty)



class FrameData():

    def __init__(self, frameno: int, pageno:int=-1, pinned: bool=False, dirty: bool=False):
        super().__init__()
        self.dirty = dirty
        self.pinned = pinned
        self.pageno = pageno
        self.frameno = frameno

