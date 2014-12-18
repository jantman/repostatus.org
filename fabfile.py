from fabric.api import *
import os
import re
import sys
import datetime
import requests
import json

update_files = [
    ('README.md', 'bar'),
    ('LICENSE.txt', 'blam/blarg/hsof/lic.t'),
]

def update():
    """ Update files pulled in from master branch """
    for f in update_files:
        _update_file('master', f[0], f[1])
    # version-specific stuff
    tags = _get_tags()
    raise SystemExit("do version-specific stuff")

def _get_tags():
    """ get a list of all git tags """
    raw = local("git tag", capture=True).strip().split("\n")
    tags = []
    tag_re = re.compile(r'^\d+\.\d+(\.\d+)?$')
    for t in raw:
        if tag_re.match(t):
            tags.append(t)
    return tags
        
def _update_file(src_treeish, src_path, dst_path):
    """ update a single file from another branch into this one """
    _check_dirs(dst_path)
    local("git show {t}:{s} > {d}".format(t=src_treeish, s=src_path, d=dst_path))

def _check_dirs(fname):
    """ get parent directories to a file; create them under pwd if they don't exist """
    d = os.path.dirname(fname)
    if d == '':
        return
    if os.path.exists(d) and not os.path.isdir(d):
        raise SystemExit("ERROR: path {d} exists but is not a directory.".format(d=d))
    if not os.path.exists(d):
        os.makedirs(d)

def _download_media(url, fname):
    """ download the given binary URL to fname """
    if os.path.exists(fname):
        raise SystemExit("Path {f} already exists.".format(f=fname))
    r = requests.get(url, stream=True)
    if r.status_code != 200:
        raise SystemExit("%s returned status code %d" % (url, r.status_code))
    with open(fname, 'wb') as fh:
        for chunk in r.iter_content():
            fh.write(chunk)
        fh.flush()

def make_badges():
    """ Regenerate the badges. Once run, copy them into badges/x.y.x/ """
    badges = {
        'concept': 'http://img.shields.io/badge/repo%20status-Concept-ffffff.svg',
        'wip': 'http://img.shields.io/badge/repo%20status-WIP-yellow.svg',
        'suspended': 'http://img.shields.io/badge/repo%20status-Suspended-orange.svg',
        'abandoned': 'http://img.shields.io/badge/repo%20status-Abandoned-000000.svg',
        'active': 'http://img.shields.io/badge/repo%20status-Active-brightgreen.svg',
        'inactive': 'http://img.shields.io/badge/repo%20status-Inactive-yellowgreen.svg',
        'unsupported': 'http://img.shields.io/badge/repo%20status-Unsupported-lightgrey.svg',
    }
    for name in badges:
        _download_media(badges[name], '{n}.svg'.format(n=name))

