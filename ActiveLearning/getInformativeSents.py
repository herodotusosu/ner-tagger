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
TrainLength  = int(sys.argv[3])
recursivelyAddedPortion = (float(sys.argv[4])/100)
inputfile = (open(sys.argv[5]))
sentID2origUNKcounts = pickle.load(inputfile)

priorities = []
freqs = []
origUNKcounts = []
MPimprovs = []
sentProbs = []
allLists = []

for sid in sentID2tUNK2listStats:
	for tUNK in sentID2tUNK2listStats[sid]:
		l = sentID2tUNK2listStats[sid][tUNK]
		l.append(sid)
		allLists.append(sentID2tUNK2listStats[sid][tUNK])

""" 
x[0] = priority
x[1] = freqs
x[2] = MPi
x[3] = origUNKcounts
x[4] = sentProbs
THE LAST NUMBER LISTED WILL GET HIHGEST PRIORITY IN SORTING
 """		
allLists = sorted(sorted(sorted(sorted(sorted(allLists, key = lambda x : x[4], reverse = True), key = lambda x : x[2], reverse = True), key = lambda x : x[3]), key = lambda x : x[1], reverse = True), key = lambda x : x[0])

wordsLeft = int(float(TrainLength)*float(recursivelyAddedPortion))
usedSIDs = []

######### WRITE OUT NEW UNSUPERVISED FILE AS TRAINNEW.FTRS ####

count = 0
with open('trainNew.ftrs', 'w') as output:
	for l in allLists:
		if wordsLeft > 0:
			usedSIDs.append(l[6])
			for line in l[5]:
				output.write(line+'\n')
				wordsLeft -= 1
			output.write('\n')

####### PRINT OUT NEW LEFTOVERUNANNOTATED.FTRS ################
			
oldSIDs2newSIDs = [] # each item = embedded list [oldID,newID]

oldSID = 0	
newSID = 0
for line in LeftOverWithFeatsAdded:
	if len(line.split()) == 0:
		oldSIDs2newSIDs.append([oldSID,newSID])
		if lastIn == True:
			print
			newSID += 1
		oldSID += 1
	elif oldSID not in usedSIDs:
		print line
		lastIn = True
	else:
		lastIn = False
	
############## MAP OLD SIDS TO NEW SIDS ###################	

sentID2origUNKcounts2 = {}
for entry in oldSIDs2newSIDs:
	oldSID = entry[0]
	newSID = entry[1]
	orgUNKs = sentID2origUNKcounts[oldSID]
	sentID2origUNKcounts2[newSID] = orgUNKs

""" HERE WE PICKLE OUT DICT OF ORIG UNK COUNTS UPDATED WITH NEW SENT LINES IN NEW LEFTOVERUNANNOTATED """
with open("sentID2origUNKcounts2.dat",'w') as of:
		pickle.dump(sentID2origUNKcounts2,of)

###############################################################

	
	