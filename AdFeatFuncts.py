from __future__ import division
import sys
import re
import os
import string
import operator
from model import *
import cPickle as pickle
import time


""" STANDARD FEATURES """

def usePOS(printline,feats):
	for ft in feats:
		if 'POSft-' in ft and 'Morpheme=' not in ft and 'lemma=' not in ft:
			printline += '\t'+ft
	return printline
	
def addCollectivePOS(printline,feats):
	collFt = []
	for ft in feats:
		if 'POSft-' in ft and 'Morpheme=' not in ft and 'lemma=' not in ft:
			collFt.append(ft)
	if len(collFt) > 1:
		CF = ''
		for item in collFt:
			CF += item
		printline += '\t'+CF
	return printline
	
def useDefMorphs(printline,feats):
	for ft in feats:
		if '-defMorpheme=' in ft:
			ft = ft.replace('POSft-','')
			printline += '\t'+ft
	return printline

def useLemmas(printline,lem):
	for ft in lem:
		printline += '\t'+'LEMMA-'+ft
	return printline
	
def useNumber(printline,feats):
	if 'num-sing' in feats:
		printline += '\tnum-sing'
	elif 'num-plur' in feats:
		printline += '\tnum-plur'
	return printline
	
def addTtlPnctCrdnmAbbrv(printline, word, lem):
	# for lemma in lem:
		# if '<unknown>' not in lemma:
			# lem = lemma
			# break
	CardNum = True
	if word.isupper() == False:
		CardNum = False
	else:
		for ch in word:
			if ch not in ('M','C','D','L','I','V','X'):
				CardNum = False
	if CardNum == True:
		printline += '\t'+'CardNum'
	elif len(word) == 1 and word in string.punctuation:
		printline += '\t'+'PUNCT'
	elif len(word) > 1 and word[0] in string.punctuation and word[-1] in string.punctuation:
		printline += '\t'+'PUNCT'
	elif word == '<COLON>':
		printline += '\t'+'PUNCT'
	elif len(word) > 1:
		if word[0].isupper():
			if word[-1] in string.punctuation:
				if word == 'M.':
					printline += '\t'+'Abbrev-Case'
				elif word == 'L.':
					printline +='\t'+'Abbrev-Case'
				elif word == 'C.':
					printline += '\t'+'Abbrev-Case'
				elif word == 'D.':
					printline += '\t'+'Abbrev-Case'
				elif word == 'V.':
					printline += '\t'+'Abbrev-Case'
				else:
					CardNum = True
					for ch in word.replace(word[-1],''):
						if ch not in ('M','C','D','L','I','V','X'):
							CardNum = False
					if CardNum == True:
						printline += '\t'+'CardNum'
					else:
						printline += '\t'+'Abbrev-Case'
			elif word[1].isupper() == False:
				printline += '\t'+'Title-Case'
		# if lem[0].isupper() and len(lem) > 1 and lem[1].islower():
			# printline += '\t'+'Lem-Title-Case'
	return printline
					
def addCharacterNgrams(printline, word, n):
	list = []
	c = 0
	Word = '<'+word+'>'
	for i in range(1,len(Word)-1):
		if i < (n+1):
			if Word[0:i+1].lower() not in list:
				list.append(Word[0:i+1].lower())
				printline += '\t'+'Ngram-'+Word[0:i+1].lower()
		if len(Word) - i < (n+2):
			if Word[i:].lower() not in list:
				list.append(Word[i:].lower())
				printline += '\t'+'Ngram-'+Word[i:].lower()
	return printline
	
def addDeTitledNonProperNouns(printline, word, words):
	if word[0].isupper() and word[-1].islower() and word.lower() in words:
		printline += '\t'+'NotAProperNoun'
	return printline
	
def addPrevNNextLemma(printline,prevLem,nextLem):
	for item in prevLem:
		printline += '\t'+'PL-'+item
	for item in nextLem:
		printline += '\t'+'NL-'+item
	return printline
	
def addPrevNNextWord(printline, prevWord, nextWord):
	printline += '\t'+'PW-'+prevWord+'\t'+'NW-'+nextWord
	return printline
	
def addAllPrevNNextPOS(printline,prevFeats,nextFeats):
	for item in prevFeats:
		if 'Morpheme' not in item:
			printline += '\tprev-'+item
	for item in nextFeats:
		if 'Morpheme' not in item:
			printline += '\tnext-'+item
	return printline
	
def getFbiAndTriGrams(C, N, NN):
	fBi = 'fBigram-'+C+'-'+N 
	fTri = 'fTrigram-'+C+'-'+N+'-'+NN
	return fBi, fTri
	
def getBbiAndTriGrams(PP, P, C):
	bBi = 'bBigram-'+P+'-'+C
	bTri = 'bTrigram-'+PP+'-'+P+'-'+C 
	return bBi, bTri
	
def getFbiGrams(C, N):
	fBi = 'fBigram-'+C+'-'+N
	return fBi
	
def getBbiGrams(P, C):
	bBi = 'bBigram-'+P+'-'+C
	return bBi
	
def getFlemBiAndTriGrams(CL, NL, NNL):
	for C in CL:
		for N in NL:
			for NN in NNL:
				fBi = 'fLemBigram-'+C+'-'+N
				fTri = 'fLemTrigram-'+C+'-'+N+'-'+NN
	return fBi, fTri
	
def getBlemBiAndTriGrams(PPL, PL, CL):
	for PP in PPL:
		for P in PL:
			for C in CL:
				bBi = 'bLemBigram-'+P+'-'+C
				bTri = 'bLemTrigram-'+PP+'-'+P+'-'+C 
	return bBi, bTri
	
def getFlemBiGrams(CL, NL):
	for C in CL:
		for N in NL:
			fBi = 'fLemBigram-'+C+'-'+N
	return fBi
	
def getBlemBiGrams(PL, CL):
	for P in PL:
		for C in CL:
			bBi = 'bLemBigram-'+P+'-'+C
	return bBi
						
def getFPOSbiAndTriGrams(CPOS, NPOS, NNPOS):
	CPOS.sort()
	C = ''
	for x in CPOS:
		if 'Morpheme' not in x:
			C += x
	NPOS.sort()
	N = ''
	for x in NPOS:
		if 'Morpheme' not in x:
			N += x
	NNPOS.sort()
	NN = ''
	for x in NNPOS:
		if 'Morpheme' not in x:
			NN += x
					
	fBi = 'fPOSBigram-'+C+'THEN'+N
	fTri = 'fPOSTrigram-'+C+'THEN'+N+'THEN'+NN
	return fBi, fTri
	
def getBPOSbiAndTriGrams(PPPOS, PPOS, CPOS):
	PPPOS.sort()
	PP = ''
	for x in PPPOS:
		if 'Morpheme' not in x:
			PP += x
	PPOS.sort()
	P = ''
	for x in PPOS:
		if 'Morpheme' not in x:
			P += x
	CPOS.sort()
	C = ''
	for x in CPOS:
		if 'Morpheme' not in x:
			C += x
					
	bBi = 'bPOSBigram-'+P+'THEN'+C
	bTri = 'bPOSTrigram-'+PP+'THEN'+P+'THEN'+C 
	return bBi, bTri
	
def getFPOSbiGrams(CPOS, NPOS):
	CPOS.sort()
	C = ''
	for x in CPOS:
		if 'Morpheme' not in x:
			C += x
	NPOS.sort()
	N = ''
	for x in NPOS:
		if 'Morpheme' not in x:
			N += x
					
	fBi = 'fPOSBigram-'+C+'THEN'+N
	return fBi
	
def getBPOSbiGrams(PPOS, CPOS):
	PPOS.sort()
	P = ''
	for x in PPOS:
		if 'Morpheme' not in x:
			P += x	
	CPOS.sort()
	C = ''
	for x in CPOS:
		if 'Morpheme' not in x:
			C += x
					
	bBi = 'bPOSBigram-'+P+'THEN'+C
	
	return bBi
	
""" W2V FEATURES """

def addW2Vsims(printline, word, sims):
	printline += '\tsim-'+word.lower().replace('j','i').replace('v','u')
	if word in sims:
		for sim in sims[word]:
			printline += '\tsim-'+sim
	return printline
	
def addW2VsimsLemmed(printline, lem, simsLemmed):
	for l in lem:
		if '<unknown' not in l:
			lemma = l
	lem = lemma
	printline += '\tsimlem-'+lem.lower().replace('j','i').replace('v','u')
	if lem in simsLemmed:
		for sim in simsLemmed[lem]:
			printline += '\tsimLem-'+sim
	return printline
	
""" GAZETTEER FEATURES """

### Uses all gazetteers except MWE's
def useGazatteer(printline, word, gazList):
	strGazList = ['GazGEOall','GazGEOFs','GazGEOLs','GazGEOMWEs','GazGEOs','GazGEOUs','GazPRSall','GazPRSFs','GazPRSLs','GazPRSMWEs','GazPRSs','GazPRSUs','GazUNKall','GazUNKFs','GazUNKLs','GazUNKMWEs','GazUNKs','GazUNKUs']
	word = word.lower()
	n = -1
	for gaz in gazList:
		n += 1
		if word in gaz:
			printline += '\t'+strGazList[n]
	return printline
	
""" DOMAIN ADAPTATION """
def addDomain(printline, domains, prose):
	if prose == 'prose':
		domains.append('proseText')
	elif prose == 'poetry':
		domains.append('poetryText')
	for dom in domains:
		if 'domain-author' in dom:
		# if 'domain-title' in dom:
			printline += '\t'+dom
	return printline
def DaumeDomAdap(printline, domains, prose):
	if prose == 'prose':
		domains.append('proseText')
	elif prose == 'poetry':
		domains.append('poetryText')
	if len(printline.split()) > 0:
		items = []
		for item in printline.split()[1:]:
			items.append(item)
		for item in items:
			for domain in domains:
				if 'domain-author' in domain:
				# if 'domain-title' in domain:
					printline += '\t'+domain+'-'+item
	return printline
def addProsePoetry(printline, prose):			
	if prose == True:
		printline += '\tproseText'
	else:
		printline += '\tpoetryText'
	return printline	
def addDaumeProsePoetry(printline, prose):
	if prose == True:
		dom = 'proseText'
	else:
		dom = 'poetryText'
	if len(printline.split()) > 0:
		items = []
		for item in printline.split()[1:]:
			items.append(item)
		for item in items:
			printline += '\t'+dom+'-'+item
	return printline
		
		