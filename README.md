Author: Ian Gable <igable@uvic.ca>


## texwatcher

texwatcher is a basic tool for automatically compiling a TeX file with rubber
when that file is changed. The tool was designed for OSX so that you can use
any editor to edit your TeX and have the Mac Preview application pop up with
your most recent changes contained in it.

### Usage

Use the built in help by

    $texwatcher.py --help

## webdeploy.py

webdeploy is can be used to clone a git repo and scp its contentents to a
webserver after cleaning out the .git directories. It could also be modified to
use rsync. Using rsync is probably better then this script.

### usage

Call it from .git/hooks/post-commit. You can see the built in help with

    $webdeploy.py --help

## condor_plot

A perl script that makes a histogram of the number of completed Condor jobs
with a day wide bin. Everything is hardcoded into the script. You have to read
the source to figure out how to use it.

## benchmark-buf.py

Reads and wirtes a file with  with python IO with different buffer sizes. It
outputs the time required for the various buffer sizes

    $ benchmark-buf.py --help

## License

This program is free software; you can redistribute it and/or modify
it under the terms of either:

a) the GNU General Public License as published by the Free
Software Foundation; either version 3, or (at your option) any
later version, or

b) the Apache v2 License.
