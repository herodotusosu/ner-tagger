import sys

#all = (open(sys.argv[2]).read().splitlines())
spec = (open(sys.argv[1]).read().splitlines())

specList = []

for line in spec:
	line = line.lower()
	if line not in specList:
	# for word in line.split():
		# if word not in specList:
			# specList.append(word.lower())
		specList.append(line.lower())
			
for word in specList:
	print word