#!/usr/bin/env python
"""
This is a simple repostatus.org status parser for GitHub repositories.

It is **NOT** compliant with the official spec; this is just something
I use for my own repos, when I know beyond a doubt that the status
badge is in a README file that is rendered properly and automatically
by GitHub.

This requires the requests package, which can be installed via
`pip install requests`.

"""

import sys
import optparse
import requests
import re

def get_repostatusorg_for_url(url):
    """ check and return repo status """
    r = requests.get(url)
    if r.status_code != 200:
        raise SystemExit("ERROR: Got HTTP status code {c} for url: {u}".format(c=r.status_code, u=url))
    m = re.search(r'http[s]?:\/\/.*repostatus\.org\/badges\/(.+)\/(.+)\.svg', r.text)
    if m is None:
        # no match found
        return None
    # ok, the status is in capture group 2 from the above search
    return m.group(2)

def parse_args(argv):
    """ parse arguments/options """
    p = optparse.OptionParser(usage="USAGE: github_simple_checker.py -g <username/reponame> OR -u <url>")
    p.add_option('-g', '--github', action='store', dest='github', type=str, help="github URL portion, in <username>/<reponame> format")
    p.add_option('-u', '--url', action='store', dest='url', type=str, help='URL to check for repostatus badge (for non-GitHub sites)')
    options, args = p.parse_args(argv)

    if options.github and options.url:
        raise SystemExit("ERROR: you must specify either -g/--github or -u/--url not both.")
    
    return options

if __name__ == "__main__":
    # parse and validate options/arguments
    opts = parse_args(sys.argv[1:])
    if opts.github:
        # if github, just build a URL out of the string we were given
        url = 'https://github.com/' + opts.github
    elif opts.url:
        url = opts.url
    else:
        raise SystemExit("ERROR: you must specify either -g/--github or -u/--url; see --help for more info.")
    # get the status
    status = get_repostatusorg_for_url(url)
    if status is None:
        status = 'not specified'
    print("{url} status: {status}".format(url=url, status=status))
