from ..buffer import Buffer
from ..replacers import SequentialReplacer
from ...globals import *
from ...storage.disk import Disk
from ..frame import Frame
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
        frame = self.buffer.requestFrame(0)
        self.assertEqual(frame.rawbytes, self.pages[0])
        frame.pinned = False

    def test_pinned(self):
        pageno = 31
        frame = self.buffer.requestFrame(pageno)
        self.assertEqual(frame.rawbytes, self.pages[pageno])
        for i in range(50, 100):
            self.buffer.requestFrame(i).pinned = False
        #print([fd.pageno for fd in self.buffer.replacer.fda])
        self.assertNotEqual(self.buffer.manager.findFrame(pageno), None)

    def test_writeFlushRead(self):
        pageno = 42
        frame = self.buffer.requestFrame(pageno)
        self.assertEqual(frame.rawbytes, self.pages[pageno])
        newpage = self.pages[5]
        frame.rawbytes = newpage
        frame.pinned = False
        self.buffer.returnFrame(frame)
        self.assertEqual(self.buffer.manager.findFrame(pageno).rawbytes, newpage)
        self.assertEqual(self.buffer.manager.findFrame(pageno).dirty, True)
        for i in range(50, 100):
            self.buffer.requestFrame(i).pinned = False
        self.assertEqual(self.buffer.manager.findFrame(pageno), None)
        self.assertEqual(self.buffer.requestFrame(pageno).rawbytes, newpage)

    

