from ..heapfile import HeapFile
from ...page.datapage import DataPage
import os
import unittest
import io


def listToStreamOutput(records):
    s = ''
    for record in records:
        s += record
        s += '\n'
    return s


class HeapFileTests(unittest.TestCase):
    def setUp(self):
        self.filename = 'heapfiletest.toydb'      
        self.hf = HeapFile(self.filename)

    def tearDown(self):
        self.hf.close()
        os.remove(self.filename)

    def test_readWrite(self):
        tablename = 'movie'
        records = ['rambo', 'iron man', 'silence of the lambs']

        a = listToStreamOutput(records)

        for record in records:
            self.hf.addRecord(tablename, record)

        io1 = io.StringIO()
        self.hf.readTable(tablename, io1)
        self.assertEqual(io1.getvalue(), a)

    def test_twoTables(self):
        table1 = 'movie'
        table2 = 'book'
        records1 = ['rambo', 'iron man', 'silence of the lambs', 'ghostbusters']
        records2 = ['mistborn', 'dune', '1984', 'all quiet on the western front']
        
        a1 = listToStreamOutput(records1)
        a2 = listToStreamOutput(records2)

        for r1, r2 in zip(records1, records2):
            self.hf.addRecord(table1, r1)
            self.hf.addRecord(table2, r2)
            
        io1 = io.StringIO()
        io2 = io.StringIO()
        self.hf.readTable(table1, io1)
        self.hf.readTable(table2, io2)
        self.assertEqual(io1.getvalue(), a1)
        self.assertEqual(io2.getvalue(), a2)
        
        
    def test_pageSpilt(self):
        tablename = 'seagull'
        records = ['mine']*10000
        a = listToStreamOutput(records)

        for record in records:
            self.hf.addRecord(tablename, record)

        #print(self.hf.getPage(2, DataPage))

        io1 = io.StringIO()
        self.hf.readTable(tablename, io1)
        self.assertEqual(io1.getvalue(), a)


    def test_search(self):
        tablename = 'movie'
        records = ['rambo', 'iron man', 'silence of the lambs']

        a = listToStreamOutput(records)

        for record in records:
            self.hf.addRecord(tablename, record)

        self.assertEqual(self.hf.searchTableForRecord(tablename, records[1]), True)
        self.assertEqual(self.hf.searchTableForRecord(tablename, 'star wars'), False)

    def test_writeFlushRead(self):
        tablename = 'movie'
        records = ['rambo', 'iron man', 'silence of the lambs']

        a = listToStreamOutput(records)

        for record in records:
            self.hf.addRecord(tablename, record)

        for i in range(50, 100):
            self.hf.getPage(i, DataPage).frame.pinned = False

        io1 = io.StringIO()
        self.hf.readTable(tablename, io1)
        self.assertEqual(io1.getvalue(), a)

    def test_closeOpen(self):
        tablename = 'movie'
        records = ['rambo', 'iron man', 'silence of the lambs']
        a = listToStreamOutput(records)

        for record in records:
            self.hf.addRecord(tablename, record)

        self.hf.close()
        self.hf = HeapFile(self.filename)

        io1 = io.StringIO()
        self.hf.readTable(tablename, io1)
        self.assertEqual(io1.getvalue(), a)