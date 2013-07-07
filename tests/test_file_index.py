#!/usr/bin/env python
# encoding: utf-8

import StringIO
import hashlib
import unittest

import file_index

class TestHashes(unittest.TestCase):
    """Test that the multiple-hash generator works as expected"""

    def setUp(self):
        input = "A test string\n"
        self.md5 = "0035e1010ea5e875c8776c69dd0ee03e"
        self.sha1 = "f5c13d47495264cfa13f6d46ec52e7ad42474e53"
        hashers = [ hashlib.md5(), hashlib.sha1() ]
        self.input = StringIO.StringIO(input)
        self.digests = file_index.hashes (self.input, hashers)

    def tearDown(self):
        pass

    def test_md5(self):
        self.assertEqual(self.digests[0], self.md5)

    def test_sha1(self):
        self.assertEqual(self.digests[1], self.sha1)

if __name__ == '__main__':
        unittest.main()
