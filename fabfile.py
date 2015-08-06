"""
Repostatus.org fabfile - this is used to build badges and push to GitHub Pages.

Requires Python (only tested with 2.7), Fabric and ghp-import.

requirements (and tested versions):

Fabric==1.8.1
ghp-import==0.4.0
requests==2.7.0

"""

from fabric.api import local
import os
import re
import requests
import json
import shutil

badge_info = {
    'concept': {
        'shield_url': 'http://img.shields.io/badge/repo%20status-Concept-ffffff.svg',
        'description': "Minimal or no implementation has been done yet.",
    },
    'wip': {
        'shield_url': 'http://img.shields.io/badge/repo%20status-WIP-yellow.svg',
        'description': "Initial development is in progress, but there has not yet been a stable, usable release suitable for the public.",
    },
    'suspended': {
        'shield_url': 'http://img.shields.io/badge/repo%20status-Suspended-orange.svg',
        'description': "Initial development has started, but there has not yet been a stable, usable release; work has been stopped for the time being but the author(s) intend on resuming work.",
    },
    'abandoned': {
        'shield_url': 'http://img.shields.io/badge/repo%20status-Abandoned-000000.svg',
        'description': "Initial development has started, but there has not yet been a stable, usable release; the project has been abandoned and the author(s) do not intend on continuing development.",
    },
    'active': {
        'shield_url': 'http://img.shields.io/badge/repo%20status-Active-brightgreen.svg',
        'description': "The project has reached a stable, usable state and is being actively developed.",
    },
    'inactive': {
        'shield_url': 'http://img.shields.io/badge/repo%20status-Inactive-yellowgreen.svg',
        'description': "The project has reached a stable, usable state but is no longer being actively developed; support/maintenance will be provided as time allows.",
    },
    'unsupported': {
        'shield_url': 'http://img.shields.io/badge/repo%20status-Unsupported-lightgrey.svg',
        'description': "The project has reached a stable, usable state but the author(s) have ceased all work on it. A new maintainer may be desired.",
    },
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
    """ Regenerate the badges into badges/latest """
    if not os.path.exists('badges/latest'):
        os.makedirs('badges/latest')
    badge_data = {}
    for name in badge_info:
        badge_data[name] = {
            'description': badge_info[name]['description'],
            'url': 'http://www.repostatus.org/badges/latest/{name}.svg'.format(name=name)
        }
    with open('badges/latest/badges.json', 'w') as fh:
        fh.write(json.dumps(badge_data, indent=2, sort_keys=True))
    print("badge info written to badges/latest/badges.json")
    for name, _dict in badge_info.items():
        _download_media(_dict['shield_url'], 'badges/latest/{n}.svg'.format(n=name))
        _make_badge_markup(name, _dict['description'], badge_data[name]['url'], 'badges/latest')
    print("badge images and markup written to badges/latest")

def version_badges(ver):
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

def badges2pages():
    """Copy badges/ to gh_pages/badges/"""
    shutil.rmtree('gh_pages/badges')
    shutil.copytree('badges', 'gh_pages/badges')

def publish():
    """Regenerate and publish to GitHub Pages"""
    x = local('git branch', capture=True)
    if '* master' not in x.stdout:
        print("ERROR: publish must be run from the master branch")
        raise SystemExit(1)
    x = local('git status', capture=True)
    if (('Your branch is up-to-date with' not in x.stdout and
                'HEAD detached at' not in x.stdout) or
                'nothing to commit' not in x.stdout):
        print("ERROR: Your local git clone is dirty or not pushed to origin.")
        raise SystemExit(1)
    local("ghp-import gh_pages")
    print("Changes pushed into gh-pages branch; please verify that branch and then push it to origin to deploy.")
