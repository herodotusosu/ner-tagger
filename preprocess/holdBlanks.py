#!/usr/bin/env python

### run with "cat name_of_file.html | python ../perseusExtractor.py"
import sys
import string

output = {}

for line in sys.stdin:
	if len(line.split()) != 0:
		print line
	else:
		print 'LEAVEBLANK'
