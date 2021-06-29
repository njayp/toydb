import string
import json
from ...buffer.buffer import Buffer
from ...storage.disk import Disk
from ...page.headerpage import HeaderPage
from ...globals import *
from ..heapfile import HeapFile
import os

class BufferTests(unittest.TestCase):
    def setUp(self):
        self.filename = 'heapfiletest.toydb'      
        self.hf = HeapFile(self.diskname)

    def tearDown(self):
        self.hf.close()
        os.remove(self.filename)

        