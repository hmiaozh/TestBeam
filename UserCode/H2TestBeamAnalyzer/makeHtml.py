#!/usr/bin/env python

import sys
import optparse
import commands
import os
import glob

#######################
# Get options
#######################

parser = optparse.OptionParser("usage: %prog [options]\
<input directory> \n")

parser.add_option ('--t', dest='title', type='string',
                   default = 'Plots',
                   help="Title of html page.")
parser.add_option ('--s', dest='size', type='int',
                   default = 500,
                   help="Size of displayed plots.")
parser.add_option ('--rw', dest='rowWidth', type='int',
                   default = -1,
                   help="Size of displayed plots.")
parser.add_option ('--ext', type="string",
                   dest="ext", default="pdf",
                   help="Format of linked image.")
parser.add_option ('--img', type='string',
                   dest="img", default="gif",
                   help="Format of displayed image.")
options, args = parser.parse_args()


if len(args) != 1:
    print "Please specify input dir.  Exiting."
    sys.exit()

indir  = args[0]+"/"
title = options.title
size = options.size
ext = options.ext
img = options.img
rowWidth = options.rowWidth

##############################################
# Check dir
##############################################
if not os.path.isdir(indir) :
    print "Cannot find %s.  Exiting." % infile
    sys.exit()


if title == "make":
    print indir
    sindir = indir.split("/")
    # remove white spaces
    while '' in sindir: sindir.remove('')
    print sindir
    title = sindir[len(sindir)-1]
    print len(sindir)-1
    print title
#if os.path.isfile(indir+"index.html") :
#    print "%s already exists.  Exiting." % indir+"index.html"

files = glob.glob(indir+'*'+ext)
files.sort()

for file in files:
    base = os.path.splitext(file)[0]
    print "Processing", file
    
    command = "convert %s.%s -resize %sx%s %s_small.%s" % (base, img, size, size, base, img)
    #    command = "cp %s.%s %s_small.%s" % (base, img, base, img)
    os.system(command)


os.system("rm -f "+indir+"index.html")
os.system("touch "+indir+"index.html")
findex = open(indir+"index.html","w")

print >> findex, "<h1> "+title+"</h1>"
print >> findex, "<hr>\n"
print >> findex, "<table>"


if rowWidth == -1:
    if int(size) <= 300:
        rowWidth = 3
    else:
        rowWidth = 2
    
nfile = 0
for file in files:
    base = os.path.basename(file).split("."+ext)[0]

    if nfile == 0: print >> findex, "<tr>"
    elif nfile % rowWidth == 0: print >> findex, "</tr>\n<tr>"

    print >> findex, '<td><a href="%s.%s"><img src="%s_small.%s"></a></td>' % (base, ext, base, img)
    nfile += 1

print >> findex, "</tr>\n</table>\n"



findex.close()     
