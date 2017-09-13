import sys
import string

test = (open(sys.argv[1]).read().splitlines())
train = (open(sys.argv[2]).read().splitlines())

words = []
allWords = []

i = 0
for line in train:
	if len(line.split()) > 0:
		word = line.split()[1]
		if word not in words:
			words.append(word)
		if word not in allWords:
			allWords.append(word)
		
for line in test:
	if len(line.split()) > 0:
		word = line.split()[1]
		if word not in allWords:
			allWords.append(word)
		
for line in test:
	if len(line.split()) > 0:
		word = line.split()[1]
		if word not in words:
			if word[0].isupper():
				if word[0].lower()+word[1:] in allWords:
					print "PRIORITY 2:	",word
				else:
					print "PRIORITY 1:	",word