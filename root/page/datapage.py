from .basepage import BasePage

DATAPAGETYPE = 3
class DataPage(BasePage):

    def __init__(self, frame):
        super().__init__(frame)

    def init_header(self):
        super().init_header()
        self.setPageType(DATAPAGETYPE)
        self.setPageNo(self.frame.pageno)
        return self
