import sys
import time

Alex = (open(sys.argv[1]).read().splitlines())
Petra = (open(sys.argv[2]).read().splitlines())
Christopher = (open(sys.argv[3]).read().splitlines())

print "RUNNING CHECK"

checkLength = 10000
i = -1
while i < checkLength:
	for line in Alex:
		i += 1 
		if len(line.split()) == 0:
			if len(Petra[i].split()) != 0:
				print 'NEED TO FIX LINE', str(i), 'IN PETRA'
				time.sleep(5)
			if len(Christopher[i].split()) != 0:
				print 'NEED TO FIX LINE', str(i), 'IN Christopher'
				time.sleep(5)
		else:
			Aword = line.split()[1]
			Pword = Petra[i].split()[1]
			Cword = Christopher[i].split()[1]
			if Pword != Aword:
				print 'NEED TO FIX LINE', str(i), 'IN PETRA'
				print Aword, Pword, Cword
				time.sleep(5)
			if Cword != Aword:
				print 'NEED TO FIX LINE', str(i), 'IN Christopher'
				print Aword, Pword, Cword
				time.sleep(5)
					
	print "DONE WITH CHECK"
	time.sleep(2)		

correct = 0
incorrect = 0
correct0s = 0
i = 0
for line in Alex:
	if i >4998 and i < 10000:
		if len(line.split()) > 0:
			label = line.split()[0]
			word = line.split()[1]
			if label == Petra[i].split()[0]:
				correct += 1
				if label == '0':
					correct0s += 1
				if label == Christopher[i].split()[0]:
					correct += 1
					if label == '0':
						correct0s += 1
				else:
					incorrect += 1
					print 'line', str(i)
					print '\t', 'Alex:', line
					print '\t', 'Petra:', Petra[i] 
					print '\t', 'Christopher:', Christopher[i]
			else:
				incorrect += 1
				print 'line', str(i)
				print '\t', 'Alex:', line 
				print '\t', 'Petra:', Petra[i] 
				print '\t', 'Christopher:', Christopher[i]
				if Petra[i].split()[0] == Christopher[i].split()[0]:
					correct += 1
					if label == '0':
						correct0s += 1
	i += 1
	
A = correct
B = incorrect
C = correct + incorrect
D = correct0s
print 'Overall Accuracy:', str(float(A)/float(C))
print 'Accuracy on Named Entities:', str((float(A)-float(D))/(float(C)-float(D)))