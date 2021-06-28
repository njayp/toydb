from ..buffer import Buffer
from ..replacers import SequentialReplacer
from ...globals import *
from ...storage.disk import Disk
import unittest
import os

class BufferTests(unittest.TestCase):
    def setUp(self):
        self.filename = 'buffertest.toydb'
        self.disk = Disk(self.filename)
        self.disk.setSize(100)
        self.pages = list(map(lambda i: bytearray([i])*PAGESIZE, range(100)))
        for i, page in enumerate(self.pages):
            self.disk.writeBytes(i, page)      

        self.buffer = Buffer(self.disk, SequentialReplacer)

    def tearDown(self):
        self.buffer.close()
        self.disk.close()
        os.remove(self.filename)

    def test_requestFrame(self):
        self.assertEqual(self.buffer.requestFrame(0).rawbytes, self.pages[0])
        self.assertEqual(self.buffer.requestFrame(50).rawbytes, self.pages[50])

    def test_pinned(self):
        self.assertEqual(self.buffer.requestFrame(31, True).rawbytes, self.pages[31])
        for i in range(50, 100):
            self.buffer.requestFrame(i)
        #print([fd.pageno for fd in self.buffer.replacer.fda])
        self.assertNotEqual(self.buffer.manager.findFrame(31), None)

    def test_writeFlushRead(self):
        self.assertEqual(self.buffer.requestFrame(32).rawbytes, self.pages[32])
        newpage = self.pages[5]
        self.buffer.setPageBytes(newpage, 32)
        self.assertEqual(self.buffer.requestFrame(32).rawbytes, newpage)
        self.assertEqual(self.buffer.manager.findFrame(32).rawbytes, newpage)
        self.assertEqual(self.buffer.manager.findFrame(32).dirty, True)
        for i in range(50, 100):
            self.buffer.requestFrame(i)
        self.assertEqual(self.buffer.manager.findFrame(32), None)
        self.assertEqual(self.buffer.requestFrame(32).rawbytes, newpage)

    

