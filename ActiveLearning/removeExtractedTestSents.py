from __future__ import division
import sys
import string
from model import *
import time

test = (open(sys.argv[1]).read().splitlines())
delete = (open(sys.argv[2]).read().splitlines())

sents = []
sent = []
for line in delete:
	if len(line.split()) > 0:
		word = line.split()[1]
		sent.append(word)
	else:
		sents.append(sent)
		sent = []

sent = []
printlines = []		
for line in test:
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
		print
		