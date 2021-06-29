import mmap
from ..globals import *
import os
#from ..page.headerpage import createBlankHeader

class Disk():
    
    def __init__(self, filename='disk.toydb'):
        super().__init__()

        # mmap an empty file throws error
        if os.path.exists(filename):
            self.f = open(filename, "r+b")
        else:
            self.f = open(filename, "a+b")
            #self.f.write(createBlankHeader().frame.rawbytes)
            self.f.write(bytearray((PAGESIZE)*DISKSIZE))
            self.f.flush()

        self.disk = mmap.mmap(self.f.fileno(), 0)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def close(self):
        self.disk.close()
        self.f.close()
        
    def readBytes(self, pageno):
        start = pageno * PAGESIZE
        return bytearray(self.disk[start:start + PAGESIZE])

    def writeBytes(self, pageno, data):
        start = pageno * PAGESIZE
        size = len(data)
        self.disk[start:start + size] = data
        #self.disk.flush()

    def setSize(self, nopages):
        self.disk.resize(PAGESIZE * nopages)
        #self.disk.flush()