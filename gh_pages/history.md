---
layout: minimal
---

## History

I have about 50 repositories on GitHub, in varying states of completion and support. Some of them are totally abandoned, some are active (with users and everything!) and some
are just repositories holding a ``README.md`` describing some idea I had. I was about to embark on a new project, and realized I needed to get a handle on what I currently have
first. After some thought, I realized that an awful lot of people are in the same position. And even more so, I can't count the number of times I've dug through a repository -
and even emailed the author - to try and figure out if it was still active or not.

So, I came up with this idea. I had to stop myself before I over-engineered it too much with a formal specification and versioned API and everything.

I originally thought that this should be a feature built-in to GitHub. But for anyone who's seen [isaacs/github](https://github.com/isaacs/github), you know how unlikely
that is, and how ironically secretive GH is about feature requests and fixing bugs, and communication with the community in general. So I [opened an issue](https://github.com/isaacs/github/issues/312)
anyway, but I doubt it will go anywhere. Then I started thinking about how to do this without GitHub involved, which would give the added bonus that it's hosting-service
agnostic (and VCS-agnostic too, so it'll work for that crowd of Mercurial users too).

The blog post where I first laid this out is [here](http://blog.jasonantman.com/2014/12/idea-for-a-generic-method-to-communicate-repositoryproject-status/). Sure, this is a tiny
little thing that is more of a community suggestion than a standard, but it'd sure be nice if we could all easily tell each other what's done and what isn't, and more importantly,
what we want to spend time on again "one day."
