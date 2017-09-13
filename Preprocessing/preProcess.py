import sys
import string
CW = (open(sys.argv[1]).read().splitlines())
#CW = sys.argv[1].splitlines()
#CW = sys.stdin #Use this version of CW if running perseusExtractor.sh

i = 0
for line in CW:
	line = line.replace('!','.')
	if line.split()[0] == 'LEAVEBLANK':
		print
	else:
		print line.replace('\n','')
		if line.split()[1] == 'SENT':
			if len(CW) > i:
				if len(CW[i+1].split()) > 0:
					if CW[i+1].split()[1] != 'PUN':
						print
				else:
					print
			else:
				print
		elif line.split()[1] == 'PUN':
			if i > 0 and len(CW[i-1].split()) > 0 and CW[i-1].split()[1] == 'SENT':
				print
			elif i > 1 and len(CW[i-1].split()) > 0 and len(CW[i-2].split()) > 0 and CW[i-1].split()[1] == 'PUN' and CW[i-2].split()[1] == 'SENT':
				print
	i += 1