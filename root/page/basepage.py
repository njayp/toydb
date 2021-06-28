from ..globals import *
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

    def __init__(self, pagetype: int=0, pageno: int=0, nextpage: int=0):
        super().__init__()
        self.rawbytes = bytearray(PAGESIZE)
        self.rawbytes[:PAGETYPESIZE] = pagetype.to_bytes(PAGETYPESIZE, ENOCDE)
        self.rawbytes[PAGETYPESIZE:PAGENOEND] = pageno.to_bytes(PAGENOSIZE, ENOCDE)
        self.rawbytes[NEXTPAGESTART:NEXTPAGEEND] = nextpage.to_bytes(DATAMAXSIZE, ENOCDE)
        self.rawbytes[DATAMAXSTART:DATAMAXEND] = DATAMAX.to_bytes(DATAMAXSIZE, ENOCDE)

    # for testing
    def setBytes(self, rawbytes):
        self.rawbytes = rawbytes
        return self
 
    def setData(self, rawbytes):
        self.rawbytes[HEADERSIZE:] = rawbytes

    def getPageType(self):
        return int.from_bytes(self.rawbytes[:PAGETYPESIZE], ENOCDE)

    def getPageNo(self):
        return int.from_bytes(self.rawbytes[PAGETYPESIZE:PAGENOEND], ENOCDE)

    def getDataMax(self):
        return int.from_bytes(self.rawbytes[DATAMAXSTART:DATAMAXEND], ENOCDE)

    def setNextPage(self, pageno: int):
        self.rawbytes[NEXTPAGESTART:NEXTPAGEEND] = pageno.to_bytes(DATAMAXSIZE, ENOCDE)

    def getNextPage(self):
        return int.from_bytes(self.rawbytes[NEXTPAGESTART:NEXTPAGEEND], ENOCDE)

    def getData(self):
        return self.rawbytes[HEADERSIZE:]

    def getBytes(self):
        return self.rawbytes

        