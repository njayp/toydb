from .basepage import BasePage

DATAPAGETYPE = 3
class DataPage(BasePage):

    def __init__(self, frame):
        super().__init__(frame)

    def init_header(self):
        super().initHeader()
        self.setPageType(DATAPAGETYPE)
        self.setPageNo(self.frame.pageno)

    def getRecords(self):
        pass