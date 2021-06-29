import string
import json
from ..buffer.buffer import Buffer
from ..storage.disk import Disk
from ..page.headerpage import HeaderPage
from ..page.datapage import DataPage
from ..globals import *
from types import SimpleNamespace

HEADERPAGENO = 0

class HeapFile():

    def __init__(self, name: string):
        super().__init__()
        self.disk = Disk(name)
        self.buffer = Buffer(disk)

    def addRecord(self, tablename: string, record: string):
        headerpage, tables = self.getTables()

        if tablename in tables.keys():
            pageno = tables[tablename][-1]

        else:
            pageno = self.addTable(tablename)

        self.addRecordToPage(pageno)

    def addRecordToPage(self, pageno: int):
        pass

    def getReadTable(self):
        pass

    def addPageToTable(self, table: string, pageno: int):
        headerpage, tables = self.getTables()

        if table in tables.keys():
            tables[table].append(pageno)

        else:
            table[table] = [pageno]

        data = json.dumps(tables)
        headerpage.setData(data)
        self.buffer.writeFrame(headerpage.frame)
        return pageno

    def scanFromStartPage(self, startpage: int):
        page, recordlist = self.getPageData(startpage, DataPage)
        page.frame.pinned = False
        while (nextpage := page.getNextPage()) != 0:
            page, nextlist = getPageData(nextpage, DataPage)
            recordlist.extend(nextlist)
            page.frame.pinned = False

        return recordlist


    def getPageData(self, pageno: int, pagetype):
        frame = self.buffer.requestFrame(pageno, True)
        page = pagetype(frame)
        tables = json.loads(page.getData())
        return (page, tables)

    def writePage(self, page):
        pass

    def getTables(self):
        pass

    def getTablePages(self):
        pass

    def appendRecord(self):
        pass

    def addDataPage(self):
        pass

    def addTablePage(self):
        pass

    def addHeaderPage(self):
        pass

    def close(self):
        self.buffer.close()
        self.disk.close()
