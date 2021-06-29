from ..disk import Disk
from ...globals import *
import unittest
import os

class StorageTests(unittest.TestCase):
    def setUp(self):
        self.filename = 'storagetest.toydb'
        self.disk = Disk(self.filename)
        self.ba = PAGESIZE*b'\1'

    def tearDown(self):
        self.disk.close()
        os.remove(self.filename)

    def test_readwrite(self):
        pageno = 3
        self.disk.writeBytes(pageno, self.ba)
        self.assertEqual(self.ba, self.disk.readBytes(pageno))

    def test_closeopen(self):
        pageno = 10
        self.disk.writeBytes(pageno, self.ba)
        self.disk.close()
        self.disk = Disk(self.filename)
        self.assertEqual(self.ba, self.disk.readBytes(pageno))

    def test_setSize(self):
        pageno = 99
        self.disk.setSize(100)
        self.disk.writeBytes(99, self.ba)
        self.assertEqual(self.ba, self.disk.readBytes(99))

    def test_pagenoToByteAddr(self):
        self.assertEqual((0, PAGESIZE), self.disk.pagenoToByteAddr(0))
        self.assertEqual((PAGESIZE * 5, PAGESIZE * 6), self.disk.pagenoToByteAddr(5))


    

    