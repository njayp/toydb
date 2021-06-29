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
        self.setDBSize(1)
        self.setDBCap(DISKSIZE)
        self.trySetPageObj({})
        return self

    def getDBSize(self):
        return self.getR1()

    def setDBSize(self, size: int):
        return self.setR1(size)

    def getDBCap(self):
        return self.getR2()

    def setDBCap(self, size: int):
        return self.setR2(size)
