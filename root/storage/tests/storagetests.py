from ..storage import Storage
from ...globals import *
import unittest
import os

class StorageTests(unittest.TestCase):
    def setUp(self):
        self.filename = 'storagetest.toydb'
        self.disk = Storage(self.filename)
        self.ba = PAGESIZE*b'\1'

    def tearDown(self):
        self.disk.close()
        os.remove(self.filename)

    def test_readwrite(self):
        self.disk.writePage(0, self.ba)
        self.assertEqual(self.ba, self.disk.readPage(0))

    def test_closeopen(self):
        self.disk.writePage(0, self.ba)
        self.disk.close()
        self.disk = Storage(self.filename)
        self.assertEqual(self.ba, self.disk.readPage(0))

    def test_setSize(self):
        self.disk.setSize(1)
        self.disk.writePage(5, self.ba)
        self.assertEqual(self.ba, self.disk.readPage(5))

    def test_pagenoToByteAddr(self):
        self.assertEqual((0, PAGESIZE), self.disk.pagenoToByteAddr(0))
        self.assertEqual((PAGESIZE * 5, PAGESIZE * 6), self.disk.pagenoToByteAddr(5))


    

    