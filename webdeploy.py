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
import shlex

def main():

    deploy_dir = "/Users/igable/code/webdeploy/"
    ssh_location = "igable@fate-2.phys.uvic.ca:~/public_html/testdeploy/."

    try:
        os.chdir(os.path.dirname(deploy_dir))
    except OSError as e:
        print "Could not prep deployment in " + e.filename
        print "Because: '" + e.strerror + "'"
        sys.exit()
        
    try:
        #remove the directory if it already exists
        checkout = deploy_dir + "bootstrap/"
        shutil.rmtree(os.path.dirname(checkout))
    except OSError:
        print "First time deploy this clearly"

    # need to handle an error if we can't checkout
    gitprocess = subprocess.Popen(["git","clone","/Users/igable/code/bootstrap"],stdout=open(os.devnull, 'w'))
    gitprocess.wait()

    # look for all the .git directories
    findprocess = subprocess.Popen(["find", deploy_dir,  "-type", "d", "-name", ".git"], stdout=subprocess.PIPE)
    findoutput = findprocess.communicate()[0]
    findprocess.wait()

    gitdirs = findoutput.split()

    for gitdir in gitdirs:
        gitdirslash = gitdir + "/"
        shutil.rmtree(os.path.dirname(gitdirslash))
    
    # now copy the files into place with ssh
    os.chdir("bootstrap/")
    sshprocess = subprocess.Popen(["scp","-p","-r"] + os.listdir(os.path.dirname(os.getcwd()+"/")) + [ssh_location], stdout=open(os.devnull,'w'))
    sshprocess.wait()

main()





