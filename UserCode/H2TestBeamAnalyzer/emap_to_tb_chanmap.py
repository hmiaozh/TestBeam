#!/usr/bin/python
#Takes electronics channel map with first two lines as header, properties delimited by spaces, and writes the code for the chanmap in tb_utils.py, to be copied and pasted
import sys

if len(sys.argv) != 2:
    print "Usage: ./emap_to_tb_chanmap.py [emap file]"
else:
    f = open('tb_chanmap.py', 'w')
    filename = sys.argv[1]
    with open(filename, 'r') as inFile:
        lines = inFile.readlines()
        i = -1
        reverse = []
        f.write("chanmap = {}\n")
        f.write("#ieta iphi depth = channelId\n")
        for line in lines:
            l = line.strip()
            #line = line[:-1]
            if l.startswith("#"):
                continue
	    if len(l) > 0:
                    i = i + 1
                    print l
                    channel = l.split()
                    print len(channel),channel
                    ieta = channel[9]
                    iphi = channel[10]
                    depth = channel[11]
                    f.write("chanmap[%s,%s,%s] = %s\n" % (iphi, ieta, depth, i))
                    reverse.append(("chanmap[%s]  = (%s,%s,%s)" % (i, iphi, ieta, depth)))
        f.write("\n")
        for rev in reverse:
            f.write(rev)
	    f.write("\n")
        f.write("\n")
        f.write("chanlist = range(0,%i)\n" % (i+1))
