from __future__ import division
import sys
import re
import os
import string
import operator
from model import *
import cPickle as pickle
import numpy
import time

LeftOver = (open(sys.argv[1]).read().splitlines())
inputfile = (open(sys.argv[2]))
testUNKs = pickle.load(inputfile)
inputfile = (open(sys.argv[3]))
trainWords = pickle.load(inputfile)
args = len(sys.argv)
if args > 4:
	printOutInformativeSents = sys.argv[4]
else:
	printOutInformativeSents = None

minSentLength = 3
maxNumberUNKs = 5
if printOutInformativeSents != None:
	maxNumberUNKs = 8
	minSentLength = 5

sentID2origUNKcounts = {}
sentID = -1
sent = []

foundTestUNK = False
for line in LeftOver:
	if len(line.split()) == 0:
		if len(sent) >= minSentLength:
			UNKs = 0
			for line2 in sent:
				word = line2.split()[1]
				if word not in trainWords:
					UNKs += 1
					if UNKs > maxNumberUNKs:
						break
					for priority in testUNKs:
						if word.lower() in testUNKs[priority]:
							foundTestUNK = True
							break
			if foundTestUNK == True and UNKs <= maxNumberUNKs:
				sentID += 1
				sentID2origUNKcounts[sentID] = UNKs
				for line2 in sent:
				
					# pass
					print line2 #+ '\t'+str(UNKs)	
				print
				
		sent = []
		foundTestUNK = False
	else:
		sent.append(line)
	
with open("sentID2origUNKcounts.dat",'w') as of:
		pickle.dump(sentID2origUNKcounts,of)
		
# for i in range(0,len(sentID2origUNKcounts)):
	# print i 
	# print sentID2origUNKcounts[i]
	# print
	# time.sleep(1)
	