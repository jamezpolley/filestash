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

class FileStats(object):
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

class FileStatsBucket(collections.defaultdict):
    """Bucket for storing FileStats.

    It's a multidict. Like a dict but values are stored in lists to handle duplicates.
    """

    def __init__(self):
        self.duplicates = set([])
        super(FileStatsBucket, self).__init__(list)

    def __str__(self):
        return yaml.dump((self.duplicates, self))

    def add_file(self, file):
        if file.sha1 in self:
            self.duplicates.add(file.sha1)
        self[file.sha1].append(file)

    def add_bucket(self, bucket):
        for sha1, file in bucket.iteritems():
            self[sha1] = file

class FilesystemStatsCollector(object):
    """Walks the filesystem, collects FileStats and stores them in a Bucket"""

    def __init__(self, tag, collection_date=None, collection_host=None):
        """Create the Collector

        :tag: tag to record on FileStats
        :collection_date: date to record on FileStats
        :collection_host: host to record on FileStats
        """
        self._bucket = FileStatsBucket()
        self.tag = tag
        self.collection_date = collection_date
        self.collection_host = collection_host

    def add(self, file_path):
        """Collect stats on files under file_path and add them to the bucket.

        :file_path: @todo
        :returns: @todo

        """
        if os.path.isdir(file_path):
            for root, dirs, files in os.walk(file_path):
                base = os.path.abspath(root)
                for file in files:
                    full_path = os.path.join(base, file)
                    f = FileStats(self.tag, full_path)
                    self._bucket.add_file(f)
        else:
            full_path = os.path.abspath(file_path)
            f = FileStats(self.tag, full_path)
            self._bucket.add_file(f)

def main():
    tag = sys.argv[1]
    file_path = sys.argv[2]

    collector = FilesystemStatsCollector(tag)
    collector.add(file_path)

    print collector._bucket

if __name__ == '__main__':
    main()

