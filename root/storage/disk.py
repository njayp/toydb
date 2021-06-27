import mmap
from ..globals import *
import os

class Disk():
    
    def __init__(self, filename='disk.toydb'):
        super().__init__()

        # mmap an empty file throws error
        if os.path.exists(filename):
            self.f = open(filename, "r+b")
        else:
            self.f = open(filename, "a+b")
            self.f.write(bytearray(PAGESIZE*10)) # TODO replace w/ database header
            self.f.flush()

        self.disk = mmap.mmap(self.f.fileno(), 0)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def close(self):
        self.disk.close()
        self.f.close()

    def pagenoToByteAddr(self, pageno: int):
        start = pageno * PAGESIZE
        return (start, start + PAGESIZE)
        
    def readPage(self, pageno):
        start, stop = self.pagenoToByteAddr(pageno)
        return self.disk[start:stop]

    def writePage(self, pageno, data):
        start, stop = self.pagenoToByteAddr(pageno)
        self.disk[start:stop] = data
        #self.disk.flush()

    def setSize(self, newnopages):
        self.disk.resize(PAGESIZE * newnopages)
        #self.disk.flush()