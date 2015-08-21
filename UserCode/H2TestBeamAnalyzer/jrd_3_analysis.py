#!/usr/bin/env python
#run_analysis.py

import subprocess
import sys
import socket
import optparse
import os
import re

#Options

parser = optparse.OptionParser("usage: %prog [options]")

parser.add_option ('-r','--r', type='string', dest="runs",
                   help="Pick a specific run number or range of numbers with Unix globbing - may need to use single quotes or -f before running. NOTE - MUST USE 6 DIGIT RUN NUMBER, add leading zeros as needed.")
parser.add_option ('-d',
                   dest="delete", action="store_true",
                   default=False, help="Delete files after moving to destination")
parser.add_option ('-o','--dest', type='string', dest="outputLoc", help="Destination directory for run results/html. Remote locations ok")
parser.add_option ('--runDest', type='string', dest="runDest", help="Where the run files HTB*.root are to be stored during processing.")
parser.add_option ('-i', type='string',dest="inputLoc",help="Where to find the HTB*.root files.  This can be a network location.")
parser.add_option ('-v', dest="verbose", action="store_true",
                   default=False, help="Runs the analysis in verbose mode. Not recommended on large runs or batches of runs, as verbose output can be quite massive.")
parser.add_option ('-q', dest="mute", action="store_true", default=False, help="Further decreases verbosity.")
parser.add_option ('--all', dest="all", action="store_true", default=False, help="Use --all to run on all files in spool")
parser.add_option ('-f', dest="force", action="store_true", default=False, help="Ignore warnings about run(s) already being staged and proceed with processing run(s)")
parser.add_option ('--clobber', dest="clobber", action="store_true", default=False, help="Overwrite output files if they exist")
parser.add_option ('-u', dest="doUndone", action="store_true", default=False, help="Run analysis on all runs which have not been processed into the destination directory")
parser.add_option ('-c', dest="cmsRun", action="store_true", default=False, help="Run only cmsRun h2testbeamanalyzer_cfg.py and other selected options, default is all on")
parser.add_option ('-a', dest="tb_ana", action="store_true", default=False, help="Run only tb_ana.py and other selected options, default is all on")
parser.add_option ('-p', dest="tb_plots", action="store_true", default=False, help="Run only tb_plots.py and other selected options, default is all on")
parser.add_option ('-m', dest="makeHtml", action="store_true", default=False, help="Run only makeHtml.py and other selected options, default is all on")
parser.add_option ('-s', dest="sync", action="store_true", default=False, help="Only sync and use and other selected options, default is all on")



options, args = parser.parse_args()


all = options.all
delete = options.delete
runDest = options.runDest
runs = options.runs
outputLoc = options.outputLoc
verbose = options.verbose
mute = options.mute
force = options.force
doUndone = options.doUndone
inputLoc = options.inputLoc
cmsRun = options.cmsRun
tb_ana = options.tb_ana
tb_plots = options.tb_plots
makeHtml = options.makeHtml
sync = options.sync
clobber = options.clobber

if len(sys.argv) == 1:
    parser.print_help()
    sys.exit(1)


# Determine the set of runs to be processed.
# If the input argument contains a hyphen, take it to be a range of runs.
# In this case, set the wildcard to '*' but set runList

if all:
    runs = '*'
if not runs:
    print "No runs specified. Use -r or --all"
    sys.exit(1)

runList = []
if '-' in runs:
    lo = runs.split('-')[0]
    hi = runs.split('-')[1]
    if lo.isdigit() and hi.isdigit():
        loRun = int(lo)
        hiRun = int(hi)
        runList = range(loRun,hiRun+1) 
        runs = '*'

print "runDest =",runDest
if not runDest:
    print "fixing runDest"
    runDest = "/home/daq/Analysis/HcalTestBeam/data_spool_mirror"
    if socket.gethostname() is not "cmshcaltb05": runDest = "."

#envTest = subprocess.Popen(['$CMSSW_BASE'], stdout=subprocess.PIPE)
#envTest.wait()
#out = envTest.communicate()
#print out[0]
#if out[0] != "/":
#    print out[0]
#    print "CMS environment not set up."
#    sys.exit(1)

# Run all the steps unless one or more steps is specified

if (cmsRun == False) & (tb_ana == False) & (tb_plots == False) & (makeHtml == False) & (sync == False):
    cmsRun = True
    tb_ana = True
    tb_plots = True
    makeHtml = True
    sync = True

# Determine the first and last steps to run

if sync: firstStep = 4
if makeHtml: firstStep = 3
if tb_plots: firstStep = 2
if tb_ana: firstStep = 1
if cmsRun: firstStep = 0

if cmsRun: lastStep = 0
if tb_ana: lastStep = 1
if tb_plots: lastStep = 2
if makeHtml: lastStep = 3
if sync: lastStep = 4

filePrefixList = ["HTB_","ana_h2_tb_run","ana_tb_out_run","tb_plots_run","tb_plots_run","tb_plots_run"]
fileSuffixList = [".root",".root",".root","","",""]

inputFileFormat = [filePrefixList[firstStep],fileSuffixList[firstStep]]
outputFileFormat = [filePrefixList[lastStep+1],fileSuffixList[lastStep+1]]


# Based on the contents of the input and output directories and command line options, determine which files to process

if not inputLoc:
    inputLoc = "/data/spool"
    if socket.gethostname() is not "cmshcaltb05": inputLoc = "daq@cmshcaltb02.cern.ch:/data/spool"

inputLoginInfo = ""
inputIsRemote = False
if ':' in inputLoc:
    inputIsRemote = True     #if the input location has a colon, assume a network location
    inputLoginInfo = inputLoc.split(':')[0]
    inputLoc = inputLoc.split(':')[1]

inputFileSpec = inputLoc.rstrip('/') + '/' + inputFileFormat[0] + '*' + runs + inputFileFormat[1]
inputCommand = 'ls ' + inputFileSpec
print 'inputCommand = ',inputCommand

# At this point, the following are set: inputLoc, inputLoginInfo, inputIsRemote, inputLoginInfo, inputCommand

if inputIsRemote:
    ls1 = subprocess.Popen(['ssh', inputLoginInfo, inputCommand], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    ls1.wait()
    out, err =  ls1.communicate()
    print out,err
else:
    ls1 = subprocess.Popen(inputCommand, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)    
    ls1.wait()
    out, err =  ls1.communicate()

inputFileList = out.split()
inputFileList.sort(reverse=True)

# If a runList is defined, select only those runs and reset the inputFileList

if len(runList) > 0:
    inputPattern = re.compile(inputFileFormat[0]+"(0*[0-9]+)")
    temp_input_file_list = []
    for oneInputFile in inputFileList:
        m = inputPattern.search(oneInputFile)
        if m:
            runnum = int(m.group(1).lstrip('0'))
            if runnum in runList: temp_input_file_list.append(oneInputFile)
    inputFileList = temp_input_file_list                        

if verbose: 
    print "Attempting to find input files that match:", inputLoginInfo + ':' + inputFileSpec
    if len(inputFileList) == 0:
        print("No files found.")
    else:
        print("\n".join(inputFileList))

#Now check output location        
                                                     
if clobber:
    processFileList = inputFileList

else:

    outputPattern = re.compile(outputFileFormat[0]+"(0*[0-9]+)"+outputFileFormat[1])
            
    if not outputLoc:
        outputLoc = "/hcalTB/Analysis"
        if socket.gethostname() is not "cmshcaltb05": outputLoc = "daq@cmshcaltb05.cern.ch:/hcalTB/Analysis"
    
    outputLoginInfo = ""
    outputIsRemote = False
    if ':' in outputLoc:
        outputIsRemote = True     #if the output location has a colon, assume a network location
        outputLoginInfo = outputLoc.split(':')[0]  #everything before the colon
        outputLoc = outputLoc.split(':')[1]  #everything after the colon

    #Get files from cmshcaltb02
    outputDirectory = outputLoc.rstrip('/')
    outputCommand = 'ls ' + outputDirectory
    
    if outputIsRemote:
        ls2 = subprocess.Popen(['ssh', outputLoginInfo, outputCommand], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        ls2.wait()
        out, err =  ls2.communicate()
    else:
        ls2 = subprocess.Popen(outputCommand, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)    
        ls2.wait()
        out, err =  ls2.communicate()

    outputFiles = out.split()

    runNumbersFoundList = []
    outputExistingFilesList = []                
    for oneFile in outputFiles:
        m = outputPattern.match(oneFile)
        if m: 
            runNumbersFoundList.append(m.group(1).lstrip('0'))
            outputExistingFilesList.append(oneFile)
    
    runNumbersFoundList.sort(reverse=True)
    outputExistingFilesList.sort(reverse=True)

    if verbose:
        print "Files that already appear in the output directory", outputDirectory
        if len(outputExistingFilesList) == 0:
            print("No Files found.")
        else:
            print("\n".join(outputExistingFilesList))

    processFileList = []
    for inputFileName in inputFileList:
        doProcess = True
        for runNumber in runNumbersFoundList:
            if runNumber in inputFileName:
                doProcess = False
                break
        if doProcess: processFileList.append(inputFileName)        
                                                                                                                                                                  
if verbose: 
    print "Planning to process the following input data files:"
    if len(processFileList) == 0:
        print("None.")
    else:
        print("\n".join(processFileList))
    
runNumberPattern = re.compile(inputFileFormat[0]+"(0*[0-9]+)")

for fileName in processFileList:
    runNum = -1
    m = runNumberPattern.search(fileName)
    if m: runNum = m.group(1)
    if runNum == -1: continue
    
    print "Getting run number %s" % runNum
    
    ana = filePrefixList[1] + runNum + fileSuffixList[1]
    ana2 = filePrefixList[2] + runNum + fileSuffixList[2]
    plotsDir = filePrefixList[3] + runNum + fileSuffixList[3]

    # If the input file is remote, we need to make a local copy
    
    if inputIsRemote:
        rsyncPath = inputLoginInfo + ':' + fileName
        print rsyncPath, runDest
        subprocess.call(["rsync", "-av", rsyncPath, runDest])
    
    if cmsRun:
        subprocess.call(["cmsRun", "h2testbeamanalyzer_cfg.py", runNum])
    if tb_ana:
        subprocess.call(["./tb_ana.py", "--i", ana, "--o", ana2, "--r", str(int(runNum))])
        #subprocess.call(["rm", "-rf", plotsDir])
    if tb_plots:
        print "Generating plots for run " + runNum
        subprocess.call(["./tb_plots.py", "--i", ana2, "--o", plotsDir, "--r", str(int(runNum))])
    if makeHtml:
        print "Generating html for run " + runNum
        subprocess.call(["./makeHtml.py", plotsDir])
    #if sync:
    #    print "Moving results of run " + runNum
    #    subprocess.call(["rsync", "-av", "--delete", plotsDir, outputLoginInfo + outputDirectory])
    
quit()


fileList = processFileList

for fileName in fileList:
    name = fileName[12:]
    runNum = fileName[16:-5]
    if len(runNum) == 6:
        print "Getting run number %s" % runNum
        rsyncPath = "daq@cmshcaltb02:%s" % fileName
        if verbose:
            subprocess.call(["rsync", "-av", rsyncPath, runDest])
        else:
            subprocess.call(["rsync", "-aq", rsyncPath, runDest])
        symLinkPath = runDest + '/' + name
        if runDest != '.':
            link = subprocess.Popen(["ln", "-s", symLinkPath, "."], stdout=open(os.devnull, 'wb'), stderr=subprocess.PIPE)
            out, err = link.communicate()
            if err[:2] == "ln":
                if force:
                    print "Warning, run %s has already been staged for processing. -f used, proceeding anyway..." % runNum
                else:
                    print "Warning, run %s has already been staged for processing, skipping." % runNum
                    fileList.remove(fileName)
###########################
#Run analysis
for fileName in fileList:
    name = fileName[12:]
    runNum = fileName[16:-5]
    #Check if file is an HTB*.root file
    if len(name) == 15 and name[:3] == "HTB" and name[-5:] == ".root":
        if cmsRun:
            if verbose:
                subprocess.call(["cmsRun", "h2testbeamanalyzer_cfg_verbose.py", runNum])
            elif 1:
                subprocess.call(["cmsRun", "h2testbeamanalyzer_cfg.py", runNum], stdout=open(os.devnull, 'wb'))
            else:
                subprocess.call(["cmsRun", "h2testbeamanalyzer_cfg.py", runNum])
        ana = "ana_h2_tb_run%s.root" % runNum
        ana2 = "ana_tb_out_run%s.root" % str(int(runNum))
        plotsDir = "tb_plots_run%s" % str(int(runNum))
        if mute:
            if tb_ana:
                subprocess.call(["./tb_ana.py", "--i", ana, "--o", ana2, "--r", str(int(runNum))], stdout=open(os.devnull, 'wb'))
                subprocess.call(["rm", "-rf", plotsDir], stdout=open(os.devnull, 'wb'))
            if tb_plots:
                print "Generating plots for run " + runNum
                subprocess.call(["./tb_plots.py", "--i", ana2, "--o", plotsDir, "--r", str(int(runNum))], stdout=open(os.devnull, 'wb'))
            if makeHtml:
                print "Generating html for run " + runNum
                subprocess.call(["./makeHtml.py", plotsDir], st2dout=open(os.devnull, 'wb'))
            #if sync:
            #    print "Moving results of run " + runNum
            #   subprocess.call(["rsync", "-aq", "--delete", plotsDir, outputLoc], stdout=open(os.devnull, 'wb'))
        else:
            if tb_ana:
                subprocess.call(["./tb_ana.py", "--i", ana, "--o", ana2, "--r", str(int(runNum))])
                subprocess.call(["rm", "-rf", plotsDir])
            if tb_plots:
                print "Generating plots for run " + runNum
                subprocess.call(["./tb_plots.py", "--i", ana2, "--o", plotsDir, "--r", str(int(runNum))])
            if makeHtml:
                print "Generating html for run " + runNum
                subprocess.call(["./makeHtml.py", plotsDir])
                subprocess.call(["./makeMenu.sh", plotsDir])
            #if sync:
            #    print "Moving results of run " + runNum
            #    subprocess.call(["rsync", "-av", "--delete", plotsDir, outputLoc])
        subprocess.call(["rm", name])
        if delete:
            subprocess.call(["rm", ana])
            subprocess.call(["rm", ana2])
            subprocess.call(["rm", "-rf", plotsDir])
        if sync:
            print "Finished processing run %s. Results at http://cmshcalweb01.cern.ch/hcalTB/Analysis/%s" % (runNum, plotsDir)
