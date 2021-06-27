from .basepage import BasePage

class HeaderPage(BasePage):

    def __init__(self, rawbytes=None, pagetype=0, pageno=0):
        super().__init__(pagetype=pagetype, pageno=pageno)

    def getRecords(self):
        return super().getRecords()