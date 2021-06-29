from .basepage import BasePage

DATAPAGETYPE = 3
class DataPage(BasePage):

    def __init__(self, frame):
        super().__init__(frame)

    def init_header(self):
        super().init_header()
        return self
