import sys
import chardet

test  = (open(sys.argv[1]).read().splitlines())

for line in test:
	printline = ''
	if len(line.split()) > 0:
		printline += 'P: '+line.split()[2]+' A: '+line.split()[1]+' '+line.split()[0]
	print printline