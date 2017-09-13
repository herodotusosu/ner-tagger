### run with "cat name_of_file.html | python ../perseusExtractor.py"
import sys
import string

iChars = ['#']
badWords = ['unietvicensimae','terrestriumter','terisuna','totidemtres','terrarumter']

for line in sys.stdin:
	line = line.replace('\n','')
	if len(line.split()) == 0:
		print
	else:
		for ch in iChars:
			if ch in line:
				line = line.replace(ch,'')
		for w in badWords:
			if w in line:
				line = line.replace(w,w+'PROBLEM')
		print line