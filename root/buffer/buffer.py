from ..globals import *
from .replacers import SequencialReplacer
from .frame import Frame
from ..storage.disk import Disk
from ..page.basepage import BasePage

class Buffer():

    def __init__(self, disk: Disk, replacer=SequencialReplacer()):
        super().__init__()
        self.replacer = replacer
        self.frames = {i:Frame() for i in range(BUFFERSIZE)}
        self.disk = disk

    def loadPage(self, pageno: int):
        while  self.frames[(frameno := self.replacer.chooseEvicted())].pinned:
            pass

        evicted = self.frames[frameno]

        if evicted.dirty:
            Disk.writePage(evicted.page.getPageNo(), evicted.page.getBytes())

        self.frames[frameno] = Frame(BasePage(self.disk.readPage(pageno)))
