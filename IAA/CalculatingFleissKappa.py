from __future__ import division
import sys
import time
import math
import string
from model import *

Alex = (open(sys.argv[1]).read().splitlines())
Petra = (open(sys.argv[2]).read().splitlines())
Christopher = (open(sys.argv[3]).read().splitlines())

print "RUNNING CHECK"

checkLength = 10000
i = -1
for line in Alex:
	i += 1
	if i < checkLength:
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
	else:
		break
					
print "DONE WITH CHECK - if this is the second line of the results file, there were no fatal errors prohibiting us from calculating Fleiss Kappa Agreement"
print
time.sleep(1)		

print "STARTING CALCULATION OF FLEISS KAPPA"
print
	
Pis = Model('')
Pjs = Model('')
numOfAnnotators = len(['Alex','Christopher','Petra'])
possibleTags = ['0','PRSU','PRSF','PRS','PRSL','GRPU','GRPF','GRP','GRPL','GEOU','GEOF','GEO','GEOL']
wordCount = 0

firstLineNum = 0
lastLineNum = 5000
# firstLineNum = 5000
# lastLineNum = 10002

i = -1
for line in Alex:
	i += 1
	if i >= firstLineNum and i < lastLineNum:
		if len(line.split()) > 0:
			wordCount += 1
			Alabel = line.split()[0]
			word = line.split()[1]
			Plabel = Petra[i].split()[0]
			Clabel = Christopher[i].split()[0]
			# if Alabel != Plabel or Alabel != Clabel:
				# print Alabel, Plabel, Clabel, word
				# time.sleep(1)
			Pjs[Alabel] += 1 
			Pjs[Clabel] += 1
			Pjs[Plabel] += 1
			choices = Model('')
			choices[Alabel] += 1 
			choices[Plabel] += 1
			choices[Clabel] += 1
			choiceSum = 0
			for pt in possibleTags:
				choiceSum += choices[pt]*(choices[pt]-1)
			Pis[i] = (1/(numOfAnnotators*(numOfAnnotators-1)))*(choiceSum)

Pjs.normalize()
Pe = 0
for pt in possibleTags:
	Pe += Pjs[pt]**2
sumPi = 0			
for i in Pis:
	sumPi += Pis[i]
Pbar = (1/wordCount)*sumPi			
k = (Pbar - Pe) / (1 - Pe)

print 'FOR', str(wordCount), "WORDS IN THE ORIGINAL IAA TEST, WE ACHIEVED THE FOLLOWING FLEISS KAPPA AGREEMENT SCORE"
print k

###################################################################

Pis = Model('')
Pjs = Model('')
numOfAnnotators = len(['Alex','Christopher','Petra'])
possibleTags = ['0','PRSU','PRSF','PRS','PRSL','GRPU','GRPF','GRP','GRPL','GEOU','GEOF','GEO','GEOL']
wordCount = 0

# firstLineNum = 0
# lastLineNum = 5000
firstLineNum = 5000
lastLineNum = 10002

i = -1
for line in Alex:
	i += 1
	if i >= firstLineNum and i < lastLineNum:
		if len(line.split()) > 0:
			wordCount += 1
			Alabel = line.split()[0]
			word = line.split()[1]
			Plabel = Petra[i].split()[0]
			Clabel = Christopher[i].split()[0]
			# if Alabel != Plabel or Alabel != Clabel:
				# print Alabel, Plabel, Clabel, word
				# time.sleep(1)
			Pjs[Alabel] += 1 
			Pjs[Clabel] += 1
			Pjs[Plabel] += 1
			choices = Model('')
			choices[Alabel] += 1 
			choices[Plabel] += 1
			choices[Clabel] += 1
			choiceSum = 0
			for pt in possibleTags:
				choiceSum += choices[pt]*(choices[pt]-1)
			Pis[i] = (1/(numOfAnnotators*(numOfAnnotators-1)))*(choiceSum)

Pjs.normalize()
Pe = 0
for pt in possibleTags:
	Pe += Pjs[pt]**2
sumPi = 0			
for i in Pis:
	sumPi += Pis[i]
Pbar = (1/wordCount)*sumPi			
k = (Pbar - Pe) / (1 - Pe)

print
print 'AFTER CONVENING AND UPDATING ANNOTATION GUIDELINES, WE RECONDUCTED A TEST OF IAA'
print 'OVER', str(wordCount), "ADDITIONAL WORDS, WE ACHIEVED THE FOLLOWING FLEISS KAPPA AGREEMENT SCORE"
print k