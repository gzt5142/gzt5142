# Git Hooks

Hooks can do a lot of things related to the git workflow. It is possible to run custom scripts before and after key events
like merges and commits. This example, we will intercept the commit message just prior to moment when the commit goes into
the repository.

The key hook we'll work with is `prepare-commit-msg`.  All hooks are **LOCAL** to your copy of the repository, found in
the `hooks` folder within `$GIT_DIR`.  That typically is in `.git/hooks`.  The scripts here are named for the moment in the
workflow when they are called.

## Create the hook script

Copy this into `<repo_dir>/.git/hooks/prepare-commit-msg`:

```sh
#!/bin/sh

## We will take an environment variable ISSUE_NO if it exists.
## If not, we will attempt to derive it from the branch name. 
if [ XX = X${ISSUE_NO}X ]; then
  BRANCH_NAME=$(git symbolic-ref --short HEAD)
  ISSUE_NO=$(echo $BRANCH_NAME | sed -n 's/^[^0-9]*-\([0-9]*\).*/\1/p')
fi

if [ XX = X${ISSUE_NO}X ]; then
  # No issue number known. 
  exit 0
fi

sed -i.bak "1s/^/[#$ISSUE_NO]: /" "$1"
```

Make sure that this script has the execute bit set on it (`chmod a+x prepare-commit-msg`).

This script will run any time a commit message is prepared by git. Note that this is designed for use on a unix-like system like
Linux or MacOS.  Have not tested on Windows (yet).

## Usage Notes

* If you set an environment variable `ISSUE_NO`, this will be prepended to every commit message.
* If you are working on a branch with a 'standard' branch name which includes an issue number, the script will try to find it. It is
  currently set upu to find issue number if the branch name starts with 'xx-000'. This is the WIM convention of using one's initials followed
  by a dash, followed by an issue number.  The rest of the branch name can be anything.
* If `ISSUE_NO` is set by either of the above two methods, then it is used to prepend a string to the commit message.
