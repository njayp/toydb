from ..globals import *
import json

'''
class Header():

    def __init__(self, headerbytes):
        super().__init__()
        self.headerbytes = headerbytes

    def __init__(self, pagetype, pageno):
        super().__init__()
        self.headerbytes = bytearray([pagetype, pageno])

    def getPageType(self):
        return self.headerbytes[:1]

    def getPageNo(self):
        return self.headerbytes[1:2]

    def printSelf(self):
        print(self.headerbytes)
'''

PAGETYPESIZE = 1 # byte
PAGENOSIZE = 3 # bytes


class BasePage():

    def __init__(self, rawbytes: bytearray):
        super().__init__()
        self.rawbytes = rawbytes

    def __init__(self, pagetype: int, pageno: int):
        super().__init__()
        self.rawbytes = bytearray(PAGESIZE)
        self.rawbytes[:PAGETYPESIZE] = pagetype.to_bytes(PAGETYPESIZE, 'big')
        self.rawbytes[PAGETYPESIZE:PAGETYPESIZE + PAGENOSIZE] = pageno.to_bytes(PAGENOSIZE, 'big')


    def getPageType(self):
        return int.from_bytes(self.rawbytes[:PAGETYPESIZE], 'big')

    def getPageNo(self):
        return int.from_bytes(self.rawbytes[PAGETYPESIZE:PAGETYPESIZE + PAGENOSIZE], 'big')

    def getRecords(self):
        return self.rawbytes[HEADERSIZE:]

    def addRecord(self, record):
        self.recordbytes.append(record)

    def getBytes(self):
        return self.rawbytes

        