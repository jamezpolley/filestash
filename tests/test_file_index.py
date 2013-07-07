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

class TestFileRead(unittest.TestCase):
    """Read file; check attributes; hash"""

    def setUp(self):
        in_file= open("tests/test_file")
        self.md5 = "0035e1010ea5e875c8776c69dd0ee03e"
        self.sha1 = "f5c13d47495264cfa13f6d46ec52e7ad42474e53"
        hashers = [ hashlib.md5(), hashlib.sha1() ]
        self.digests = file_index.hashes(in_file, hashers)

    def tearDown(self):
        pass

    def test_md5(self):
        self.assertEqual(self.md5, self.digests[0])

    def test_sha1(self):
        self.assertEqual(self.sha1, self.digests[1])

if __name__ == '__main__':
        unittest.main()
