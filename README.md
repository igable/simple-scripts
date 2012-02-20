

## texwatcher
texwatcher is a very basic tool for automatically compiling a TeX file with
rubber when that file is changed. The tool was designed for OSX so that you can
use any editor to edit your TeX and have the Mac Preview application pop up
with your most recent changes contained in it.

### Usage

Use the build in help by

    $texwatcher.py --help

## webdeploy.py

webdeploy is can be used to checkout out clone a git repo and scp its
contentents to a webserver after cleaning out the .git directories. It has
losts of hardcoded entries.

### usage

Call it from .git/hooks/post-commit, then edit the script with the directories
you want to deploy to.
