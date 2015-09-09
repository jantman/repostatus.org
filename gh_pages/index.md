---
layout: minimal
---

### What It Is

Many people and organizations have publicly available code in varying states of usability, development (whether or not further development is planned), and support (whether bugfixes and user assistance will be given). With the increased popularity of code sharing sites such as GitHub, Gitorious, etc. it's becoming even more common for new projects to be shared publicly from the time of the first commit, and for projects to continue being publicly accessible long after development and support have ceased. So far, there seem to be few if any methods for authors/maintainers to indicate the usability and development/support status of a project. At best, tagging and releases (even when using [semver](http://semver.org/) properly) only differentiate between code that the author deems to be production-ready versus pre-release (and even the definition of pre-release states vary widely). There is no accepted way of indicating the development or support status of a project, specifically whether or not further development is planned and whether support will be provided. Repostatus.org aims to fill this gap by providing an easy-to-use method of communicating the usability and development/support status of a project to both humans and machines.

This is accomplished by including a simple badge or URL in your project's README file, or by including a link in a specially-named file inside your project. The badge is easily visible to humans, and machines can determine the project's status by searching for a string matching a specific pattern in a set list of possible files. We define a list of possible project statuses which aim to encompass axes of both code completion and development/support status (future plans), in a simple and user-centric manner.

#### Project Statuses

* <a name="concept"></a>__Concept__ – Minimal or no implementation has been done yet.
* <a name="wip"></a>__WIP__ – Initial development is in progress, but there has not yet been a stable, usable release suitable for the public.
* <a name="suspended"></a>__Suspended__ – Initial development has started, but there has not yet been a stable, usable release; work has been stopped for the time being but the author(s) intend on resuming work.
* <a name="abandoned"></a>__Abandoned__ – Initial development has started, but there has not yet been a stable, usable release; the project has been abandoned and the author(s) do not intend on continuing development.
* <a name="active"></a>__Active__ – The project has reached a stable, usable state and is being actively developed.
* <a name="inactive"></a>__Inactive__ – The project has reached a stable, usable state but is no longer being actively developed; support/maintenance will be provided as time allows.
* <a name="unsupported"></a>__Unsupported__ – The project has reached a stable, usable state but the author(s) have ceased all work on it. A new maintainer may be desired.

These status descriptions and the URLs to the corresponding icons are also available in a [JSON file](/badges/latest/badges.json).

### What It Looks Like

When using the recommended method (a badge embedded in your project's README file), it's as concise as this one image:

[![Project Status: Active – The project has reached a stable, usable state and is being actively developed.](http://www.repostatus.org/badges/latest/active.svg)](http://www.repostatus.org/#active)

This incorporates three components:

1. The image URL, which serves as the machine-readable status identifier. It points to a status-specific image hosted on repostatus.org, and also incorporates a specification version number.
2. Alt-text on the image (this can generally be viewed in a browser by mousing over the image) which begins with the canonical project status ("Project Status: <status name>") and can optionally be followed by a human-readable description of the status, provided by the project's maintainer(s). Such text might also be useful to appear after the badge.
3. The image is linked back to the particular status description on repostatus.org.

### How to Use It

Setting up your project to use RepoStatus.org is as simple as adding the appropriate badge to your project's README file. We define this file as any file at the top level of the project, whose name begin with the (case-insensitive) string 'readme'. When programs check the project status, they will search through any ``/^readme.*$/i`` files in lexicographical order, and choose the first one with a valid repostatus.org status URL in it. If this isn't suitable for your project, there are also some additional options described below ("Machine-Readable Only"). Note that while I've tried to think of this to be as flexible as possible, it's very strongly suggested that the badge appear in a README file rendered on your project's site (such as the readme rendering in GitHub repositories).

Below are the various status icons, along with paste-able markup to add them in a variety of markup languages. Feel free to alter the alt-text (after the first ``-``) to suit your needs.

* __Concept__ [![Project Status: Concept – Minimal or no implementation has been done yet.](http://www.repostatus.org/badges/latest/concept.svg)](http://www.repostatus.org/#concept) [markdown](javascript:showsample('concept','md')) [ReST](javascript:showsample('concept','rst')) [HTML](javascript:showsample('concept','html'))
* __WIP__ [![Project Status: Wip – Initial development is in progress, but there has not yet been a stable, usable release suitable for the public.](http://www.repostatus.org/badges/latest/wip.svg)](http://www.repostatus.org/#wip) [markdown](javascript:showsample('wip','md')) [ReST](javascript:showsample('wip','rst')) [HTML](javascript:showsample('wip','html'))
* __Suspended__ [![Project Status: Suspended – Initial development has started, but there has not yet been a stable, usable release; work has been stopped for the time being but the author(s) intend on resuming work.](http://www.repostatus.org/badges/latest/suspended.svg)](http://www.repostatus.org/#suspended) [markdown](javascript:showsample('suspended','md')) [ReST](javascript:showsample('suspended','rst')) [HTML](javascript:showsample('suspended','html'))
* __Abandoned__ [![Project Status: Abandoned – Initial development has started, but there has not yet been a stable, usable release; the project has been abandoned and the author(s) do not intend on continuing development.](http://www.repostatus.org/badges/latest/abandoned.svg)](http://www.repostatus.org/#abandoned) [markdown](javascript:showsample('abandoned','md')) [ReST](javascript:showsample('abandoned','rst')) [HTML](javascript:showsample('abandoned','html'))
* __Active__ [![Project Status: Active – The project has reached a stable, usable state and is being actively developed.](http://www.repostatus.org/badges/latest/active.svg)](http://www.repostatus.org/#active) [markdown](javascript:showsample('active','md')) [ReST](javascript:showsample('active','rst')) [HTML](javascript:showsample('active','html'))
* __Inactive__ [![Project Status: Inactive – The project has reached a stable, usable state but is no longer being actively developed; support/maintenance will be provided as time allows.](http://www.repostatus.org/badges/latest/inactive.svg)](http://www.repostatus.org/#inactive) [markdown](javascript:showsample('inactive','md')) [ReST](javascript:showsample('inactive','rst')) [HTML](javascript:showsample('inactive','html'))
* __Unsupported__ [![Project Status: Unsupported – The project has reached a stable, usable state but the author(s) have ceased all work on it. A new maintainer may be desired.](http://www.repostatus.org/badges/latest/unsupported.svg)](http://www.repostatus.org/#unsupported) [markdown](javascript:showsample('unsupported','md')) [ReST](javascript:showsample('unsupported','rst')) [HTML](javascript:showsample('unsupported','html'))

<div id="samplewrapper" style="display: none;"><h5 id="sampletitle"></h5><div id="samplecode"></div></div>

#### Machine-Readable Only

If for some reason you don't want people to see the repostatus.org status identifier (which defeats half the purpose of this idea, but may be valid for some people), you can place just the URL to the status image in a ``.repostatus.org`` or ``repostatus.org`` file in the top-level of your project. Per the specification, programs that determine project status check these files _after_ the README file(s).

### Specification

I really wanted to write a full specification for this, complete with versioned URLs and JSON metadata describing the different statuses. If anyone else in the world wants to use this stuff, maybe I'll do that. In the mean time, here's version 0.1.0 of the "specification".

#### Identifier Strings

The repostatus.org badge URL is the authoritative identifier of status. Regardless of any other formatting, when machines attempt to determine status they should only key off of a URL matching ``/^http[s]?:\/\/.*repostatus\.org\/badges\/(.+)\/(.+)\.svg$/``. The first capture group identifies the specification/API version, and the second identifies the status name. Note that the specification/API version can currently be a [semver](http://semver.org/)-compliant string, or the string "latest".

#### Machine Location and Parsing

Machine parsing is quite simple: first, search through any files in the top-level directory of the project (ideally on the default branch, usually master for git) matching ``/^readme.*$/i`` (note the case-insensitivity) in lexicographic order. The first one with a match for the identifier string (URL) wins, and the first complete match within the file wins. If no files match, then search for a ``.repostatus.org`` file, and if none is found, a ``repostatus.org`` file. Machine parsing _should_ follow the full specification rather than assuming file names (or assuming that a project's readme will be correctly displayed on GitHub).

There are some example parsers listed on the [parsers](/parsers) page.

### Changelog

See the [CHANGELOG.md on GitHub](https://github.com/jantman/repostatus.org/blob/master/CHANGELOG.md).

### Contributing

This is a crazy idea of mine. But I think it's useful. I'm very open to comments, criticisms, suggestions, etc. Feel free to open an [issue on GitHub](https://github.com/jantman/repostatus.org/issues) or submit a pull request. Instructions for contributing are available [in the README on GitHub](https://github.com/jantman/repostatus.org/blob/master/README.md#contributing). A list of contributors is [also available](https://github.com/jantman/repostatus.org/blob/master/CONTRIBUTORS.md).
