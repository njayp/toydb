from .basepage import BasePage
import json

TABLEPAGETYPE = 2

class TablePage(BasePage):

    def __init__(self, frame):
        super().__init__(frame)

    def init_header(self):
        super().initHeader()
        self.setPageType(TABLEPAGETYPE)
        self.setPageNo(self.frame.pageno)

    def getRecords(self):
        pass