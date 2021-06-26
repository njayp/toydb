from .. import basepage
from ...globals import *
import unittest

class BasePageTests(unittest.TestCase):
    def setUp(self):
        self.page = basepage.BasePage()
'''
    def test_pagesize(self):
        self.assertEqual(1024, PAGESIZE)
'''

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