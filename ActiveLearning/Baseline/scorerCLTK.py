from __future__ import division
import sys
import re
import os
import string
import operator
from model import *

Test = (open(sys.argv[1]).read().splitlines())
Pred  = (open(sys.argv[2]).read().splitlines())
Train = (open(sys.argv[3]).read().splitlines())
option = sys.argv[4] # nonCLTK if you want to compare based on binary classification in the regular model

tSentID2NEs = {}
pSentID2NEs = {}

sid = 0
pSentID2NEs[sid] = []
for i in range(0,len(Pred)):
	if 'Corpus not found.' in Pred[i]:
		pass
	elif len(Pred[i].split()) == 0:	
		sid += 1
		pSentID2NEs[sid] = []
	else:
		if option == 'nonCLTK':
			if Pred[i].split()[1] != '0':
				pSentID2NEs[sid].append(Pred[i].split()[4])
		else:
			if Pred[i].split()[0] != '0':
				pSentID2NEs[sid].append(Pred[i].split()[1])
			
sid = 0
tSentID2NEs[sid] = []
for i in range(0,len(Test)):
	if len(Test[i].split()) == 0:	
		sid += 1
		tSentID2NEs[sid] = []
	else:
		if Test[i].split()[0] != '0':
			tSentID2NEs[sid].append(Test[i].split()[1])

words = []
for line in Train:
	if len(line.split()) > 0:
		if line.split()[1] not in words:
			words.append(line.split()[1])

corrects = 0
guesses = 0
actuals = 0
count = 0
correctsUNK = 0
guessesUNK = 0
actualsUNK = 0
countUNK = 0		
for s in pSentID2NEs:
	for g in pSentID2NEs[s]:
		guesses += 1
		if g not in words:
			guessesUNK += 1
		if g in tSentID2NEs[s]:
			corrects += 1
			if g not in words:
				correctsUNK += 1
	for a in tSentID2NEs[s]:
		actuals += 1
		count += 1
		if a not in words:
			actualsUNK += 1
			countUNK += 1
		
P = corrects/guesses
R = corrects/actuals
F = 2*((P*R)/(P+R))

print F, P, R, count
		
PUNK = correctsUNK/guessesUNK
RUNK = correctsUNK/actualsUNK
FUNK = 2*((PUNK*RUNK)/(PUNK+RUNK))

print FUNK, PUNK, RUNK, countUNK




####### DOESN'T WORK BECAUSE CLTK HAS A DIFFERENT PREPROCESSING METHOD ... NEED TO MANUALLY ALIGN INSTEAD ###############
# i = -1
# for j in range(0, len(Test)):
	# i += 1
	# if 'Corpus not found' in Pred[i]:
		# i += 1
	# if len(Test[i].split()) == 0:
		# print
	# else:
		# print 'P:'
		# print Pred[i]
		# print 'A:'
		# print Test[j]
		# print
		# print 'P:', Pred[i].split()[0], 'A:', Test[j]
		# print '________________________________________'
		# print