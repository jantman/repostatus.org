# -*- coding: utf-8 -*-
"""
Repostatus.org fabfile – this is used to build badges and push to GitHub Pages.

Requires Python (tested with 3.8), Fabric and ghp-import.

requirements (and tested versions):

Fabric==2.5.0
ghp-import==0.4.0
requests==2.7.0

"""

from fabric import task
import os
import re
import requests
import json
import shutil

badge_info = {
    'concept': {
        'shield_url': 'http://img.shields.io/badge/repo%20status-Concept-ffffff.svg',
        'description': "Minimal or no implementation has been done yet, or the repository is only intended to be a limited example, demo, or proof-of-concept.",
        'display_name': 'Concept',
    },
    'wip': {
        'shield_url': 'http://img.shields.io/badge/repo%20status-WIP-yellow.svg',
        'description': "Initial development is in progress, but there has not yet been a stable, usable release suitable for the public.",
        'display_name': 'WIP',
    },
    'suspended': {
        'shield_url': 'http://img.shields.io/badge/repo%20status-Suspended-orange.svg',
        'description': "Initial development has started, but there has not yet been a stable, usable release; work has been stopped for the time being but the author(s) intend on resuming work.",
        'display_name': 'Suspended',
    },
    'abandoned': {
        'shield_url': 'http://img.shields.io/badge/repo%20status-Abandoned-red.svg',
        'description': "Initial development has started, but there has not yet been a stable, usable release; the project has been abandoned and the author(s) do not intend on continuing development.",
        'display_name': 'Abandoned',
    },
    'active': {
        'shield_url': 'http://img.shields.io/badge/repo%20status-Active-brightgreen.svg',
        'description': "The project has reached a stable, usable state and is being actively developed.",
        'display_name': 'Active',
    },
    'inactive': {
        'shield_url': 'http://img.shields.io/badge/repo%20status-Inactive-yellowgreen.svg',
        'description': "The project has reached a stable, usable state but is no longer being actively developed; support/maintenance will be provided as time allows.",
        'display_name': 'Inactive',
    },
    'unsupported': {
        'shield_url': 'http://img.shields.io/badge/repo%20status-Unsupported-lightgrey.svg',
        'description': "The project has reached a stable, usable state but the author(s) have ceased all work on it. A new maintainer may be desired.",
        'display_name': 'Unsupported',
    },
    "moved": {
        'shield_url': 'http://img.shields.io/badge/repo%20status-Moved-red.svg',
        'description': 'The project has been moved to a new location, and the version at that location should be considered authoritative.',
        'display_name': 'Moved'
    }
}

def _download_media(url, fname):
    """ download the given binary URL to fname """
    r = requests.get(url, stream=True)
    if r.status_code != 200:
        raise SystemExit("%s returned status code %d" % (url, r.status_code))
    with open(fname, 'wb') as fh:
        for chunk in r.iter_content():
            fh.write(chunk)
        fh.flush()

def _make_badge_markup(badge_name, display_name, description, url, savedir):
    """ generate example markup for a badge, write to disk under savedir """
    if badge_name == 'moved':
        moved_to = 'http://example.com'
        moved = 'to %s ' % moved_to
    else:
        moved_to = None
        moved = ''
    alt = "Project Status: {statuscap} {moved}– {desc}".format(
        desc=description,
        statuscap=display_name,
        moved=moved
    )
    target = "https://www.repostatus.org/#{status}".format(status=badge_name)
    with open(os.path.join(savedir, '{n}_md.txt'.format(n=badge_name)), 'w') as fh:
        fh.write(_format_md(url, target, alt, moved_to))
    with open(os.path.join(savedir, '{n}_html.txt'.format(n=badge_name)), 'w') as fh:
        fh.write(_format_html(url, target, alt, moved_to))
    with open(os.path.join(savedir, '{n}_rst.txt'.format(n=badge_name)), 'w') as fh:
        fh.write(_format_rst(url, target, alt, moved_to))

def _format_md(url, target, alt, moved_to=None):
    if moved_to is None:
        moved = ''
    else:
        moved = ' to [%s](%s)' % (moved_to, moved_to)
    s = "[![{alt}]({url})]({target}){moved}\n".format(
        target=target,
        url=url,
        alt=alt,
        moved=moved
    )
    return s

def _format_rst(url, target, alt, moved_to=None):
    if moved_to is None:
        return '.. image:: {url}\n   :alt: {alt}\n   :target: {target}\n'.format(
            url=url,
            target=target,
            alt=alt
        )
    s = '|repostatus| to `%s <%s>`_\n\n' % (moved_to, moved_to)
    s += '.. |repostatus| image:: {url}\n   :alt: {alt}\n   ' \
        ':target: {target}\n'.format(
            url=url,
            target=target,
            alt=alt
        )
    return s

def _format_html(url, target, alt, moved_to=None):
    if moved_to is None:
        moved = ''
    else:
        moved = ' to <a href="%s">%s</a>' % (moved_to, moved_to)
    s = '<a href="{target}"><img src="{url}" alt="{alt}" /></a>{moved}\n'.format(
        url=url,
        target=target,
        alt=alt,
        moved=moved
    )
    return s

@task
def make_badges(c):
    """ Regenerate the badges into badges/latest """
    if not os.path.exists('badges/latest'):
        os.makedirs('badges/latest')
    badge_data = {}
    for name in badge_info:
        badge_data[name] = {
            'description': badge_info[name]['description'],
            'url': 'https://www.repostatus.org/badges/latest/{name}.svg'.format(name=name),
            'display_name': badge_info[name]['display_name'],
        }
    with open('badges/latest/badges.json', 'w') as fh:
        fh.write(json.dumps(badge_data, indent=2, sort_keys=True))
    print("badge info written to badges/latest/badges.json")
    for name, _dict in badge_info.items():
        _download_media(_dict['shield_url'], 'badges/latest/{n}.svg'.format(n=name))
        _make_badge_markup(name, _dict['display_name'], _dict['description'], badge_data[name]['url'], 'badges/latest')
    print("badge images and markup written to badges/latest")

@task
def version_badges(c, ver):
    """Copy the latest badges into a versioned directory; update related files"""
    if not re.match(r'\d+\.\d+\.\d+', ver):
        raise SystemExit("Error: %s does not appear to be an x.y.z semver version" % ver)
    badgedir = os.path.join('badges', ver)
    if os.path.exists(badgedir):
        raise SystemExit("Error: badge version %s already present!" % ver)
    # copy latest
    print("Copying badges/latest to badges/%s" % ver)
    shutil.copytree('badges/latest', 'badges/%s' % ver)
    # update URLs
    print("Updating URLs in badges/%s/*.txt" % ver)
    for fname in os.listdir(badgedir):
        if not fname.endswith('.txt'):
            continue
        fpath = os.path.join(badgedir, fname)
        with open(fpath, 'r') as fh:
            content = fh.read()
        content = content.replace('/badges/latest/', '/badges/%s/' % ver)
        with open(fpath, 'w') as fh:
            fh.write(content)
    print("Updating badges/%s/badges.json" % ver)
    with open('badges/%s/badges.json' % ver, 'r') as fh:
        content = fh.read()
    content = content.replace('/badges/latest/', '/badges/%s/' % ver)
    with open('badges/%s/badges.json' % ver, 'w') as fh:
        fh.write(content)

@task
def badges2pages(c):
    """Copy badges/ to gh_pages/badges/"""
    shutil.rmtree('gh_pages/badges')
    shutil.copytree('badges', 'gh_pages/badges')

@task
def publish(c):
    """Regenerate and publish to GitHub Pages"""
    x = c.run('git branch')
    if '* master' not in x.stdout:
        print("ERROR: publish must be run from the master branch")
        raise SystemExit(1)
    x = c.run('git status')
    if (('Your branch is up-to-date with' not in x.stdout and
                'HEAD detached at' not in x.stdout) or
                'nothing to commit' not in x.stdout):
        print("ERROR: Your local git clone is dirty or not pushed to origin.")
        raise SystemExit(1)
    c.run("ghp-import gh_pages")
    print("Changes pushed into gh-pages branch; please verify that branch and then push it to origin to deploy.")
