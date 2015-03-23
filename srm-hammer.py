#!/usr/bin/python

#
# Don't use this highly brittle script for
# anything.
#
#

import subprocess
import sys
import os
import shlex
import time
import random
from optparse import OptionParser

class SRMFile:
    
    def __init__(self,filepath):
        self.filepath = filepath.rstrip()
        self.filename = os.path.basename(self.filepath).rstrip()
        self.process = ""
        self.isstarted = False
        self.command = ""
        self.start_time = 0.0

    def filename(self):
        return self.filename

    def getprocess(self):
        return self.process

    def get_command(self):
        return self.command

    def get_start_time(self):
        return self.start_time

    def start(self):
        #self.process =subprocess.Popen(["sleep",str(random.randint(1,10))])
        self.command =  "%s %s %s" % ("lcg-cp", self.filepath, self.filename )
        print self.command
        self.start_time = time.time()
        self.process = subprocess.Popen(["lcg-cp", self.filepath, self.filename ])
        self.isstarted = True

    def kill(self):
        try:
            self.process.kill()
            print "Killed: %s" % self.command
        except (OSError):
            print "Failed to kill %s" % self.command

    def isstarted(self):
        return self.is_started

    def isdone(self):
        if self.process:
            return self.process.poll()
        else:
            return None
        

def printstatus(waiting, running, finished):
    print "%s %s %s" % (waiting, running, finished)     

def main():
    try:
        threads = 1
        filelist = ""
        parser = OptionParser(usage="%prog -f FILELIST -t NUMTHREADS",version = "%prog 0.1")
        parser.add_option("-f", "--file-list", dest="filelist",
        help="list of files to transfer", metavar="FILELIST")
        parser.add_option("-t","--threads",dest="threads",
        help="the number of transfers to do in parallel", metavar="NUMTHREADS")
        (options, args) = parser.parse_args()
        if not options.filelist:
            parser.print_help()
            parser.error("You must specify a file list")
        if not options.threads:
            options.threads = 1
        if not os.path.exists(options.filelist):
            parser.print_help()
            parser.error("The file: " + options.filelist + " does not exist.")
        
        filelist = options.filelist
        threads = int(options.threads)

    except:
        raise

    files =  []
    waiting = []
    running = []
    finished = []
    timeout = 60.0
    print "Running %s threads" % threads
    with open(filelist) as f:
        files = f.readlines()

    for file in files:
        waiting.append(SRMFile(file))

    while len(waiting) or len(running):
        for transfer in running:
            if 0 == transfer.isdone():
                finished.append(transfer)
            if (time.time() - transfer.get_start_time()) > timeout:
                transfer.kill()
                finished.append(transfer) 
    
        for transfer in finished:
            if running.count(transfer):
                running.remove(transfer)
                printstatus(len(waiting), len(running), len(finished))

        while (len(running) < threads) and (len(waiting) > 0):
            current = waiting.pop()
            current.start()
            running.append(current)
            printstatus(len(waiting), len(running), len(finished))
        time.sleep(1);
        
    for transfer in finished:
        stdoutdata = ""
        stderrdata = ""
        (stdoutdata, stderrdata) = transfer.getprocess().communicate()
        if stdoutdata or stderrdata:
            print transfer.command()
            print "Output this:"
            print stdoutdata
            print stderrdata        
        

main()
