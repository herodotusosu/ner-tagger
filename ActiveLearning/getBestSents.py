from __future__ import division
import sys
import string
from model import *
import time

orderedTest = (open(sys.argv[1]).read().splitlines())
sentsAtATime = int(sys.argv[2])
option = sys.argv[3]

i = 0

if option == '-train':
	for line in orderedTest:
		if len(line.split()) > 0:
			print line
		else:
			print
			i += 1
			if i >= sentsAtATime:
				break
				
if option == '-leftOver':
	for line in orderedTest:
		if len(line.split()) > 0:
			if i >= sentsAtATime: 
				print line
		else:
			if i >= sentsAtATime:
				print
			i += 1