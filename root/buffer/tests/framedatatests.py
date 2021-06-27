from ..framedata import FDA
from ...globals import *
import unittest

class FrameDataTests(unittest.TestCase):
    def setUp(self):
        self.fda = FDA()

    def test_fdaPageReplacement(self):
        self.fda.replaceFrameData(2, 5)
        self.assertEqual(self.fda.findFrameNo(5), 2)
        