#!/usr/bin/env python

import sys
import subprocess
import optparse
import re

from runlists import getEmapFromRun

parser = optparse.OptionParser("usage: %prog <input filename> [options]")

parser.add_option('-v', dest="verbose", action="store_true", default=False, help="Runs the analysis in verbose mode.")
parser.add_option('-n', dest="nevents", default="-1", help="Number of events to process.")
parser.add_option('-m', '-e', dest="emap", default=None, help="EMAP file")

options, args = parser.parse_args()

numargs = len(args)
if len(args) != 1:
    print "Usage: h2-tb-analyzer.py <input filename> [options]"
    sys.exit(1)

inputFile = args[0]
inputPattern = re.compile("([0-9]+).root")
m = inputPattern.search(inputFile)
if m:
   runNumber = m.group(1)
else:
   print "### ERROR: Could not extract run number from filename."
   print "### The filename must end in:  xxxxxx.root where xxxxxx is the run number."
   sys.exit(1)

doVerbose = options.verbose

numEvents = 0
if options.nevents.isdigit():
   numEvents = int(options.nevents)
   if numEvents == 0:
        print "Specificying -n 0 processes all events."
   else:
        print "User Limit on number of events to process: ",numEvents   
 

rn = int(runNumber)
prefix = "UserCode/H2TestBeamAnalyzer/"
if options.emap:
    emapFile = prefix + options.emap.split('/')[-1]
    print "Using EMAP: ",emapFile       
else:
    emapFile = prefix + getEmapFromRun(int(runNumber))
    print "No EMAP Specified.  Using EMAP ",emapFile

command = ["cmsRun","h2-tb-analyzer-run.py",inputFile,emapFile,str(int(doVerbose)),str(numEvents),runNumber]
if doVerbose: print "Executing \"%s\"" % " ".join(command) 
subprocess.call(command)

