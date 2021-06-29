from ..basepage import (BasePage, HEADERSIZE)
from ...globals import *
from ...buffer.frame import Frame
import unittest

class BasePageTests(unittest.TestCase):
    def setUp(self):
        self.page = BasePage(Frame(bytearray(PAGESIZE), 0, False, False))

    def test_pagecreation(self):
        self.assertEqual(0, self.page.getPageType())
        self.assertEqual(0, self.page.getPageNo())

    def test_setget(self):
        data = b'\1'*(PAGESIZE - HEADERSIZE)
        pagetype = 5
        pageno = 2
        nextpageno = 3
        datamax = 4
        self.page.setData(data)
        self.page.setPageType(pagetype)
        self.page.setPageNo(pageno)
        self.page.setDataMax(datamax)
        self.page.setNextPage(nextpageno)
        self.assertEqual(data, self.page.getData())
        self.assertEqual(pagetype, self.page.getPageType())
        self.assertEqual(pageno, self.page.getPageNo())
        self.assertEqual(nextpageno, self.page.getNextPage())
        self.assertEqual(datamax, self.page.getDataMax())

'''
    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError): # (Exception) for any error
            s.split(2)
'''