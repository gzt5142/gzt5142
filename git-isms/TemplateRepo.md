# Template Repository

Custom configurations for your repositories can be standardized with a template. 
This template will influence both new repositories (made with `git init`) as well
as those cloned from a remote (e.g. `git clone https:\\github.com\path-to\repo.git`). This
is true because a clone implicitly calls init, which honors the template setting. 

## Setting up a template

### 1) Set up a template folder

```sh
> cd $HOME
> mkdir .git_template
> cd .git_template
> git init --bare
```

At this point, your .git_template folder has everything that would normally found in
the `.git` folder within any repository on your local host.

### 2) Configure hooks

```sh
> cd $HOME/.git_template
> cd hooks
> rm *.sample
> edit prepare-comit-msg
```

Install or edit other hooks you might like. See [this file](Hooks-prepare-commit-msg.md) for
an example hook to adjust commit messages.

### 3) Configure filters

```sh
> cd $HOME/.git_template
> edit config       ## Define filters you want;
> cd info
> edit attributes   ## define the filter attribute on files you want to filter
```

See [this file](Filters.md) for information on the filters I like to use.

## Set your template as the default for new repos

```sh
> git config --global init.templateDir $HOME/.git_template
```

From now on, any new repositories will have the filter and hook 
configuration that you've set up in the template folder. You can 
override this template with some other template: 
```
git init --template=<template_directory>
```
If you just want the standard, default, (i.e. boring) template, use
the templateDir provided when git was installed.  The documentation
claims that this is in `/usr/share/git-core/templates`, but it may
not be on your system (it isn't in that folder on my MacOS host). 