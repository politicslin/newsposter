# -*- coding: utf-8 -*-
import unittest

from contentposter import cpapi

class TestCpApi(unittest.TestCase):

    def setUp(self):
        pass

    def testMatchByTag(self):
        tags = ['tag1', 'tag2']

        self.assertTrue(cpapi._matchByTag(tags, ''))
        self.assertTrue(cpapi._matchByTag(tags, 'tag1'))
        self.assertTrue(cpapi._matchByTag(tags, 'tag1+tag2'))
        self.assertFalse(cpapi._matchByTag(tags, 'tag1+tagn'))
        self.assertFalse(cpapi._matchByTag(tags, 'tagn'))


if __name__ == '__main__':
    unittest.main()

