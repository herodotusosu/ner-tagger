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

train = (open(sys.argv[1]).read().splitlines())
test = (open(sys.argv[2]).read().splitlines())
	
words = Model('')
priority2testUNKs = {}
highPriorityUNKs = Model('')
lowPriorityUNKs = Model('')
	
for line in train:
	if len(line.split()) > 0:
		word = line.split()[1]
		words[word] += 1

searchThese = []		
for line in test:
	if len(line.split()) > 0:
		word = line.split()[1]
		if word not in words:
#### TOGGLE THIS OFF TO INCLUDE UNCAPPED TEST UNKS AS WELL ####
			if word[0].isupper() and 'NotAProperNoun' not in line:
				highPriorityUNKs[word.lower()] += 1
			if word[0].isupper() and 'NotAProperNoun' in line:
				lowPriorityUNKs[word.lower()] += 1
priority2testUNKs[1] = highPriorityUNKs
priority2testUNKs[2] = lowPriorityUNKs

with open("testUNKs.dat",'w') as of:
		pickle.dump(priority2testUNKs,of)
with open("trainWords.dat",'w') as of:
		pickle.dump(words,of)

# tokens = 0		
# for i in priority2testUNKs[1]:
	# tokens += priority2testUNKs[1][i]
# print len(priority2testUNKs[1])
# print tokens

# tokens = 0		
# for i in priority2testUNKs[2]:
	# tokens += priority2testUNKs[2][i]
# print len(priority2testUNKs[2])
# print tokens
		
############### DEBUGGING AND BETA TESTING ####################
				
#pred = (open(sys.argv[3]).read().splitlines())
				
# print 'THINKING ABOUT LOW PRIORITY WORDS'
# right = 0
# total = 0
# for lp in lowPriorityUNKs:
	# count = lowPriorityUNKs[lp]
	# for line in pred:
		# if len(line.split()) > 0 and lp == line.split()[4].lower():
			# if line.split()[1] == line.split()[3]:
				# right += 1
			# total += 1
			# count -= 1
			# if count == 0:
				# break
# accuracy = right / total
# print accuracy
# print

# print 'THINKING ABOUT HIGH PRIORITY WORDS'
# right = 0
# total = 0
# for lp in highPriorityUNKs:
	# count = lowPriorityUNKs[lp]
	# for line in pred:
		# if len(line.split()) > 0 and lp == line.split()[4].lower():
			# if line.split()[1] == line.split()[3]:
				# right += 1
			# total += 1
			# count -= 1
			# if count == 0:
				# break
# accuracy = right / total
# print accuracy
# print

# print 'THINKING ABOUT ALL CAPPED UNK WORDS'
# right = 0
# total = 0
# for line in pred:
	# if len(line.split()) > 0 and line.split()[4] not in words and line.split()[4][0].isupper():
		# total += 1
		# if line.split()[1] == line.split()[3]:
			# right += 1
# accuracy = right / total
# print accuracy
# print

	
##############################################################
	