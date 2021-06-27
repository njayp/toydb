from ..globals import *
import json

PAGETYPESIZE = 1 # bytes

PAGENOSIZE = 3
PAGENOSTART = PAGETYPESIZE
PAGENOEND = PAGETYPESIZE + PAGENOSIZE

HEADERSIZE = PAGENOEND

class BasePage():

    def __init__(self, pagetype: int=0, pageno: int=0):
        super().__init__()
        self.rawbytes = bytearray(PAGESIZE)
        self.rawbytes[:PAGETYPESIZE] = pagetype.to_bytes(PAGETYPESIZE, 'big')
        self.rawbytes[PAGETYPESIZE:PAGENOEND] = pageno.to_bytes(PAGENOSIZE, 'big')

    def loadBytes(self, rawbytes):
        self.rawbytes = rawbytes
        return self

    def getPageType(self):
        return int.from_bytes(self.rawbytes[:PAGETYPESIZE], 'big')

    def getPageNo(self):
        return int.from_bytes(self.rawbytes[PAGETYPESIZE:PAGENOEND], 'big')

    def getRecords(self):
        return self.rawbytes[HEADERSIZE:]

    def getBytes(self):
        return self.rawbytes

        