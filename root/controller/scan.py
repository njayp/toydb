from ..page.datapage import DataPage

class Scan():
    def __init__(self, heapfile, startpageno: int):
        super().__init__()
        self.heapfile = heapfile
        self.page = self.heapfile.getPage(startpageno, DataPage)
        self.stream = self.page.getPageObj()


    def getNext(self):

        if len(self.stream) == 0:
            if not self.getMoreRecords():
                return None
        return self.stream.pop(0)


    def getMoreRecords(self):
        if (nextpageno := self.page.getNextPage()) != 0:
            self.page.frame.pinned = False
            self.page = self.heapfile.getPage(nextpageno, DataPage)
            self.stream.extend(self.page.getPageObj())
            return True
        else:
            return False

    def close(self):
        self.page.frame.pinned = False
