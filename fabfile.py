from fabric.api import *
import os
import re
import sys
import datetime
import requests
import json

translate_files = [
    ('README.md', 'README.md'),
    ('LICENSE.txt', 'LICENSE.txt'),
]

checkout_paths = [
    'badges',
]

def _get_branch():
    """ get the current git branch """
    br = local("git symbolic-ref -q HEAD", capture=True).replace('refs/heads/', '', 1)
    return br

def _require_branch(b_req):
    branch = _get_branch()
    if branch != b_req:
        print("ERROR: command can only be run on branch {b_req}, not {b}".format(b_req=b_req, b=branch))
        raise SystemExit(1)

def update():
    """ Update files pulled in from master branch """
    _require_branch('gh-pages')
    _check_fabfile_update()
    for f in translate_files:
        _update_file('master', f[0], f[1])
    for p in checkout_paths:
        local("git checkout master -- {p}".format(p=p))

def _get_tags():
    """ get a list of all git tags """
    raw = local("git tag", capture=True).strip().split("\n")
    tags = []
    tag_re = re.compile(r'^\d+\.\d+(\.\d+)?$')
    for t in raw:
        if tag_re.match(t):
            tags.append(t)
    return tags

def _check_fabfile_update():
    """ check for an updated fabfile, update if there is one """
    _update_file('master', 'fabfile.py', 'fabfile.py.master')
    with settings(warn_only=True):
        res = local('diff fabfile.py fabfile.py.master')
    if res.failed:
        print("fabfile.py differs from master, updating")
        os.rename('fabfile.py.master', 'fabfile.py')
        raise SystemExit("fabfile.py updated from master, exiting. Please re-run command")
    os.remove('fabfile.py.master')

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
    _require_branch('master')
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
