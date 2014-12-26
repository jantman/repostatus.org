---
layout: minimal
---

## Parsers

* [check_github_repos.py](https://github.com/jantman/repostatus.org/blob/master/parsers/check_github_repos.py) Implements the full specification and uses the GitHub API (requires an API token) to list all of a user's repositories (defaulting to the user your token was generated for) and display the status of each one.
* [repostatusorg_list_repo_status.py](https://github.com/jantman/repostatus.org/blob/master/parsers/repostatusorg_list_repo_status.py) implements the full specification to search projects on disk and report their status. It takes an argument of a filesystem path and searches it for a matching status identifier, assuming it is a project. If no candidate files are found (readme, ``repostatus.org`` or ``.repostatus.org``), it assumes this directory holds multiple projects and searches all immediate subdirectories. The final results are output showing the path to the project on disk, and the status that was determined (or "unknown" if candidate files were found, but they all lacked the status identifier URL).
* [github_simple_checker.py](https://github.com/jantman/repostatus.org/blob/master/parsers/github_simple_checker.py) is only suitable for use on one's own projects, as it does not follow the specification. This takes either the name of a GitHub repository (in "username/reponame" format, which it converts to the main project/repository page URL) or an arbitrary URL, and searches for the identifier in the source of the page. This is only suitable for cases when you can be certain that the identifier, if used, will be included in the source of that page (i.e. the automatically-rendered README for a GitHub repo).

