from ..globals import *
from ..buffer.buffer import Frame
import json

PAGETYPESIZE = 1 # bytes
PAGETYPESTART = 0
PAGETYPEEND = PAGETYPESIZE + PAGETYPESTART

PAGENOSIZE = 3
PAGENOSTART = PAGETYPESIZE
PAGENOEND = PAGETYPESIZE + PAGENOSIZE

NEXTPAGESIZE = 3
NEXTPAGESTART = PAGENOEND
NEXTPAGEEND = NEXTPAGESTART + NEXTPAGESIZE

DATAMAXSIZE = 3
DATAMAXSTART = NEXTPAGEEND
DATAMAXEND = DATAMAXSTART + DATAMAXSIZE

R1SIZE = 3
R1START = DATAMAXEND
R1END = R1START + R1SIZE

R2SIZE = 3
R2START = R1END
R2END = R2START + R2SIZE

HEADERSIZE = DATAMAXEND + RESERVED

#####

DATAMAX = PAGESIZE - HEADERSIZE
ENOCDE = 'big'

class BasePage():

    def __init__(self, frame: Frame):
        super().__init__()
        self.frame = frame

    def initHeader(self):
        self.setDataMax(DATAMAX)
        return self

    def getData(self):
        return self.frame.rawbytes[HEADERSIZE:]
 
    def setData(self, rawbytes: bytearray):
        self.frame.rawbytes[HEADERSIZE:] = rawbytes

    def getPageType(self):
        return int.from_bytes(self.frame.rawbytes[PAGETYPESTART:PAGETYPEEND], ENOCDE)

    def setPageType(self, pagetype: int):
        self.frame.rawbytes[PAGETYPESTART:PAGETYPEEND] = pagetype.to_bytes(PAGETYPESIZE, ENOCDE)

    def getPageNo(self):
        return int.from_bytes(self.frame.rawbytes[PAGENOSTART:PAGENOEND], ENOCDE)

    def setPageNo(self, pageno: int):
        self.frame.rawbytes[PAGENOSTART:PAGENOEND] = pageno.to_bytes(PAGENOSIZE, ENOCDE)

    def getR1(self):
        return int.from_bytes(self.frame.rawbytes[R1START:R1END], ENOCDE)

    def setR1(self, pageno: int):
        self.frame.rawbytes[R1START:R1END] = pageno.to_bytes(R1SIZE, ENOCDE)

    def getR2(self):
        return int.from_bytes(self.frame.rawbytes[R2START:R2END], ENOCDE)

    def setR2(self, pageno: int):
        self.frame.rawbytes[R2START:R2END] = pageno.to_bytes(R2SIZE, ENOCDE)

    def getDataMax(self):
        return int.from_bytes(self.frame.rawbytes[DATAMAXSTART:DATAMAXEND], ENOCDE)

    def setDataMax(self, nobytes: int):
        self.frame.rawbytes[DATAMAXSTART:DATAMAXEND] = nobytes.to_bytes(DATAMAXSIZE, ENOCDE)

    def getNextPage(self):
        return int.from_bytes(self.frame.rawbytes[NEXTPAGESTART:NEXTPAGEEND], ENOCDE)

    def setNextPage(self, pageno: int):
        self.frame.rawbytes[NEXTPAGESTART:NEXTPAGEEND] = pageno.to_bytes(DATAMAXSIZE, ENOCDE)

        