---
layout: minimal
---

### What It Is

Many people and organizations have publicly available code in varying states of usability, development (whether or not further development is planned), and support (whether bugfixes and user assistance will be given). With the increased popularity of code sharing sites such as GitHub, Gitorious, etc. it's becoming even more common for new projects to be shared publicly from the time of the first commit, and for projects to continue being publicly accessible long after development and support have ceased. So far, there seem to be few if any methods of clearly indicating the usability and development/support status of a project. At best, tagging and releases (even when using [semver](http://semver.org/) properly) only differentiate between code that the author deems to be production-ready versus pre-release (and even the definition of pre-release states vary widely). There is no accepted way of indicating the development or support status of a project, specifically whether or not further development is planned and whether support will be provided. Repostatus.org aims to fill this gap by providing an easy-to-use method of communicating the usability and development/support status of a project to both humans and machines.

This is accomplished by including a simple badge or URL in your project's README file, or by including a link in a specially-named file inside your project. The badge is easily visible to humans, and machines can determine the project's status by searching for a string matching a specific pattern (in a set list of possible files). We define a list of possible project statuses which aim to encompass axes of both code completion and development/support status (future plans), in a simple and user-centric manner.

#### Project Statuses

here. need anchors to them...

### What It Looks Like

When using the recommended method (a badge embedded in your project's README file), it's as concise as this one image:

[![Alt Text](/image/path)](link_url_to_status)

This incorporates three components:
1. The image URL, which serves as the machine-readable status identifier. It points to a status-specific image hosted on repostatus.org, and also incorporates a specification version number.
2. Alt-text on the image (this can generally be viewed in a browser by mousing over the image) which begins with the canonical project status ("Project Status: <status name>") and can optionally be followed by a human-readable description of the status, provided by the project's maintainer(s). Such text might also be useful to appear after the badge.
3. The image is linked back to the particular status description on repostatus.org.

### How to Use It

Setting up your project to use RepoStatus.org is as simple as adding the appropriate badge to your project's README file. We define this file as any file at the top level of the project, whose name begin with the case-insensitive string 'readme'. When programs check the project status, they will search through any ``/readme*/i`` files in lexicographical order, and choose the first one with a valid repostatus.org status URL in it. If this isn't suitable for your project, there are also some additional options described below ("Machine-Readable Only").

Below are the various status icons, along with paste-able markup to add them in a variety of markup languages. Feel free to alter the alt-text (after the first ``-``) to suit your needs.

images here, with links. ideally I'd like some sort of JS markup thingy, so we'll see what we can do about that.

#### Machine-Readable Only

If for some reason you don't want people to see the repostatus.org status identifier (which defeats half the purpose of this idea, but may be valid for some people), you can place just the URL to the status image in a ``.repostatus.org`` or ``repostatus.org`` file in the top-level of your project. Per the specification, programs that determine project status check these files _after_ the README file(s).

### Specification

The full technical specification is available on GitHub. The gist of it is as follows:

#### Identifier Strings

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam ex dolor, lacinia vel elementum rhoncus, blandit nec nunc. Nunc in ultrices ex, quis laoreet dui. Donec condimentum purus in dui sagittis, at facilisis ipsum pellentesque. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi rutrum congue tempus. Praesent tempus at ex et vestibulum. Integer lacinia sed ipsum eget volutpat. Proin eu nisl nec erat porta consectetur in eget ex.

#### Machine Location and Parsing

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam ex dolor, lacinia vel elementum rhoncus, blandit nec nunc. Nunc in ultrices ex, quis laoreet dui. Donec condimentum purus in dui sagittis, at facilisis ipsum pellentesque. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi rutrum congue tempus. Praesent tempus at ex et vestibulum. Integer lacinia sed ipsum eget volutpat. Proin eu nisl nec erat porta consectetur in eget ex.
