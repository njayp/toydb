from ...globals import *
from ..frame import Frame
from ..replacers import sequentialReplaceWith
import unittest

class FrameTests(unittest.TestCase):
    def setUp(self):
        self.replacewith = sequentialReplaceWith
        self.framearray = [Frame(bytearray(PAGESIZE), i, False, False) for i in range(BUFFERSIZE)]


    def test_creation(self):
        self.assertEqual(len(self.framearray), BUFFERSIZE)
        
        