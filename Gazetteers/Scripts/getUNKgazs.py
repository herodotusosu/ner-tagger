import sys

full = (open(sys.argv[1]).read().splitlines())

allList = []
MWElist = []
Ulist = []

n = 0
for line in full:
	line = line.replace('_',' ')
	if len(line.split()) > 1:
		if line.split()[1][0].isupper() == True:
			line = line.lower()
			MWElist.append(line)
		else:
			line = line.split()[0].lower()
	else:
		if line.split()[0].lower() not in Ulist:
			Ulist.append(line.split()[0].lower())
	for word in line.split():
		word = word.lower()
		if word not in allList:
			allList.append(word)
		
# for item in MWElist:
	# while item[-1] == ' ':
		# item = item[0:-1]
	# print item
	
# for item in Ulist:
	# print item.replace(' ','')
	
for item in allList:
	print item