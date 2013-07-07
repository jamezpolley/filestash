#!/usr/bin/env python
# encoding: utf-8

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

    def __repr__(self):
        """Simple string representing the file.  """

        repr = "%(collection_date)s %(file_name)s: %(md5)s %(sha1)s %(stat)s" % self.__dict__
        return repr

def main():
    tag = sys.argv[1]
    file_path = sys.argv[2]

    all_files = {}

    if os.path.isdir(file_path):
        for root, dirs, files in os.walk(file_path):
            base = os.path.abspath(root)
            for file in files:
                full_path = os.path.join(base, file)
                all_files[full_path] = File(tag, full_path)
    else:
        full_path = os.path.abspath(file_path)
        myfile = File(tag, full_path)
        all_files[full_path] = myfile

    print yaml.dump(all_files)

if __name__ == '__main__':
    main()

