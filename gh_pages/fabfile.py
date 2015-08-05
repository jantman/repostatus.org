from fabric.api import *
import os
import re
import sys
import datetime
import requests
import json

translate_files = [
    ('LICENSE.txt', 'LICENSE.txt'),
]

checkout_paths = [
    'badges',
]

badge_descriptions = {
    "concept": "Minimal or no implementation has been done yet.",
    "wip": "Initial development is in progress, but there has not yet been a stable, usable release suitable for the public.",
    "suspended": "Initial development has started, but there has not yet been a stable, usable release; work has been stopped for the time being but the author(s) intend on resuming work.",
    "abandoned": "Initial development has started, but there has not yet been a stable, usable release; the project has been abandoned and the author(s) do not intend on continuing development.",
    "active": "The project has reached a stable, usable state and is being actively developed.",
    "inactive": "The project has reached a stable, usable state but is no longer being actively developed; support/maintenance will be provided as time allows.",
    "unsupported": "The project has reached a stable, usable state but the author(s) have ceased all work on it. A new maintainer may be desired.",
}

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

def _make_badge_markup(badge_name, description, url, savedir):
    """ generate example markup for a badge, write to disk under savedir """
    alt = "Project Status: {statuscap} - {desc}".format(desc=description, statuscap=badge_name.capitalize())
    target = "http://www.repostatus.org/#{status}".format(status=badge_name)
    with open(os.path.join(savedir, '{n}_md.txt'.format(n=badge_name)), 'w') as fh:
        fh.write("[![{alt}]({url})]({target})\n".format(target=target,
                                                        url=url,
                                                        alt=alt))
    with open(os.path.join(savedir, '{n}_html.txt'.format(n=badge_name)), 'w') as fh:
        fh.write('<a href="{target}"><img src="{url}" alt="{alt}" /></a>\n'.format(url=url,
                                                                                   target=target,
                                                                                   alt=alt))
    with open(os.path.join(savedir, '{n}_rst.txt'.format(n=badge_name)), 'w') as fh:
        fh.write('.. image:: {url}\n   :alt: {alt}\n   :target: {target}\n'.format(url=url,
                                                                                   target=target,
                                                                                   alt=alt))
        
def make_badges():
    """ Regenerate the badges. Once run, copy them into badges/x.y.x/ """
    _require_branch('master')
    version = '0.1.0'
    badge_sources = {
        'concept': 'http://img.shields.io/badge/repo%20status-Concept-ffffff.svg',
        'wip': 'http://img.shields.io/badge/repo%20status-WIP-yellow.svg',
        'suspended': 'http://img.shields.io/badge/repo%20status-Suspended-orange.svg',
        'abandoned': 'http://img.shields.io/badge/repo%20status-Abandoned-000000.svg',
        'active': 'http://img.shields.io/badge/repo%20status-Active-brightgreen.svg',
        'inactive': 'http://img.shields.io/badge/repo%20status-Inactive-yellowgreen.svg',
        'unsupported': 'http://img.shields.io/badge/repo%20status-Unsupported-lightgrey.svg',
    }
    if not os.path.exists('badges/generated'):
        os.makedirs('badges/generated')
    badge_data = {}
    for name in badge_descriptions:
        badge_data[name] = {'description': badge_descriptions[name], 'url': 'http://www.repostatus.org/badges/{ver}/{name}.svg'.format(ver=version, name=name)}
    with open('badges/generated/badges.json', 'w') as fh:
        fh.write(json.dumps(badge_data, indent=2, sort_keys=True))
    print("badge info written to badges/generated/badges.json")
    for name in badge_sources:
        _download_media(badge_sources[name], 'badges/generated/{n}.svg'.format(n=name))
        _make_badge_markup(name, badge_descriptions[name], badge_data[name]['url'], 'badges/generated')
    print("badge images and markup written to badges/generated")
