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

HEADERSIZE = R2END

#####

DATAMAX = PAGESIZE - HEADERSIZE
ENDIAN = 'big'
ENCODE = 'utf-8'


class BasePage():

    def __init__(self, frame: Frame):
        super().__init__()
        self.frame = frame

    def init_header(self):
        self.setDataMax(DATAMAX)
        return self

    def getDataBytes(self):
        return self.frame.rawbytes[HEADERSIZE:]
 
    def setDataBytes(self, rawbytes: bytearray):
        self.frame.dirty = True
        self.frame.rawbytes[HEADERSIZE:] = rawbytes

    def getHeaderAttr(self, start: int, end: int):
        return int.from_bytes(self.frame.rawbytes[start:end], ENDIAN)

    def setHeaderAttr(self, start: int, end: int, data: int, size: int):
        self.frame.dirty = True
        self.frame.rawbytes[start:end] = data.to_bytes(size, ENDIAN)

    def getPageType(self):
        return self.getHeaderAttr(PAGETYPESTART, PAGETYPEEND)

    def setPageType(self, pagetype: int):
        self.setHeaderAttr(PAGETYPESTART, PAGETYPEEND, pagetype, PAGETYPESIZE)

    def getPageNo(self):
        return self.getHeaderAttr(PAGENOSTART, PAGENOEND)

    def setPageNo(self, pageno: int):
        self.setHeaderAttr(PAGENOSTART, PAGENOEND, pageno, PAGENOSIZE)

    def getR1(self):
        return self.getHeaderAttr(R1START, R1END)

    def setR1(self, pageno: int):
        self.setHeaderAttr(R1START, R1END, pageno, R1SIZE)

    def getR2(self):
        return self.getHeaderAttr(R2START, R2END)

    def setR2(self, pageno: int):
        self.setHeaderAttr(R2START, R2END, pageno, R2SIZE)

    def getDataMax(self):
        return self.getHeaderAttr(DATAMAXSTART, DATAMAXEND)

    def setDataMax(self, nobytes: int):
        self.setHeaderAttr(DATAMAXSTART, DATAMAXEND, nobytes, DATAMAXSIZE)

    def getNextPage(self):
        return self.getHeaderAttr(NEXTPAGESTART, NEXTPAGEEND)

    def setNextPage(self, pageno: int):
        self.setHeaderAttr(NEXTPAGESTART, NEXTPAGEEND, pageno, DATAMAXSIZE)

    def getPageObj(self):
        return json.loads(self.getDataBytes())

    def trySetPageObj(self, page, obj):
        rawbytes = bytearray(json.dumps(obj), ENCODE)
        if len(rawbytes) > self.getDataMax():
            return False
        else:
            self.setDataBytes(rawbytes)
            return True


        