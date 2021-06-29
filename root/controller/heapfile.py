import string
import json
from ..buffer.buffer import Buffer
from ..storage.disk import Disk
from ..page.headerpage import HeaderPage
from ..page.tablepage import TablePage
from ..page.datapage import DataPage
from .scan import Scan

import sys

HEADERPAGENO = 0

class HeapFile():

    def __init__(self, name: string):
        super().__init__()
        self.disk = Disk(name)
        self.buffer = Buffer(self.disk)
        self.headerpage = self.getPage(0, HeaderPage)
        if self.headerpage.getDBCap() == 0:
            self.headerpage.init_header()

    def getPage(self, pageno: int, pagetype):
        frame = self.buffer.requestFrame(pageno)
        #print(frame.pageno)
        return pagetype(frame)

    def addRecord(self, tablename: string, record: string):
        tabledict = self.headerpage.getPageObj()

        if tablename in tabledict.keys():
            tablepageno = tabledict[tablename]
            tablepage = self.getPage(tablepageno, TablePage)
        else:
            tablepageno = self.getNextEmptyPage()
            tabledict[tablename] = tablepageno

            # TODO handle full headerpage
            if not self.headerpage.trySetPageObj(tabledict):
                raise Exception("headerpage is full")

            tablepage = self.getPage(tablepageno, TablePage).init_header()

        pagearray = tablepage.getPageObj()
        if len(pagearray) == 0:
            newpageno = self.getNextEmptyPage()
            tablepage.trySetPageObj([newpageno])
            pageno = newpageno
            page = self.getPage(pageno, DataPage).init_header()
        else:
            pageno = pagearray[-1]
            page = self.getPage(pageno, DataPage)

        records = page.getPageObj()
        records.append(record)
        if not page.trySetPageObj(records):
            newpageno = self.getNextEmptyPage()
            page.setNextPage(newpageno)
            pagearray.append(newpageno)

            # TODO handle full tablepage
            if not tablepage.trySetPageObj(pagearray):
                raise Exception("tablepage is full")
                
            newpage = self.getPage(newpageno, DataPage).init_header()
            newpage.trySetPageObj([record])
            newpage.frame.pinned = False

        tablepage.frame.pinned = False
        page.frame.pinned = False

    def findFirstPageOfTable(self, tablename: string):
        tabledict = self.headerpage.getPageObj()

        if tablename in tabledict.keys():
            tablepageno = tabledict[tablename]
            tablepage = self.getPage(tablepageno, TablePage)
            firstpageno = tablepage.getPageObj()[0]
            tablepage.frame.pinned = False
            return firstpageno

        else:
            return None

    def searchTableForRecord(self, tablename: string, target: string):
        if (firstpageno := self.findFirstPageOfTable(tablename)) != None:
            scan = Scan(self, firstpageno)
            while (record := scan.getNext()) != None:
                if record == target:
                    return True
            
        return False

    def readTable(self, tablename: string, filestream=sys.stdout):
        if (firstpageno := self.findFirstPageOfTable(tablename)) != None:
            scan = Scan(self, firstpageno)
            while (record := scan.getNext()) != None:
                filestream.write(record)
                filestream.write('\n')
            
            filestream.flush()
            scan.close()

    def getNextEmptyPage(self):
        dbsize = self.headerpage.getDBSize()

        if dbsize == self.headerpage.getDBCap():
            self.disk.setSize(dbsize * 2)

        self.headerpage.setDBSize(dbsize + 1)
        return dbsize


    def close(self):
        self.buffer.close()
        self.disk.close()
