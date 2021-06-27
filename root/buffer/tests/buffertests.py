from ..buffer import Buffer
from ..replacers import SequencialReplacer
from ...globals import *
from ...storage.disk import Disk
import unittest
import os

class BufferTests(unittest.TestCase):
    def setUp(self):
        self.filename = 'buffertest.toydb'
        self.disk = Disk(self.filename)
        self.page0 = PAGESIZE*b'\1'
        self.page1 = PAGESIZE*b'\2'
        self.disk.writePage(0, self.page0)
        self.disk.writePage(1, self.page1)
        self.buffer = Buffer(self.disk, SequencialReplacer)

    def tearDown(self):
        self.disk.close()
        os.remove(self.filename)

    def test_requesPageBytes(self):
        self.assertEqual(self.buffer.requestPageBytes(0), self.page0)
        self.assertEqual(self.buffer.requestPageBytes(1), self.page1)
    

