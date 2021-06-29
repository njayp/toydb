from ..globals import *
from ..buffer.buffer import Frame
import json


NEXTPAGESIZE = 3
NEXTPAGESTART = 0
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
        if (databytes := self.getDataBytes()) == bytearray(PAGESIZE - HEADERSIZE):
            # Header pages will never be empty
            return []

        while databytes[-1] == 0:
            databytes.pop()

        return json.loads(databytes)

    def trySetPageObj(self, obj):
        databytes = bytearray(json.dumps(obj), ENCODE)
        if len(databytes) > self.getDataMax():
            return False
        else:
            self.setDataBytes(databytes)
            return True


        