# -*- coding: utf-8 -*-
import unittest

from contentposter import cpapi

class TestCpApi(unittest.TestCase):

    def setUp(self):
        pass

    def testIsMatched(self):
        slug = 'slug1'
        tags = 'tag1,tag2'

        self.assertFalse(cpapi._isMatched(slug, tags, '', ''))

        self.assertTrue(cpapi._isMatched(slug, tags, 'slug1', ''))
        self.assertTrue(cpapi._isMatched(slug, tags, '', 'tag1'))
        self.assertTrue(cpapi._isMatched(slug, tags, 'slug1', 'tag1'))
        self.assertTrue(cpapi._isMatched(slug, tags, 'slug1', 'tag-n'))
        self.assertTrue(cpapi._isMatched(slug, tags, 'slug-n', 'tag1'))
        self.assertTrue(cpapi._isMatched(slug, tags, 'slug1,slug-n', 'tag-n'))
        self.assertTrue(cpapi._isMatched(slug, tags, 'slug-n', 'tag1,tag-n'))

        self.assertFalse(cpapi._isMatched(slug, tags, 'slug-n', ''))
        self.assertFalse(cpapi._isMatched(slug, tags, '', 'tag-n'))
        self.assertFalse(cpapi._isMatched(slug, tags, 'slug-n', 'tag-n'))

        self.assertTrue(cpapi._isMatched(slug, tags, 'all', ''))
        self.assertTrue(cpapi._isMatched(slug, tags, '', 'all'))
        self.assertTrue(cpapi._isMatched(slug, tags, 'all,slug-n', ''))
        self.assertTrue(cpapi._isMatched(slug, tags, '', 'all,tag-n'))
        self.assertTrue(cpapi._isMatched(slug, tags, 'all', 'all'))
        self.assertTrue(cpapi._isMatched(slug, tags, 'slug-n', 'all'))
        self.assertTrue(cpapi._isMatched(slug, tags, 'all', 'tag-n'))
        self.assertTrue(cpapi._isMatched(None, tags, 'all', ''))
        self.assertTrue(cpapi._isMatched(slug, None, '', 'all'))


if __name__ == '__main__':
    unittest.main()

