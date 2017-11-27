from __future__ import division
import sys
import string
from model import *
import time
import cPickle as pickle

inputfile = (open(sys.argv[1]))
testUNKs = pickle.load(inputfile)
addedSents = (open(sys.argv[2]).read().splitlines())

tUcount = 0
for x in testUNKs:
	tUcount += len(testUNKs[x])
	
matches = []
for line in addedSents:
	if len(line.split()) > 0:
		word = line.split()[1].lower()
		if word not in matches:
			for x in testUNKs:
				if word in testUNKs[x]:
					matches.append(word)
					break
matches = len(matches)

print matches/tUcount