from fabric.api import *
import os
import re
import sys
import datetime

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

