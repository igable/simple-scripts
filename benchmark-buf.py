#!/usr/bin/python

#
# Author: Ian Gable <igable@uvic.ca>
#
# Script that checks write time for different read buffer sizes
#

import sys
import os
import time
from optparse import OptionParser


parser = OptionParser(usage="%prog -i INFILE -o OUTFILE",version = "%prog 0.1")
parser.add_option("-i", "--infile", dest="infile",
                                    help="The file to read from", metavar="INFILE")
parser.add_option("-o","--outfile",dest="outfile",
                                    help="The file to write to", metavar="OUTFILE")
parser.add_option("-b", action="store_true", dest="isbinary", default=False)
(options, args) = parser.parse_args()

isbinary = options.isbinary

if not (options.outfile and options.infile):
    parser.print_help()
    parser.error("")

#buffersizes doubling starting with 1 KB
buffers = [2**13, 2**14, 2**15, 2**16, 2**17, 2**18, 2**19, 2**20, 2**21, 2**22, 2**23, 2**24, 2**25]

src = options.infile
outfile = options.outfile


#src = "/tmp/datain"
#outfile = "/tmp/dataout"

for bufsize in buffers:
    fin=open(src,'r')

    if isbinary:
        fout=open(outfile,'wb')
    else:
        fout=open(outfile,'w')
    
    start = time.time()
    
    while True:
        buf=fin.read(bufsize)
        # In this tight loop I don't think you want logging
        #logging.debug("Read %d bytes from %s" % ( len(buf),src))
        if len(buf)==0:
            break
        fout.write(buf)
        #md5.update(buf)
        #totalBytes+=len(buf)
    fout.close()
    fin.close()
    
    elapsed = time.time() - start
    print "The elepsed time for buffer "+ str(bufsize/8192) + " KB: " + str(elapsed) + " s"
    
