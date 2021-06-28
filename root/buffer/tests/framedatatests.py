from ..frame import FrameArray
from ..replacers import SequencialReplacer
from ...globals import *
import unittest

class FrameDataTests(unittest.TestCase):
    def setUp(self):
        self.replacer = SequencialReplacer()

    def test_fdaPageReplacement(self):
        self.assertEqual(len(self.replacer.framearray), BUFFERSIZE)
        