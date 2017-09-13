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
import math

inputfile = (open(sys.argv[1]))
sentID2tUNK2listStats = pickle.load(inputfile)
LeftOverWithFeatsAdded = (open(sys.argv[2]).read().splitlines())
wordsLeft  = int(sys.argv[3])
thisDoesntMatter = wordsLeft

priorities = []
freqs = []
origUNKcounts = []
MPimprovs = []
sentProbs = []
allLists = []
tUNKs2freqs = {}
priority2tok2freqs = CondModel('')

for sid in sentID2tUNK2listStats:
	for tUNK in sentID2tUNK2listStats[sid]:
		l = sentID2tUNK2listStats[sid][tUNK]
		""" WIEGHT FREQ BY PRIORITY """
		weightedFreq = int(l[1] / l[0])
		while tUNK[-1] == '*':
			tUNK = tUNK[0:-1]
		tUNKs2freqs[tUNK] = l[1]
		l.append(weightedFreq)
		l.append(sid)
		l.append(tUNK)
		allLists.append(l)
		
		
		if int(l[0]) == 1:
			p = 1
		if int(l[0]) == 2:
			p = 2
		priority2tok2freqs[p][tUNK] = l[1]

# print 'high priority'		
# print len(priority2tok2freqs[1])
# tokens = 0
# for x in priority2tok2freqs[1]:
	# tokens += priority2tok2freqs[1][x]
# print tokens
		
# print 'low priority'		
# print len(priority2tok2freqs[2])
# tokens = 0
# for x in priority2tok2freqs[2]:
	# tokens += priority2tok2freqs[2][x]
# print tokens

# while True:
	# pass
			
		
""" 
x[0] = priority
x[1] = freqs
x[2] = MPi
x[3] = origUNKcounts
x[4] = sentProbs
x[-3] = freqs/priority
THE LAST NUMBER LISTED WILL GET HIHGEST PRIORITY IN SORTING
 """	
 
allLists = sorted(sorted(sorted(sorted(sorted(sorted(allLists, key = lambda x : x[1], reverse = True), key = lambda x : x[4]), key = lambda x : x[3]), key = lambda x : x[0]), key = lambda x : x[2]), key = lambda x : x[-3], reverse = True)

######### WRITE OUT NEW UNSUPERVISED FILE AS TRAINNEW.FTRS ####

### First pass: 1 for each unique word ranked by priority, then freq, then MPi

usedSIDs = []
counter = 0

while counter < len(allLists):
	counter += 1
	usedWords = []
	for l in allLists:
		if l[-2] not in usedSIDs:
			tUNK = l[-1]
			if tUNK not in usedWords:
				# newSID = wordsLeft - sentsLeft + 1
				# header = 'Sent#'
				# header += str(newSID)+'	TestUNK: '+l[-1]+'	Priority: '+str(l[0])+'	MP+MedMPfromTest: '+str(l[2])+'	SP: '+str(l[4])+'	freq: '+str(l[1])+'	totalUNKs: '+str(l[3])
				# print header
				for line in l[5]:
					print line
				print
				# sentsLeft -= 1
				usedSIDs.append(l[-2])
				usedWords.append(tUNK)
			
###############################################################

### Finish writing this later if I decide adding multiple sents for some testUNKs is not repetitive			
# if sentsLeft > 0:
	# usedWords = []
	# neglectedSents = []
	# for l in allLists:
		# currentFreq = l[-3]
		# if currentFreq != pastFreq:
			

	
		# else:
			# if l[-2] not in usedSIDs:
				# tUNK = l[-1]
				# if tUNK not in usedWords:
					# newSID = wordsLeft - sentsLeft + 1
					# header = 'Sent#'
					# header += str(newSID)+'	TestUNK: '+l[-1]+'	Priority: '+str(l[0])+'	MP-MedMPfromTest: '+str(l[2])+'	SP: '+str(l[4])+'	freq: '+str(l[1])+'	totalUNKs: '+str(l[3])
					# print header
					# for line in l[5]:
						# print line
					# print
					# sentsLeft -= 1
					# usedSIDs.append(l[-2])
					# usedWords.append(tUNK)	
				# else:
					# neglectedSents.append(l)
		
		
		
		
		
		# pastFreq = currentFreq
		
		
		
		
		
		