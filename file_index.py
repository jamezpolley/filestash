#!/usr/bin/env python
# encoding: utf-8

from functools import total_ordering
import collections
import datetime
import hashlib
import os
import os.path
import platform
import stat
import sys

import yaml

def hashes(stream, hashers):
    """Run the hashers over the input stream.

    Data is read from stream.read() and fed to the update() function of each
    hasher.

    Parameters:
    * stream: a stream to be hashed
    * hashers: an array of hashing functions. The file is fed to them all.

    Returns:
    * digests: array of digests from the hash functions in hashers
    """

    chunk = stream.read(8192)
    while chunk:
        for hasher in hashers:
            hasher.update(chunk)
        chunk = stream.read(8192)

    digests = [ hasher.hexdigest() for hasher in hashers ]
    return digests

class File(object):
    """A single on-disk file

    TODO: file type detection
    TODO: payload detection; payload hashes; payload metadata

    """
    def __init__(self, tag, file_path, collection_date=None, hostname=None):
        self.stat = os.stat(file_path)

        self.tag = tag
        self.path = os.path.abspath(file_path)
        self.file_name = os.path.basename(file_path)
        self.collection_date = datetime.datetime.now()
        self.collection_host = hostname or platform.node()
        self.md5, self.sha1 = hashes(open(file_path),
                                     (hashlib.md5(), hashlib.sha1()))

    def __str__(self):
        """Simple string representing the file.  """
        return "%(sha1)s %(file_name)s" % self.__dict__

class FileBucket(dict):
    """Bucket for storing Files.

    It's a multidict. Like a dict but values are stored in lists to handle duplicates.
    """

    def __setitem__(self, key, item):
        """@todo: Docstring for __setitem__

        :arg1: @todo
        :returns: @todo
        """

        self.setdefault(key, []).append(item)



def main():
    tag = sys.argv[1]
    file_path = sys.argv[2]

    fb = FileBucket()

    if os.path.isdir(file_path):
        for root, dirs, files in os.walk(file_path):
            base = os.path.abspath(root)
            for file in files:
                full_path = os.path.join(base, file)
                f = File(tag, full_path)
                fb[f.sha1] = f
    else:
        full_path = os.path.abspath(file_path)
        f = File(tag, full_path)
        fb[f.sha1] = f

    print yaml.dump(fb)

if __name__ == '__main__':
    main()

