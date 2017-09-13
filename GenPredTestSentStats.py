from __future__ import division
import sys
import re
import os
import string
import operator
from model import *
import cPickle as pickle
import time
import numpy
import math

LeftOverUnannotated = (open(sys.argv[1]).read().splitlines())
inputfile = (open(sys.argv[2]))
sentID2origUNKcounts = pickle.load(inputfile)
# LeftOverOrigUNKs  = (open(sys.argv[2]).read().splitlines())
LeftOverPred  = (open(sys.argv[3]).read().splitlines())
TestPred = (open(sys.argv[4]).read().splitlines())
inputfile = (open(sys.argv[5]))
TestUNKs = pickle.load(inputfile)
Test = (open(sys.argv[6]).read().splitlines())
train = (open(sys.argv[7]).read().splitlines())
easy = sys.argv[8]
if easy == 'True':
	easy = True
else:
	easy = False

""" get median margProbs of all TestUNKs in Test set """
sentID = -1
wordID = -1
sent = []
more = 0
TestUNKs2MPs = {}

if easy == False:
	for i in range(0, len(Test)):
		if '@probability' in TestPred[i+more]:
			sentID += 1
			wordID = -1
			sentProb = TestPred[i+more].split()[1]
			more += 1
		if len(Test[i].split()) == 0:
			pass
		else:
			word = Test[i].split()[1]
			for p in TestUNKs:
				if word.lower() in TestUNKs[p]:
					if word.lower() not in TestUNKs2MPs:
						TestUNKs2MPs[word.lower()] = []
					margProb = TestPred[i+more].split()[1].split(':')[1]
					TestUNKs2MPs[word.lower()].append(float(margProb))
			wordID += 1

	for unk in TestUNKs2MPs:
		TestUNKs2MPs[unk] = numpy.median(TestUNKs2MPs[unk])

#########################################################

""" getting list of words in new training set to measure how many current UNKs are in each sentence (because some orig UNKs may have become known) """

trainWords = []

for line in train:
	if len(line.split()) > 0:
		word = line.split()[1]
		if word not in trainWords:
			trainWords.append(word)

""" get tuples of statistics for all eligible sent ID's """

sentID2tUNK2listStats = CondModel('')

sentID = -1
wordID = -1
sent = []
sentList = []
more = 0
if len(sys.argv) > 9:
	unkCountLimit = int(sys.argv[9])
else:
	unkCountLimit = 1

for i in range(0, len(LeftOverUnannotated)):
	if '@probability' in LeftOverPred[i+more]:
		if sentID != -1:
			if easy == False:
				if unkCount <= unkCountLimit:
					for word2 in sent:
						word = word2.split('$$$')[0]
						for p in TestUNKs:
							if word.lower() in TestUNKs[p]:
								mp = word2.split('$$$')[1]
								mpDiff = float(mp)-float(TestUNKs2MPs[word.lower()])
								if mpDiff > 0:
									origUNKs = sentID2origUNKcounts[sentID]
									freq = TestUNKs[p][word.lower()]
									list = [float(p), float(freq), float(mpDiff), float(origUNKs), (float(sentProb) / (len(sentList))), sentList]
									key = word.lower()
									while key in sentID2tUNK2listStats[sentID]:
										key += '*'
										#print key
									sentID2tUNK2listStats[sentID][key] = list
			else:
				list = [0,0,0,0,(float(sentProb) / (len(sentList))),sentList]
				sentID2tUNK2listStats[sentID][sentProb] = list
		
		sentProb = LeftOverPred[i+more].split()[1]
		if float(sentProb) <= 0:
			sentProb = -1000000
		else:
			sentProb = math.log(float(sentProb))
		sent = []
		sentList = []
		unkCount = 0
		sentID += 1
		wordID = -1
		more += 1
	elif len(LeftOverUnannotated[i].split()) == 0:
		pass
	else:
		word = LeftOverUnannotated[i].split()[1]
		if word not in trainWords:
			unkCount += 1
		margProb = LeftOverPred[i+more].split()[1].split(':')[1]
		wordID += 1
		sent.append(word+'$$$'+margProb)
		line = ''
		""" LOOK HERE !!!!!!!!!!!!!!! """
		label = LeftOverPred[i+more].split()[1].split(':')[0]
		line += label
		for item in LeftOverUnannotated[i].split()[1:]:
			line += '\t'+item
		sentList.append(line)
		
with open("sentID2tUNK2listStats.dat",'w') as of:
		pickle.dump(sentID2tUNK2listStats,of)
		
#############################################################

# for sid in sentID2tUNK2listStats:
	# for UNK in sentID2tUNK2listStats[sid]:
		# print sid
		# print UNK
		# print sentID2tUNK2listStats[sid][UNK]
		# print
		
# print len(sentID2tUNK2listStats)


			