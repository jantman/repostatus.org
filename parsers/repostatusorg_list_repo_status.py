#!/usr/bin/env python
"""
This is an example parser for the <https://www.repostatus.org/> specification.
It checks a single project/repository on disk, or a directory containing multiple
projects, and reports the status(es).

NOTE: This script works with Python 2.7 or newer.

=============
Example Usage
=============

On a single directory, containing a README.md file with the identifier string present in it:

    $ repostatusorg_list_repo_status.py -p ~/GIT/repostatus.org/
    /home/jantman/GIT/repostatus.org/: active

In pwd, containing a README.md file with the identifier string present:

    $ repostatusorg_list_repo_status.py
    ./: active

On a directory containing multiple git clones, some of which have the identifier present:

    $ parsers/repostatusorg_list_repo_status.py -p ~/GIT
    /home/jantman/GIT/php-nagios-xml: unsupported
    /home/jantman/GIT/ec2machines: active
    /home/jantman/GIT/nodejs-rpm-centos5: inactive
    /home/jantman/GIT/updatewatcher: concept
    /home/jantman/GIT/repostatus.org: active
    /home/jantman/GIT/TuxTruck-wxPython: abandoned

=========
Copyright
=========

Copyright 2014 Jason Antman <jason@jasonantman.com> <http://www.jasonantman.com>
Free for any use provided that patches are submitted back to me.

The latest version of this script can be found at:
https://github.com/jantman/repostatus.org/blob/master/parsers/repostatusorg_list_repo_status.py

=========
CHANGELOG
=========

2014-12-25 jantman:
- initial script
"""

import sys
import argparse
import logging
import os
import re

FORMAT = "[%(levelname)s %(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
logging.basicConfig(level=logging.ERROR, format=FORMAT)


class RepoStatusOrg_Checker:
    """ check directories on disk for repostatus.org status identifier """

    readme_re = re.compile(r'^readme.*$', flags=re.I)
    url_re = re.compile(r'http[s]?:\/\/.*repostatus\.org\/badges\/(.+)\/(.+)\.svg', flags=re.I)
    
    def __init__(self, verbose=False):
        self.logger = logging.getLogger(self.__class__.__name__)
        if verbose:
            self.logger.setLevel(logging.DEBUG)

    def check(self, path):
        """
        check a path, that may be a single project
        or a directory containing multiple projects

        returns a dictionary of path to status name (or None if no status found)

        :param path: path to check
        :type path: string
        :rtype: dict
        """
        # first, see if we have a matching file in this path
        candidates = self._find_candidate_files(path)
        self.logger.debug("Found {c} candidate files in path {p}: {candidates}".format(c=len(candidates),
                                                                                       p=path,
                                                                                       candidates=candidates))
        if len(candidates) > 0:
            # this path is a project itself, check for a match and return that
            self.logger.debug("Found candidate files in {p}; checking only this path".format(p=path))
            res = self._find_status_for_files(candidates)
            return {path: res}
        # else we found no candidates; look for child directories that might be projects
        self.logger.debug("Found no candidate files in {p}; checking subdirectories".format(p=path))
        res = {}
        for d in os.listdir(path):
            dpath = os.path.join(path, d)
            if not os.path.isdir(dpath) or d == '.' or d == '..':
                self.logger.debug("skipping non-directory or system directory: {dpath}".format(dpath=dpath))
                continue
            candidates = self._find_candidate_files(dpath)
            if len(candidates) < 1:
                self.logger.debug("found 0 candidates in directory: {dpath}".format(dpath=dpath))
                continue
            self.logger.debug("Found candidate files in subdirectory: {d}".format(d=dpath))
            res[dpath] = self._find_status_for_files(candidates)
        return res

    def _find_status_for_files(self, flist):
        """
        Given a list of files to search, returns the repostatus.org version
        and status name of the first matching status identifier URL found;
        searches the files in list order. Returns None if no match found

        :param flist: list of files to search through, in order
        :type flist: list of strings (file paths)
        :rtype: 2-tuple (version, status name) or None
        """
        for f in flist:
            with open(f, 'r') as fh:
                content = fh.read()
            res = self.url_re.search(content)
            if res is not None:
                self.logger.debug("Match found in {f}: {u}".format(f=f, u=res.group(0)))
                return (res.group(1), res.group(2))
        return None
        
    def _find_candidate_files(self, path):
        """
        Return a list of all files under a given path,
        which should be examined for a repostatus identifier.
        List is in the order they should be checked.
        """
        candidates = []
        files = os.listdir(path)
        # sort files lexicographically
        for fname in sorted(files, lambda x,y: cmp(x.lower(), y.lower()) or cmp(x,y)):
            if self.readme_re.match(fname) and os.path.isfile(os.path.join(path, fname)):
                candidates.append(os.path.join(path, fname))
        for fname in [os.path.join(path, '.repostatus.org'), os.path.join(path, 'repostatus.org')]:
            if os.path.exists(fname) and os.path.isfile(fname):
                candidates.append(fname)
        return candidates
            

def parse_args(argv):
    """
    parse command line arguments/options
    """
    p = argparse.ArgumentParser(description='Sample python script skeleton.')
    p.add_argument('-v', '--verbose', dest='verbose', action='store_true', default=False,
                   help='verbose output (internal debugging).')
    p.add_argument('-p', '--path', dest='path', type=str, default=os.getcwd(),
                   help='path to a project or directory of projects to check; default is cwd')
    args = p.parse_args(argv)
    return args

if __name__ == "__main__":
    args = parse_args(sys.argv[1:])
    # initialize the class
    checker = RepoStatusOrg_Checker(verbose=args.verbose)
    # run the check
    result = checker.check(args.path)
    for dir_path in result:
        status = 'unknown'
        if result[dir_path] is not None:
            status = result[dir_path][1]
        print("{dirpath}: {status}".format(dirpath=dir_path, status=status))
