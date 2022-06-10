---
layout: minimal
---

### What It Is

Many people and organizations have publicly available code in varying states of usability, development (whether or not further development is planned), and support (whether bugfixes and user assistance will be given). With the increased popularity of code sharing sites such as GitHub, Gitorious, etc. it's becoming even more common for new projects to be shared publicly from the time of the first commit, and for projects to continue being publicly accessible long after development and support have ceased. So far, there seem to be few if any methods for authors/maintainers to indicate the usability and development/support status of a project. At best, tagging and releases (even when using [semver](https://semver.org/) properly) only differentiate between code that the author deems to be production-ready versus pre-release (and even the definition of pre-release states vary widely). There is no accepted way of indicating the development or support status of a project, specifically whether or not further development is planned and whether support will be provided. Repostatus.org aims to fill this gap by providing an easy-to-use method of communicating the usability and development/support status of a project to both humans and machines.

This is accomplished by including a simple badge or URL in your project's README file, or by including a link in a specially-named file inside your project. The badge is easily visible to humans, and machines can determine the project's status by searching for a string matching a specific pattern in a set list of possible files. We define a list of possible project statuses which aim to encompass axes of both code completion and development/support status (future plans), in a simple and user-centric manner.

#### Project Statuses

* <a name="concept"></a>__Concept__ – Minimal or no implementation has been done yet, or the repository is only intended to be a limited example, demo, or proof-of-concept.
* <a name="wip"></a>__WIP__ – Initial development is in progress, but there has not yet been a stable, usable release suitable for the public.
* <a name="suspended"></a>__Suspended__ – Initial development has started, but there has not yet been a stable, usable release; work has been stopped for the time being but the author(s) intend on resuming work.
* <a name="abandoned"></a>__Abandoned__ – Initial development has started, but there has not yet been a stable, usable release; the project has been abandoned and the author(s) do not intend on continuing development.
* <a name="active"></a>__Active__ – The project has reached a stable, usable state and is being actively developed.
* <a name="inactive"></a>__Inactive__ – The project has reached a stable, usable state but is no longer being actively developed; support/maintenance will be provided as time allows.
* <a name="unsupported"></a>__Unsupported__ – The project has reached a stable, usable state but the author(s) have ceased all work on it. A new maintainer may be desired.
* <a name="moved"></a>__Moved__ - The project has been moved to a new location, and the version at that location should be considered authoritative. This status should be accompanied by a new URL.

These status descriptions and the URLs to the corresponding icons are also available in a [JSON file](/badges/latest/badges.json) or in a more formal ontology using [SKOS](https://www.w3.org/TR/skos-reference/), defined in a [JSON-LD file](/badges/latest/ontology.jsonld).

### What It Looks Like

When using the recommended method (a badge embedded in your project's README file), it's as concise as this one image:

[![Project Status: Active – The project has reached a stable, usable state and is being actively developed.](https://www.repostatus.org/badges/latest/active.svg)](https://www.repostatus.org/#active)

This incorporates three components:

1. The image URL, which serves as the machine-readable status identifier. It points to a status-specific image hosted on repostatus.org, and also incorporates a specification version number.
2. Alt-text on the image (this can generally be viewed in a browser by mousing over the image) which begins with the canonical project status ("Project Status: <status name>") and can optionally be followed by a human-readable description of the status, provided by the project's maintainer(s). Such text might also be useful to appear after the badge.
3. The image is linked back to the particular status description on repostatus.org.

### How to Use It

Setting up your project to use RepoStatus.org is as simple as adding the appropriate badge to your project's README file. We define this file as any file at the top level of the project, whose name begin with the (case-insensitive) string 'readme'. When programs check the project status, they will search through any ``/^readme.*$/i`` files in lexicographical order, and choose the first one with a valid repostatus.org status URL in it. If this isn't suitable for your project, there are also some additional options described below ("Machine-Readable Only"). Note that while I've tried to think of this to be as flexible as possible, it's very strongly suggested that the badge appear in a README file rendered on your project's site (such as the readme rendering in GitHub repositories).

Below are the various status icons, along with paste-able markup to add them in a variety of markup languages. Feel free to alter the alt-text (after the first ``-``) to suit your needs.

* __Concept__ [![Project Status: Concept – Minimal or no implementation has been done yet, or the repository is only intended to be a limited example, demo, or proof-of-concept.](https://www.repostatus.org/badges/latest/concept.svg)](https://www.repostatus.org/#concept) [markdown](javascript:showsample('concept','md')) [ReST](javascript:showsample('concept','rst')) [HTML](javascript:showsample('concept','html'))
* __WIP__ [![Project Status: WIP – Initial development is in progress, but there has not yet been a stable, usable release suitable for the public.](https://www.repostatus.org/badges/latest/wip.svg)](https://www.repostatus.org/#wip) [markdown](javascript:showsample('wip','md')) [ReST](javascript:showsample('wip','rst')) [HTML](javascript:showsample('wip','html'))
* __Suspended__ [![Project Status: Suspended – Initial development has started, but there has not yet been a stable, usable release; work has been stopped for the time being but the author(s) intend on resuming work.](https://www.repostatus.org/badges/latest/suspended.svg)](https://www.repostatus.org/#suspended) [markdown](javascript:showsample('suspended','md')) [ReST](javascript:showsample('suspended','rst')) [HTML](javascript:showsample('suspended','html'))
* __Abandoned__ [![Project Status: Abandoned – Initial development has started, but there has not yet been a stable, usable release; the project has been abandoned and the author(s) do not intend on continuing development.](https://www.repostatus.org/badges/latest/abandoned.svg)](https://www.repostatus.org/#abandoned) [markdown](javascript:showsample('abandoned','md')) [ReST](javascript:showsample('abandoned','rst')) [HTML](javascript:showsample('abandoned','html'))
* __Active__ [![Project Status: Active – The project has reached a stable, usable state and is being actively developed.](https://www.repostatus.org/badges/latest/active.svg)](https://www.repostatus.org/#active) [markdown](javascript:showsample('active','md')) [ReST](javascript:showsample('active','rst')) [HTML](javascript:showsample('active','html'))
* __Inactive__ [![Project Status: Inactive – The project has reached a stable, usable state but is no longer being actively developed; support/maintenance will be provided as time allows.](https://www.repostatus.org/badges/latest/inactive.svg)](https://www.repostatus.org/#inactive) [markdown](javascript:showsample('inactive','md')) [ReST](javascript:showsample('inactive','rst')) [HTML](javascript:showsample('inactive','html'))
* __Unsupported__ [![Project Status: Unsupported – The project has reached a stable, usable state but the author(s) have ceased all work on it. A new maintainer may be desired.](https://www.repostatus.org/badges/latest/unsupported.svg)](https://www.repostatus.org/#unsupported) [markdown](javascript:showsample('unsupported','md')) [ReST](javascript:showsample('unsupported','rst')) [HTML](javascript:showsample('unsupported','html'))
* __Moved__ [![Project Status: Moved to http://example.com – The project has been moved to a new location, and the version at that location should be considered authoritative.](https://www.repostatus.org/badges/latest/moved.svg)](https://www.repostatus.org/#moved) [markdown](javascript:showsample('moved','md')) [ReST](javascript:showsample('moved','rst')) [HTML](javascript:showsample('moved','html')) - __Note__ that there are special requirements around the formatting of this status. In the examples, replace ``http://example.com`` with the project's new URL. See [Moved Identifier String](#moved-identifier), below, for more information.

<div id="samplewrapper" style="display: none;"><h5 id="sampletitle"></h5><div id="samplecode"></div></div>

#### Machine-Readable Only

If for some reason you don't want people to see the repostatus.org status identifier (which defeats half the purpose of this idea, but may be valid for some people), you can place just the URL to the status image in a ``.repostatus.org`` or ``repostatus.org`` file in the top-level of your project. Per the specification, programs that determine project status check these files _after_ the README file(s).

### Specification

I really wanted to write a full specification for this, complete with versioned URLs and JSON metadata describing the different statuses. If anyone else in the world wants to use this stuff, maybe I'll do that. In the mean time, here's the current version of the "specification".

For use of the repostatus.org vocabulary in a linked open data context, consult the [JSON-LD file](/badges/latest/ontology.jsonld).

#### Identifier Strings

The repostatus.org badge URL is the authoritative identifier of status. Regardless of any other formatting, when machines attempt to determine status they should only key off of a URL matching ``/^http[s]?:\/\/.*repostatus\.org\/badges\/(.+)\/(.+)\.svg$/``. The first capture group identifies the specification/API version, and the second identifies the status name. Note that the specification/API version can currently be a [semver](http://semver.org/)-compliant string, or the string "latest".

##### <a name="moved-identifier"></a>Moved Identifier String

The "Moved" status is slightly more complicated as it must also specify the new location. Guidelines for use are as follows:

1. If the link is embedded in a markup format that supports alt-text for images (i.e. ReST, Markdown or HTML), the alt-text __must__ begin with the string "Project Status: Moved to <url>" where ``<url>`` is the new URL (where the project was moved to). That string __should__ be followed by a hyphen and then the official status description. The image __must__ remain linked to the appropriate repostatus.org URL. The image markup __may__ be followed by a separate link to the new URL.
2. Markup formats not supporting alt-text for images (i.e. plaintext files) __must__ specify this status in the format "<badge url> to <new url>".
3. If no new URL exists yet, the repository should have the "Abandoned" status instead of "Moved".

Any machine parsing of the "Moved" status should recursively follow repostatus.org identifiers to determine the final location of the project.

#### Machine Location and Parsing

Machine parsing is quite simple: first, search through any files in the top-level directory of the project (ideally on the default branch, usually master for git) matching ``/^readme.*$/i`` (note the case-insensitivity) in lexicographic order. The first one with a match for the identifier string (URL) wins, and the first complete match within the file wins. If no files match, then search for a ``.repostatus.org`` file, and if none is found, a ``repostatus.org`` file. Machine parsing _should_ follow the full specification rather than assuming file names (or assuming that a project's readme will be correctly displayed on GitHub).

There are some example parsers listed on the [parsers](/parsers) page.

### Changelog

See the [CHANGELOG.md on GitHub](https://github.com/jantman/repostatus.org/blob/master/CHANGELOG.md).

### Contributing

This is a crazy idea of mine. But I think it's useful. I'm very open to comments, criticisms, suggestions, etc. Feel free to open an [issue on GitHub](https://github.com/jantman/repostatus.org/issues) or submit a pull request. Instructions for contributing are available [in the README on GitHub](https://github.com/jantman/repostatus.org/blob/master/README.md#contributing). A list of contributors is [also available](https://github.com/jantman/repostatus.org/blob/master/CONTRIBUTORS.md).

### Community Involvement

This project seems to have gained a lot more interest than I thought it would. As of April, 2017 there are [over 1,200 references on GitHub](https://github.com/search?l=&q=http%3A%2F%2Fwww.repostatus.org%2Fbadges%2F+-user%3A%22jantman%22&ref=advsearch&type=Code&utf8=%E2%9C%93)
to repostatus.org badge URLs. I do *not* want to be the sole person making decisions for this project. I encourage everyone who finds
it useful to watch [the repo on GitHub](https://github.com/jantman/repostatus.org) and provide their feedback in discussions, especially the
issues with the [discussion](https://github.com/jantman/repostatus.org/issues?q=is%3Aopen+is%3Aissue+label%3Adiscussion) or
["needs decision"](https://github.com/jantman/repostatus.org/issues?q=is%3Aopen+is%3Aissue+label%3Adiscussion+label%3A%22needs+decision%22)
labels. I'm handling the code updates, but I very much want this project to be driven based on consensus of those who use it.
