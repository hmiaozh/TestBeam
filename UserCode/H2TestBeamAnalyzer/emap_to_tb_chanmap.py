#!/usr/bin/python
#Takes electronics channel map with first two lines as header, properties delimited by spaces, and writes the code for the chanmap in tb_utils.py, to be copied and pasted
import sys

if len(sys.argv) != 2:
    print "Usage: ./emap_to_tb_chanmap.py [emap file]"
else:
    filename = sys.argv[1]
    with open(filename, 'r') as inFile:
        lines = inFile.readlines()
        i = 0
        reverse = []
        print "chanmap = {}"
        print "#ieta iphi depth channelId"
        for line in lines:
            line = line[:-1]
	    line = line.split("#")[0]
	    if len(line) > 0:
            	if i > 1:
                    n = i - 1
                    channel = line.split()
                    ieta = channel[9]
                    iphi = channel[10]
                    depth = channel[11]
                    print "chanmap[%s,%s,%s] = %s" % (ieta, iphi, depth, n)
                    reverse.append(("chanmap[%s]  = (%s,%s,%s)" % (n, ieta, iphi, depth)))
            i = i + 1
        print "\n"
        for rev in reverse:
            print rev
