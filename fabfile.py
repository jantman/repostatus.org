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
import requests
import json
import shutil

badge_descriptions = {
    "concept": "Minimal or no implementation has been done yet.",
    "wip": "Initial development is in progress, but there has not yet been a stable, usable release suitable for the public.",
    "suspended": "Initial development has started, but there has not yet been a stable, usable release; work has been stopped for the time being but the author(s) intend on resuming work.",
    "abandoned": "Initial development has started, but there has not yet been a stable, usable release; the project has been abandoned and the author(s) do not intend on continuing development.",
    "active": "The project has reached a stable, usable state and is being actively developed.",
    "inactive": "The project has reached a stable, usable state but is no longer being actively developed; support/maintenance will be provided as time allows.",
    "unsupported": "The project has reached a stable, usable state but the author(s) have ceased all work on it. A new maintainer may be desired.",
}

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
    """ Regenerate the badges into badges/latest """
    badge_sources = {
        'concept': 'http://img.shields.io/badge/repo%20status-Concept-ffffff.svg',
        'wip': 'http://img.shields.io/badge/repo%20status-WIP-yellow.svg',
        'suspended': 'http://img.shields.io/badge/repo%20status-Suspended-orange.svg',
        'abandoned': 'http://img.shields.io/badge/repo%20status-Abandoned-000000.svg',
        'active': 'http://img.shields.io/badge/repo%20status-Active-brightgreen.svg',
        'inactive': 'http://img.shields.io/badge/repo%20status-Inactive-yellowgreen.svg',
        'unsupported': 'http://img.shields.io/badge/repo%20status-Unsupported-lightgrey.svg',
    }
    if not os.path.exists('badges/latest'):
        os.makedirs('badges/latest')
    badge_data = {}
    for name in badge_descriptions:
        badge_data[name] = {'description': badge_descriptions[name], 'url': 'http://www.repostatus.org/badges/{ver}/{name}.svg'.format(ver=version, name=name)}
    with open('badges/latest/badges.json', 'w') as fh:
        fh.write(json.dumps(badge_data, indent=2, sort_keys=True))
    print("badge info written to badges/latest/badges.json")
    for name in badge_sources:
        _download_media(badge_sources[name], 'badges/latest/{n}.svg'.format(n=name))
        _make_badge_markup(name, badge_descriptions[name], badge_data[name]['url'], 'badges/latest')
    print("badge images and markup written to badges/latest")

def publish():
    """Regenerate and publish to GitHub Pages"""
    shutil.rmtree('gh_pages/badges')
    shutil.copytree('badges', 'gh_pages/badges')
    local("ghp-import gh_pages")
    print("Changes pushed into gh-pages branch; please verify that branch and then push it to origin to deploy.")
