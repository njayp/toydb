from ..globals import *
from .replacers import SequentialReplacer
from .frame import Frame
from ..storage.disk import Disk

class Buffer():

    def __init__(self, disk: Disk, manager=SequentialReplacer):
        super().__init__()
        self.manager = manager()
        self.disk = disk

    def requestFrame(self, pageno: int):
        if (frame := self.manager.findFrame(pageno)) != None:
            frame.pinned = True
            return frame
        else:
            rawbytes = self.disk.readBytes(pageno)
            frame = Frame(rawbytes, pageno, True, False)
            replacedframe = self.manager.replacer(frame)
            self.evict(replacedframe)
            return frame

    def returnFrame(self, frame: Frame):
        frame.dirty = True
        if self.manager.findFrame(frame.pageno) == None:
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

