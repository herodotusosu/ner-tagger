from __future__ import division
import sys
import re
import os
import string
import operator
from model import *

#Compute the Overall Percent of Tags Correctly Labeled
def computeOverallCorrectLabelPercentage(PredTest):
	right = 0
	wrong = 0
	for line in PredTest:
		if len(line.split()) > 0:
			if line.split()[1] == line.split()[3]:
				right += 1
			else:
				wrong += 1
	print 'Overall Percent of Correct Tags:', str(right/(right+wrong))
	
#Compute the F-Score for General Identification of Named Entities
def Fgeneral(PredTest):
	truePos = 0
	falsePos = 0
	falseNeg = 0
	predPos = 0
	actualPos = 0
	for line in PredTest:
		if len(line.split()) > 0:
			if line.split()[1] != '0':
				if line.split()[3] != '0':
					truePos += 1
				else:
					falsePos += 1
			else:
				if line.split()[3] != '0':
					falseNeg += 1
	F1 = (2*truePos)/(2*truePos+falseNeg+falsePos)			
	print 'F-Score for General Recognition of Status as Named Entity'
	print 'F1:', str(F1)
	
# Once you reach the first word in an MWE, this will find the last
def Check4End(PredTest, j, NE, end, Label):
	if j == len(PredTest):
		Label[NE] += 1
	elif len(PredTest[j]) == 0:
		Label[NE] += 1
	elif end.replace('L','') not in PredTest[j].split()[3]:
		Label[NE] +=1
	elif end == PredTest[j].split()[3]:
		NE += ' '+ PredTest[j].split()[4]
		Label[NE] += 1
	else:
		NE += ' '+ PredTest[j].split()[4]
		j += 1
		Check4End(PredTest, j, NE, end, Label)
		
#Compute the Accuracy of Final Lists of Entities Overall and by Label
def FscoreFinalList(PredTest, Groups, Geos, People, PredGroups, PredGeos, PredPeople):	
	right = 0
	wrong = 0
	i = 0
	# This should get us a list of all the actuals...
	for line in PredTest:
		if len(line.split()) > 0:
			if 'GRPU' == line.split()[3]:
				Groups[line.split()[4]] += 1
			if 'GRPF' == line.split()[3]:
				NE = line.split()[4]
				j = i+1
				end = 'GRPL'
				Check4End(PredTest, j, NE, end, Groups)
			if 'GEOU' == line.split()[3]:
				Geos[line.split()[4]] += 1
			if 'GEOF' == line.split()[3]:
				NE = line.split()[4]
				j = i+1
				end = 'GEOL'
				Check4End(PredTest, j, NE, end, Geos)
			if 'PRSU' == line.split()[3]:
				People[line.split()[4]] += 1
			if 'PRSF' == line.split()[3]:
				NE = line.split()[4]
				j = i+1
				end = 'PRSL'
				Check4End(PredTest, j, NE, end, People)			
		i += 1
	# Now for Predictions
	i = 0
	for line in PredTest:
		if len(line.split()) > 0:
			if 'GRPU' == line.split()[1]:
				PredGroups[line.split()[4]] += 1
			if 'GRPF' == line.split()[1]:
				NE = line.split()[4]
				j = i+1
				end = 'GRPL'
				Check4End(PredTest, j, NE, end, PredGroups)
			if 'GEOU' == line.split()[1]:
				PredGeos[line.split()[4]] += 1
			if 'GEOF' == line.split()[1]:
				NE = line.split()[4]
				j = i+1
				end = 'GEOL'
				Check4End(PredTest, j, NE, end, PredGeos)
			if 'PRSU' == line.split()[1]:
				PredPeople[line.split()[4]] += 1
			if 'PRSF' == line.split()[1]:
				NE = line.split()[4]
				j = i+1
				end = 'PRSL'
				Check4End(PredTest, j, NE, end, PredPeople)			
		i += 1

#Precision and Recall by End List for (not individual occurence) for each Label				
def CalculatePrecNRec(Label, PredLabel):
	num = 0
	denprec = 0
	denrec = 0
	for l in Label:
		denrec += 1
		if l in PredLabel:
			num += 1
	for p in PredLabel:
		denprec += 1
	prec = num/denprec
	rec = num/denrec
	F = 2*((prec*rec)/(prec+rec))
	return prec, rec, F, denrec
	
def CompositeFinalListFscore(grp, geo, prs, fgrp, fgeo, fprs):
	den = len(grp) + len(geo) + len(prs)
	grpCoeff = len(grp)/den
	geoCoeff = len(geo)/den
	prsCoeff = len(prs)/den
	#print 'Concerning the Accuracy of the Overall Final Lists for All Three Labels'
	#print '(Computed by Weighting F-scores for each label by frequency in the Annotation)'
	print "Fcomposite =", str(grpCoeff*fgrp + geoCoeff*fgeo + prsCoeff*fprs)
	
def doFscoresByFinalListsGenerated(PredTest):
	### Compute the Accuracy of Final Lists of Entities Overall and by Label

	Groups = Model('') # These contain the set of each actual Group/geo/prs mentioned paired with count
	Geos = Model('')
	People = Model('')
	PredGroups = Model('') # These contain the set of each Grp/geo/prs as predicted by the CRF
	PredGeos = Model('')
	PredPeople = Model('')

	FscoreFinalList(PredTest, Groups, Geos, People, PredGroups, PredGeos, PredPeople)

	######### Just Concerning the Lists ######################
	print 'BY LISTS ONLY:'
	Fgrp = CalculatePrecNRec(Groups, PredGroups)
	print 'GROUPS(prec,rec,F,actCount):', str(Fgrp[0]),str(Fgrp[1]),str(Fgrp[2]),str(Fgrp[3])
	Fgeo = CalculatePrecNRec(Geos, PredGeos)
	print 'PLACES(prec,rec,F,actCount):', str(Fgeo[0]),str(Fgeo[1]),str(Fgeo[2]),str(Fgeo[3])
	Fprs = CalculatePrecNRec(People, PredPeople)
	print 'PEOPLE(prec,rec,F,actCount):', str(Fprs[0]),str(Fprs[1]),str(Fprs[2]),str(Fprs[3])

	CompositeFinalListFscore(Groups, Geos, People, Fgrp[2], Fgeo[2], Fprs[2])

def CompareGrpNPredGrp(grp, predGrp, strg):
	act = []
	pred = []
	actualNOTpred = []
	predNOTactual = []
	correctlyPredicted = []
	for item in grp:
		act.append(item)
		if item not in predGrp:
			actualNOTpred.append(item)
		else:
			correctlyPredicted.append(item)
	for item in predGrp:
		pred.append(item)
		if item not in act:
			predNOTactual.append(item)
	print strg, 'we Missed:', actualNOTpred
	print 'Spurious', strg+':', predNOTactual
	print
	print 'Correctly identified', str(len(correctlyPredicted))+'/'+str(len(act)), strg,'and spuriously generated', str(len(predNOTactual))
	
def getOutputDict(TP, FP, FN, TPunk, FPunk, FNunk, output, i):
	totalPrec = 0
	totalRec = 0
	totalF = 0
	denom = 0
	for entity in TP:
		if entity != 'Totals':
			p = TP[entity] / (TP[entity] + FP[entity])
			r = TP[entity] / (TP[entity] + FN[entity])
			f = 2 * ((p*r)/(p+r))
			actCount = TP[entity] + FN[entity]
			totalPrec += p*actCount
			totalRec += r*actCount
			#totalF += f*actCount
			denom += actCount
			output[i] = entity +','+ str(p)[0:6]+','+str(r)[0:6]+','+str(f)[0:6]+','+str(actCount)
			i += 1
	if denom != 0:
		p = totalPrec / denom
		r = totalRec / denom
		f = 2 * ((p*r)/(p+r))
	else:
		p = 0
		r = 0
		f = 0
	actCount = denom
	output[i] = 'Totals' +','+ str(p)[0:6]+','+str(r)[0:6]+','+str(f)[0:6]+','+str(actCount)
	i += 1

	### UNKNOWN WORDS
	output[i] = 'FOR UNKS:'
	i += 1
	totalPrec = 0
	totalRec = 0
	totalF = 0
	denom = 0
	for entity in TPunk:
		if entity != 'Totals':
			p = TPunk[entity] / (TPunk[entity] + FPunk[entity])
			r = TPunk[entity] / (TPunk[entity] + FNunk[entity])
			f = 2 * ((p*r)/(p+r))
			actCount = TPunk[entity] + FNunk[entity]
			totalPrec += p*actCount
			totalRec += r*actCount
			#totalF += f*actCount
			denom += actCount
			output[i] = entity +','+ str(p)[0:6]+','+str(r)[0:6]+','+str(f)[0:6]+','+str(actCount)
			i += 1
	if denom != 0:
		p = totalPrec / denom
		r = totalRec / denom
		f = 2 * ((p*r)/(p+r))
	else:
		p = 0
		r = 0
		f = 0
	actCount = denom
	output[i] = 'Totals' +','+ str(p)[0:6]+','+str(r)[0:6]+','+str(f)[0:6]+','+str(actCount)
	i += 1
	output[i+1] = '***'
	i += 1
	
	return output, i
	
def getResults(PredTest, words, domains):
	output = {}
	i = 0
	### Print Stanford-style Results
	output[i] = 'BY OCCURENCES OF SPECIFIC LABELS:'
	i += 1

	TP = Model('')
	FP = Model('')
	FN = Model('')
	TPunk = Model('')
	FPunk = Model('')
	FNunk = Model('')
	if domains[0] != 'OFF':
		TPd = CondModel('')
		FPd = CondModel('')
		FNd = CondModel('')
		TPdunk = CondModel('')
		FPdunk = CondModel('')
		FNdunk = CondModel('')

	for line in PredTest:
		if len(line.split()) > 0:
			word = line.split()[4]
			UNK = False
			if word not in words:
				UNK = True
			domain = None
			if domains[0] != 'OFF':
				for d in domains:
					do = d + '-'
					if do in line:
						domain = d
			pr = line.split()[1]
			ac = line.split()[3]
			if pr == '0' and ac == '0':
				pass
			else:
				if pr == ac:
					if domain != None:
						TPd[domain]['Totals'] += 1
						TPd[domain][ac] += 1
					TP[ac] += 1
					TP['Totals'] += 1
					if UNK == True:
						if domain != None:
							TPdunk[domain][ac] += 1
							TPdunk[domain]['Totals'] += 1
						TPunk[ac] += 1
						TPunk['Totals'] += 1
				else:
					if domain != None:
						FPd[domain][pr] += 1
						FNd[domain][ac] += 1
					FP[pr] += 1
					FN[ac] += 1
					if UNK == True:
						if domain != None:
							FPdunk[domain][pr] += 1
							FNdunk[domain][ac] += 1
						FPunk[pr] += 1
						FNunk[ac] += 1
	
	### Pre Domains
	list = getOutputDict(TP, FP, FN, TPunk, FPunk, FNunk, output, i)
	output = list[0]
	i = list[1]
	### With Domains
	if domains[0] != 'OFF':
		for dom in domains:
			prln = 'FOR DOMAIN '
			prln += dom.upper()
			prln += ':'
			output[i] = prln
			i += 1
			list = getOutputDict(TPd[dom], FPd[dom], FNd[dom], TPdunk[dom], FPdunk[dom], FNdunk[dom], output, i)
			output = list[0]
			i = list[1]
	
	return output
		