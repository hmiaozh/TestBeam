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
                   default = 400,
                   help="Size of displayed plots.")
parser.add_option ('--rw', dest='rowWidth', type='int',
                   default = 3,
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
    sys.exit(1)

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
    sys.exit(1)

print "Input directory: " + indir
os.chdir(indir)

#if os.path.isfile("index.html") :
#    print "%s already exists.  Exiting." % indir+"index.html"

if title == "make":
    print indir
    sindir = indir.split("/")
    # remove white spaces
    while '' in sindir: sindir.remove('')
    print sindir
    title = sindir[len(sindir)-1]
    print len(sindir)-1
    print title

# generate HTML code and prepare thumbnails
html = ""
html += "<html>\n"
html += "<head>\n"
html += "<title>" + title +"</title>\n"
html += "</head>\n"
html += "<body>\n"
html += "<h1>" + title + "</h1>\n"
html += "<hr>\n"

files = glob.glob('*' + ext)
files.sort()

for file in files:
    print "Processing", file
    
    base = os.path.splitext(file)[0]
    fname = "%s.%s" % (base, img)
    fsmall = "%s_small.%s" % (base, img)
    flink = "%s.%s" % (base, ext)
    
    command = "convert %s -resize %sx%s %s" % (fname, size, size, fsmall)
    os.system(command)
    html += '<a href="%s"><img src="%s"></a>\n' % (flink, fsmall)

html += "</body>\n"
html += "</html>\n"

# write out the index.html content
findex = open("index.html", "w")
findex.truncate()
findex.write(html)
findex.close()

