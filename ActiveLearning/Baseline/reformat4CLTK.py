import sys
import chardet

i = 0
for line in sys.stdin:
	for word in line.split():
		encoding = chardet.detect(word)
		
		if encoding['encoding'] not in ['ascii','utf-8','utf8']:
			line = line.replace(word,'')

	if len(line.split()) > 0:
		print line.split()[1],
		#pass
	else:
		print
		print