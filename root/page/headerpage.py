from .basepage import BasePage
import json
import string

HEADERPAGETYPE = 1
class HeaderPage(BasePage):

    def __init__(self, frame):
        super().__init__(frame)

    def init_header(self):
        super().initHeader()
        self.setPageType(HEADERPAGETYPE)
        self.setPageNo(self.frame.pageno)
        self.setR1(1)
        self.setR2(64)
        return self

    def getTables(self):
        return json.loads(self.getData())

    def addTable(self, table):
        tables = self.getTables()
        tables.append(table)
        data = json.dumps(table)
        if len(data) > self.getDataMax():
            return False
        else:
            self.setData(data)
            return True



class table():

    def __init__(self, name: string):
        super().__init__()
        self.name = name
        self.pages = []