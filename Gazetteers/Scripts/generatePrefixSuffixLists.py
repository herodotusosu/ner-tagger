from __future__ import division
import sys
import re
import os
import string
import operator
#from model import *
import math
import cPickle as pickle
from random import *
import time

### use BackUpTexts/corpus.pp as input

corpus = (open(sys.argv[1]))
prefixes = ['']
suffixes = ['']

for line in corpus:
	if len(line.split()) > 0:
		lemma = None
		line = line.lower()
		line = line.replace('j','i').replace('u','v')
		word = line.split()[1]
		for w in line.split():
			if "posft-lemma=" in w and '<unknown>' not in w:
				lemma = w.replace('posft-lemma=','')
				break
				
		lemmaChunks = []
		
		if lemma == None:
			lemma = ''
		oldLemma = lemma
		while lemma != '':		
			# all which include the first letter
			for i in range(len(lemma),0,-1):
				lemmaChunk = lemma[0:i]
				if lemmaChunk not in lemmaChunks:
					lemmaChunks.append(lemmaChunk)
			# all that include the last letter
			for i in range(1,len(lemma)):
				lemmaChunk = lemma[i:]
				if lemmaChunk not in lemmaChunks:
					lemmaChunks.append(lemmaChunk)
			lemma = lemma[1:-1]
		lemma = oldLemma
		
		lemmaChunks2 = []
		for i in range(len(oldLemma),0,-1):
			for lemmaChunk in lemmaChunks:
				if i == len(lemmaChunk):
					lemmaChunks2.append(lemmaChunk)
		lemmaChunks = lemmaChunks2
		
		for lemmaChunk in lemmaChunks:
			if lemmaChunk in word and len(lemmaChunk) > len(word)*0.5:
				for i in range(0,len(word)):
					if lemmaChunk == word[i:i+len(lemmaChunk)]:
						if i == 0 and len(word) > len(lemmaChunk):
							suffix = word[len(lemmaChunk):]
							if suffix not in suffixes:
								suffixes.append(suffix)
						elif len(word) == i+len(lemmaChunk) and len(word) > len(lemmaChunk):
							prefix = word[0:i]
							if prefix not in prefixes:
								prefixes.append(prefix)
						elif len(word) > len(lemmaChunk):
							prefix = word[0:i]
							suffix = word[len(lemmaChunk):]
							if prefix not in prefixes:
								prefixes.append(prefix)
							if suffix not in suffixes:
								suffixes.append(suffix)			
						break
				break
			
# for pre in prefixes:
	# print pre
for suff in suffixes:
	print suff	
