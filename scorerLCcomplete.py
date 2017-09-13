from __future__ import division
import sys
import re
import os
import string
import operator
from model import *
from functionsLCcomplete import *

PredTest = (open(sys.argv[1]).read().splitlines())
train = (open(sys.argv[2]).read().splitlines())
printOption = sys.argv[3]# -Complete = ready for templateComplete.csv
						# -Full = print everything
						# -TotalF = print just total F-score
						# -TotalUNK = print just total UNK score
						# -domainF = prints totalF-score for <domain>
						# -domainUNK = prints total UNK score for <domain>
domains = sys.argv[4:]#if domains = <name_of_domain>, domain specific information will be added to the output results
# Otherwise set to list with only item ['OFF']
### DOMAINS MUST BE LISTED ALPHABETICALLY
if len(sys.argv) < 5:
	domains = ['OFF']

words = []
for line in train:
	if len(line.split()) > 0:
		word = line.split()[1]
		if word not in words:
			words.append(word)

output = getResults(PredTest, words, domains)

def getTotalsAndByClassAndUNK(output, start, printline):
	for i in range(start+1, 100+len(output)):
		if i in output and len(output[i].split(',')) > 0 and output[i].split(',')[0] == 'Totals':
			line = output[i]
			if printline == '':
				printline = line.split(',')[3]+','+line.split(',')[1]+','+line.split(',')[2]+','+line.split(',')[4]+','
			else:
				printline += ','+line.split(',')[3]+','+line.split(',')[1]+','+line.split(',')[2]+','+line.split(',')[4]+','
			GEO = Model('')#count to [F,Prec,Rec]
			GRP = Model('')
			PRS = Model('')
			for j in range(start,i):
				if j in output and len(output[j].split(',')) > 0:
					line = output[j]
					if 'GEO' in line.split(',')[0]:
						cnt = float(line.split(',')[4])
						if cnt in GEO:
							cnt += .001
						GEO[cnt] = [float(line.split(',')[3]),float(line.split(',')[1]),float(line.split(',')[2])]
					if 'GRP' in line.split(',')[0]:
						cnt = float(line.split(',')[4])
						if cnt in GRP:
							cnt += .001
						GRP[cnt] = [float(line.split(',')[3]),float(line.split(',')[1]),float(line.split(',')[2])]
					if 'PRS' in line.split(',')[0]:
						cnt = float(line.split(',')[4])
						if cnt in PRS:
							cnt += .000000001
						PRS[cnt] = [float(line.split(',')[3]),float(line.split(',')[1]),float(line.split(',')[2])]
			### we have the class statistics, now to put them in the printline
			if len(GEO) != 0:
				totalCount = 0
				for count in GEO:
					totalCount += int(count)
				GEOF = 0
				GEOPrec = 0
				GEORec = 0
				for count in GEO:
					GEOF += GEO[count][0] * (count/totalCount)
					GEOPrec += GEO[count][1] * (count/totalCount)
					GEORec += GEO[count][2] * (count/totalCount)
				printline += str(GEOF)+','+str(GEOPrec)+','+str(GEORec)+','+str(totalCount)+','
			else:
				printline += '0,0,0,0,'
				
			if len(GRP) != 0:
				totalCount = 0
				for count in GRP:
					totalCount += int(count)
				GRPF = 0
				GRPPrec = 0
				GRPRec = 0
				for count in GRP:
					GRPF += GRP[count][0] * (count/totalCount)
					GRPPrec += GRP[count][1] * (count/totalCount)
					GRPRec += GRP[count][2] * (count/totalCount)
				printline += str(GRPF)+','+str(GRPPrec)+','+str(GRPRec)+','+str(totalCount)+','
			else:
				printline += '0,0,0,0,'
				
			if len(PRS) != 0:
				totalCount = 0
				for count in PRS:
					totalCount += int(count)
				PRSF = 0
				PRSPrec = 0
				PRSRec = 0
				for count in PRS:
					PRSF += PRS[count][0] * (count/totalCount)
					PRSPrec += PRS[count][1] * (count/totalCount)
					PRSRec += PRS[count][2] * (count/totalCount)
				printline += str(PRSF)+','+str(PRSPrec)+','+str(PRSRec)+','+str(totalCount)
			else:
				printline += '0,0,0,0'			
			break ### Stops after getting the overall totals and by class, but not domain or UNK yet
	return printline, i

""" make changes here to suit templateComplete.csv """
if printOption == '-Complete':
	start = 0
	printline = ''
	while start < len(output) - 3:
		list = getTotalsAndByClassAndUNK(output, start, printline)
		printline = list[0]
		start = list[1]
	print printline

####################################################################
		
if printOption == '-Full':
	for i in output:
		print output[i]
if printOption == '-TotalF':
	print output[7].split(',')[3]+','+output[7].split(',')[4]
if printOption == '-TotalUNK':
	print output[15].split(',')[3]+','+output[15].split(',')[4]
if printOption == '-domainF':
	for dmn in domains:
		go = False
		for i in output:
			line = output[i]
			check = 'FOR DOMAIN '+ dmn.upper() 
			if check in line:
				go = True
			if go == True and line.split(',')[0] == 'Totals':
				print dmn+','+line.split(',')[3]+','+line.split(',')[4]
				break
if printOption == '-domainUNK':
	for dmn in domains:
		go = False
		gogo = False
		for i in output:
			line = output[i]
			check = 'FOR DOMAIN '+ dmn.upper() 
			if check in line:
				go = True
			if go == True and 'FOR UNKS' in line:
				gogo = True
			if go == True and gogo == True and line.split(',')[0] == 'Totals':
				print dmn+','+line.split(',')[3]+','+line.split(',')[4]
				break