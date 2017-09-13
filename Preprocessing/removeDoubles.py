### run with "cat name_of_file.html | python ../perseusExtractor.py"
import sys
import string

output = {}

j = 0
for line in sys.stdin:
	if len(line.split()) != 0:
		print line.replace('\n','')
		j = 0
	else:
		if j != 1:
			print
		j = 1