import sys

gaz = (open(sys.argv[1]).read().splitlines())

for line in gaz:
	print line.replace('u','v').replace('j','i')