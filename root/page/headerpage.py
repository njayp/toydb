from .basepage import BasePage
from ..globals import *
from ..buffer.frame import Frame
import json
import string

HEADERPAGETYPE = 1

class HeaderPage(BasePage):

    def __init__(self, frame):
        super().__init__(frame)

    def init_header(self):
        super().init_header()
        self.setPageType(HEADERPAGETYPE)
        self.setPageNo(self.frame.pageno)
        self.setDBSize(1)
        self.setDBCap(DISKSIZE)
        return self

    def getDBSize(self):
        return self.getR1()

    def setDBSize(self, size: int):
        return self.setR1(size)

    def getDBCap(self):
        return self.getR2()

    def setDBCap(self, size: int):
        return self.setR2(size)

class table():

    def __init__(self, name: string):
        super().__init__()
        self.name = name
        self.pages = []

'''
def createBlankHeader():
    frame = Frame(bytearray(PAGESIZE), 0, False, False)
    return HeaderPage(frame).init_header()
'''