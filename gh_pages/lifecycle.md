---
layout: minimal
---

## Lifecycle

You can think of respostatus as a way to describe the lifecycle-phase of a project. This may help you to choose an appropriate status for your repositories.

Repostatus aimes to answer two questions about a repository:

* How complete is this? Should I expect it to be "stable" software, mostly working, or not really useful at all?
* Should I expect active development and support, maybe some bug fixes, or nothing at all?

We wish to talk about whether the content of a repository is in a usable state and how much support from contributors can be expected. Thus statuses can be divided along two metrics: usableness and support.

![Flowdiagram representation of a typical lifecycle.](/images/lifecycle.png)

As illustrated above the statuses of a repository can be split into two groups: unstable repos and stable repos.

### Unstable repos

These repositories have not yet reached a stable and usable state. You should expect them to change frequently and dramatically.

All repositories start as a Concept. They are little more than an idea yet. From here we might abandone the project or start to work on it in ernest. Only once a repository was a WIP can it be suspended, work on it be put aside t be continued later. To reach a stable state some work is needed thus WIP is the only state from which we can feasibly move towards a stable state.

### Stable repos

A repository will reach a stable state as something that is actively worked on. Thus all repositories will move into the second group of states as Active. From here they might become Inactive or Unsupported. Contrary to the unstable states it is totally feasable for a repository to move from any stable state into any other stable state.

### Moved

A special case is the *Moved* state for repositories. Any repository can move to be *Moved* from any state. As this states indicates that another repository will contain the actual state of the project.

## Real life application

Understanbly many repositories will not stricktly follow the lifecycle outlined here. When a few commits move a repo from *Suspended* to *Active* it is understandable that maintners might not want to make another commit just to move it to *WIP*.

We fully understand that states as outlined here will be skipped. Therefore the lifecycle hopes to outline a way of thinking about the status of a repository and help choose an appropriet status.
