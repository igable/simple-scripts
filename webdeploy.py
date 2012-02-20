#!/usr/bin/python


# Author: Ian Gable
#
# Simple script to allow the deployment of a simple website from
# a git post-update script.
#

import sys
import os
import subprocess
import shutil
import re
from optparse import OptionParser

def main():


    parser = OptionParser(usage="%prog -t TEMPDIR -s SERVERDESTINATION -r REPOSITORY",version = "%prog 0.1")
    parser.add_option("-t", "--temp-dir", dest="tempdir",
            help="The temp directory to perform the checkout into prior to the scp", 
            metavar="TEMPDIR")
    parser.add_option("-s","--server-destination", dest="serverdestination",
            help="The scp string for the location of your server for example joe@server.com:/home/joe/www/",
            metavar="SERVERDESTINATION")
    parser.add_option("-r","--repository", dest="repository",
            help="The location of the git repo", metavar="REPOSITORY")

    (options,args) = parser.parse_args()

    if not options.tempdir:
        parser.print_help()
        parser.error("You must specify a temp directory.")
    if not options.serverdestination:
        parser.print_help()
        parser.error("You must provide a server destination.")
    if not options.repository:
        parser.print_help()
        parser.error("You must provide a repository location.")

    deploy_dir = options.tempdir
    ssh_location = options.serverdestination
    repository = options.repository

    try:
        os.chdir(os.path.dirname(deploy_dir))
    except OSError as e:
        print "Could not prep deployment in " + e.filename
        print "Because: '" + e.strerror + "'"
        sys.exit()
        
    try:
        #remove the directory if it already exists
        checkout = deploy_dir + "cleandeploy/"
        shutil.rmtree(os.path.dirname(checkout))
    except OSError as e:
        print "First time you've deploy this clearly"

    # need to handle an error if we can't checkout
    gitprocess = subprocess.Popen(["git","clone",repository,"cleandeploy"],
            stdout=open(os.devnull, 'w'))
    gitprocess.wait()

    # look for all the .git directories
    # could probably replace this with a native python search
    findprocess = subprocess.Popen(["find", deploy_dir,  "-type", "d", "-name", ".git"], 
            stdout=subprocess.PIPE)
    findoutput = findprocess.communicate()[0]
    findprocess.wait()

    gitdirs = findoutput.split()

    for gitdir in gitdirs:
        gitdirslash = gitdir + "/"
        shutil.rmtree(os.path.dirname(gitdirslash))

    try:
        os.chdir("cleandeploy/")
    except OSError as e:
        print e
        print "Something just removed the directory we checked out."
        sys.exit()

    # TODO: Check the ssh return code
    # now copy the files into place with ssh
    sshprocess = subprocess.Popen(["scp","-p","-r"] + os.listdir(os.path.dirname(os.getcwd()+"/")) 
            + [ssh_location], stdout=open(os.devnull,'w'))
    sshprocess.wait()

main()





