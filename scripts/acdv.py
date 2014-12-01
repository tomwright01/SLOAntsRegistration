#!/usr/bin/python
 
from struct import *
import sys
 
if len(sys.argv) < 2:
    print "Usage: acdv.py <file.avi>"
    sys.exit(1)
 
data = open(sys.argv[1], "rb").read()
 
fileno = 0
for i in xrange(len(data)):
    if data[i:i+4] == '00dc' or data[i:i+4] == '00AC':
        size = unpack('<I', data[i+4:i+8])[0]
        open("%05d.jpg" % (fileno), "wb").write(data[i+8+4:i+8+size])
        fileno = fileno + 1
        i = i + 8 + size