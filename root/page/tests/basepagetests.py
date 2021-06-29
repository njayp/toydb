from ..basepage import (BasePage, HEADERSIZE)
from ...globals import *
from ...buffer.frame import Frame
import unittest

class BasePageTests(unittest.TestCase):
    def setUp(self):
        self.page = BasePage(Frame(bytearray(PAGESIZE), 0, False, False))

    def test_setget(self):
        data = b'\1'*(PAGESIZE - HEADERSIZE)
        nextpageno = 3
        datamax = 4
        self.page.setDataBytes(data)
        self.page.setDataMax(datamax)
        self.page.setNextPage(nextpageno)
        self.assertEqual(data, self.page.getDataBytes())
        self.assertEqual(nextpageno, self.page.getNextPage())
        self.assertEqual(datamax, self.page.getDataMax())
