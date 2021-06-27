from ..basepage import BasePage
from ...globals import *
import unittest

class BasePageTests(unittest.TestCase):
    def setUp(self):
        pass

    def test_pagesize(self):
        page = BasePage(4, 6)
        self.assertEqual(4, page.getPageType())
        self.assertEqual(6, page.getPageNo())
        page = BasePage(2, 505)
        self.assertEqual(2, page.getPageType())
        self.assertEqual(505, page.getPageNo())


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