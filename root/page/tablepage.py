from .basepage import BasePage


TABLEPAGETYPE = 2

class TablePage(BasePage):

    def __init__(self, frame):
        super().__init__(frame)

    def init_header(self):
        super().init_header()
        self.setPageType(TABLEPAGETYPE)
        self.setPageNo(self.frame.pageno)
        return self

