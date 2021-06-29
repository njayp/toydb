import string
import json
from ..buffer.buffer import Buffer
from ..storage.disk import Disk
from ..page.headerpage import HeaderPage
from ..page.tablepage import TablePage
from ..page.datapage import DataPage
from types import SimpleNamespace

HEADERPAGENO = 0

class HeapFile():

    def __init__(self, name: string):
        super().__init__()
        self.disk = Disk(name)
        self.buffer = Buffer(disk)
        self.headerpage = self.getPage(0, HeaderPage)
        if self.headerpage.getPageType() == 0:
            self.headerpage.init_header()

    def getPage(self, pageno: int, pagetype):
        frame = self.buffer.requestFrame(pageno)
        return pagetype(frame)

    def addRecord(self, tablename: string, record: string):
        tabledict = self.headerpage.getPageObj()

        if tablename in tabledict.keys():
            tablepageno = tabledict[tablename]
            tablepage = self.getPage(tablepageno)
        else:
            tablepageno = self.getNextEmptyPage()
            tabledict[tablename] = tablepageno
            # TODO handle full headerpage
            self.headerpage.trySetPageObj(tabledict)
            tablepage = self.getPage(tablepageno, TablePage).init_header()

        pagearray = tablepage.getPageObj()
        pageno = pagearray[-1]
        page = self.getPage(pageno)
        records = page.getPageObj(page)
        records.append(record)
        if not page.trySetPageObj(records):
            newpageno = self.getNextEmptyPage()
            page.setNextPage(newpageno)
            pagearray.append(newpageno)
            tablepage.trySetPageObj(pagearray)
            # TODO handle full tablepage
            newpage = self.getPage(newpageno, DataPage).init_header()
            newpage.trySetPageObj([record])
            newpage.frame.pinned = False

        tablepage.frame.pinned = False
        page.frame.pinned = False

    def readTable(self, tablename: string):
        tabledict = self.headerpage.getPageObj()

        if tablename in tabledict.keys():
            tablepageno = tabledict[tablename]
            tablepage = self.getPage(tablepageno)
            firstpageno = tablepage.getPageObj()[0]
            return self.scanRecords(firstpageno)
        else:
            return []


    def scanRecords(self, startpageno: int):
        
        page = self.getPage(startpageno)
        records = page.getPageObj()
        page.frame.pinned = False

        while (nextpageno := page.getNextPage()) != 0:
            page = self.getPage(nextpageno)
            records.append(page.getPageObj())
            page.frame.pinned = False

        return records
            

    def getNextEmptyPage(self):
        dbsize = self.headerpage.getDBSize()

        if dbsize == self.headerpage.getDBCap():
            raise Exception("Disk is full")

        self.headerpage.setDBSize(dbsize + 1)
        return dbsize


    def close(self):
        self.buffer.close()
        self.disk.close()
