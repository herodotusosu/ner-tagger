### run with "cat name_of_file.html | python ../perseusExtractor.py"
import sys
import string

output = {}

for line in sys.stdin:
	line = line.replace(':','<COLON>')
	print line[0:-1]