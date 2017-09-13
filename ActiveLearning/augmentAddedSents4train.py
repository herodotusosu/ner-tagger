from __future__ import division
import sys
import string
from model import *
import time

train = (open(sys.argv[1]).read().splitlines())
addedSents = (open(sys.argv[2]).read().splitlines())
proportion = float(sys.argv[3])

origLength = 0
for line in train:
	print line
	if len(line.split()) > 0:
		origLength += 1
		

		
addedSentCount = 0
sent = []

while ((addedSentCount)/(addedSentCount + origLength)) < proportion:
	for line in addedSents:
		if len(line.split()) > 0:
			sent.append(line)
			addedSentCount += 1
		else:
			if ((addedSentCount)/(addedSentCount + origLength)) < proportion:
				for line in sent:
					print line
				print
			else:	
				addedSentCount += 10000000000000
				break
			sent = []