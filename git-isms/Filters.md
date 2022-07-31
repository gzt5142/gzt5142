# Filters

Filters are a super-powerful part of the local repository's attributes (see https://git-scm.com/docs/gitattributes).

A properly configured filter can modify a file on its way into and out of the repository. Suppose you want to ensure that
your code file does not have trailing white space on any lines. That file can be filtered as it goes into and out of the
repository, which is one way of enforcing the no-trailing-whitespace policy automatically.  (There are other ways, arguably
better for this particular example, using git 'hooks').

## Use Case

I like this feature for cleaning up jupyter notebooks as they are beeing checked into the repository.  In particular, I want
checked-in notebooks to have all of their output cells cleared on their way to the repo. Because the notebook contains code
as well as its output, merely re-running a notebook (with no code changes) will result in a modified notebook file. (Output cells
contain metadata, including a datestamp.  The end result is that a notebook will show change under many conditions in which
no actuall code was changed.)  Further, notebooks with image outputs (from matplotlib, hvplot, etc) will occupy a fair bit
of storage. Sometimes you'll care about that disk space and network bandwidth; other times you won't.  I usually do, so I like
to strip these outputs.

## Terminology

**git** can filter files on their way into, as well as out of, the repository. A separate filter applies to each action. The keywords
to know here are `clean` and `smudge`.

* **clean** : Filter a file on its way _into_ the repo. A clean filter is used whenever the file is checked in (i.e. committed),
  but it **DOES NOT** affect the 'working' copy you have in your file tree.
* **smudge** : Filter a file on its way _out of_ the repo. This can be useful to convert files from one format to another, or to
  execute some other custom command against the file itself.

Both filters read from STDIN and write to STDOUT.

## Security Concerns

Because this configuration will be executing arbitrary code as the filter process, it is not carried with the repository itself.  If it were, then
whoever checked out or forked the repo would be running your filter on their machine without their permission or knowledge.
For this reason, configuration is made only on the LOCAL repo by each developer.

## Define the Filter

Place these lines in the `.git/config` file within your repo:

```txt
[filter "remove-notebook-output"]
        clean = "jupyter nbconvert --clear-output --to=notebook --stdin --stdout --log-level=ERROR"
```

This defines a filter with the name `remove-notebook-output`, and specifies what command to run.  Note that this particular filter
runs only on clean (i.e. _commit_ / _checkin_).  That's what we want in this case.

## Associate the filter with files

Place this line in the `.git/info/attributes` file within your repo:
```
*.ipynb filter=remove-notebook-output
```

The attribute file is similar to `.gitignore` in that you can specify a specific glob pattern to match some files but not others.
For example:

```txt
examples/*.ipynb filter=remove-notebook-output
```

This would filter only those notebooks found in the `examples/` folder, but would not filter notebooks found elsewhere in the repo.

## Usage

No new commands or behavior.  This is all automatic to the commit process, which is its key advantage. Some behavioral notes:

* This filters data as it goes into the repo; it does **not** modify the active notebook in your file tree. This means that the
  output is not purged from your local copy as you work on it.
* A checkout operation (like switching into this branch) will retrieve the file from the repo, which is to say that it will
  retrieve the filtered/cleaned result (since that's what is stored in the repo).
* Your local copy (containing output cells) will persist through many git operations:
  - git commit
  - git push
  - git fetch
  - git pull (so long as this notebook is not among the changed files to be reconciled)
* If you switch branches, the notebook is retrieved from the repo, which means you get the cleaned version. Note that it got
  clean on its way into the repo, not on its way out.
* This mechanism spawns a sub-process for the filter and a pair of pipes
  to plumb STDIN and STDOUT.  If you are committing or merging a bunch of notebooks, expect significant delay during the commit. 

## Long-term usage

This configuration is per-repository, and lives only on your local copy.
If you want it to be a standard thing for all of your local repos, then you'll want to create a template folder structure for git to use when it inits a new repo.
