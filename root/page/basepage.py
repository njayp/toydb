from ..globals import *
from ..buffer.buffer import Frame
import json

PAGETYPESIZE = 1 # bytes

PAGENOSIZE = 3
PAGENOSTART = PAGETYPESIZE
PAGENOEND = PAGETYPESIZE + PAGENOSIZE

NEXTPAGESIZE = 3
NEXTPAGESTART = PAGENOEND
NEXTPAGEEND = NEXTPAGESTART + NEXTPAGESIZE

DATAMAXSIZE = 4
DATAMAXSTART = NEXTPAGEEND
DATAMAXEND = DATAMAXSTART + DATAMAXSIZE

HEADERSIZE = DATAMAXEND

#####

DATAMAX = PAGESIZE - HEADERSIZE
ENOCDE = 'big'

class BasePage():

    def __init__(self, frame: Frame):
        super().__init__()
        self.frame = frame
 
    def setData(self, rawbytes):
        self.frame.rawbytes[HEADERSIZE:] = rawbytes

    def getPageType(self):
        return int.from_bytes(self.frame.rawbytes[:PAGETYPESIZE], ENOCDE)

    def getPageNo(self):
        return int.from_bytes(self.frame.rawbytes[PAGETYPESIZE:PAGENOEND], ENOCDE)

    def getDataMax(self):
        return int.from_bytes(self.frame.rawbytes[DATAMAXSTART:DATAMAXEND], ENOCDE)

    def setNextPage(self, pageno: int):
        self.frame.rawbytes[NEXTPAGESTART:NEXTPAGEEND] = pageno.to_bytes(DATAMAXSIZE, ENOCDE)

    def getNextPage(self):
        return int.from_bytes(self.frame.rawbytes[NEXTPAGESTART:NEXTPAGEEND], ENOCDE)

    def getData(self):
        return self.frame.rawbytes[HEADERSIZE:]

    def getBytes(self):
        return self.frame.rawbytes

        