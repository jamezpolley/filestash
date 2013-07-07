#!/usr/bin/env python
# encoding: utf-8

import datetime
import hashlib
import os
import os.path
import platform
import stat
import sys

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

    * file type - optional
    * hashes - md5, sha

    Body:
        * payload hashes
        * payload metadata

    """


    def __init__(self, tag, file_path, collection_date=None, hostname=None):
        self.stat = os.stat(file_path)

        self.tag = tag
        self.path = os.path.abspath(file_path)
        self.file_name = os.path.basename(file_path)
        self.collection_date = datetime.datetime.now()
        self.collection_host = hostname or platform.node()

def main():
    tag = sys.argv[1]
    file_path = sys.argv[2]

    myfile = File(tag, file_path)
    print myfile.stat

if __name__ == '__main__':
    main()

