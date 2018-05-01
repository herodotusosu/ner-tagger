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

minSentLength = 3
maxNumberUNKs = 8

sentID2origUNKcounts = {}
sentID = -1
sent = []

if sys.argv[4] != '-rest':
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
						print line2
					print
			sent = []
			foundTestUNK = False
		else:
			sent.append(line)
		
	with open("sentID2origUNKcounts.dat",'w') as of:
			pickle.dump(sentID2origUNKcounts,of)
			
else:
	LO = (open(sys.argv[5]).read().splitlines())
	
	sents = []
	sent = []
	for line in LO:
		if len(line.split()) > 0:
			word = line.split()[1]
			sent.append(word)
		else:
			sents.append(sent)
			sent = []
	if sent != []:
		sents.append(sent)

	sent = []
	printlines = []		
	for line in LeftOver:
		if len(line.split()) > 0:
			word = line.split()[1]
			sent.append(word)
			printlines.append(line)
		else:
			if sent in sents:
				sents.remove(sent)
				# print 'FOUND ONE'
				# print sent
				# print
				# time.sleep(3)
			else:
				for l2 in printlines:
					print l2
				print		
			sent = []
			printlines = []
	if sent != []:
		if sent not in sents:
			for l2 in printlines:
				print l2
