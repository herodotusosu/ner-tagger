from __future__ import division
import sys
import re
import os
import string
import operator
import time
from model import *
from AdFeatFuncts import *

""" run with:
	python ../AddingFeatures.py ../Preprocessing/Preprocessed/$folder/$file.pp domainPlaceHolder ../Gazetteers/GEOall.txt ../Gazetteers/GEOFs.txt ../Gazetteers/GEOLs.txt ../Gazetteers/GEOMWEs.txt ../Gazetteers/GEOs.txt ../Gazetteers/GEOUs.txt ../Gazetteers/PRSall.txt ../Gazetteers/PRSFs.txt ../Gazetteers/PRSLs.txt ../Gazetteers/PRSMWEs.txt ../Gazetteers/PRSs.txt ../Gazetteers/PRSUs.txt ../Gazetteers/UNKall.txt ../Gazetteers/UNKFs.txt ../Gazetteers/UNKLs.txt ../Gazetteers/UNKMWEs.txt ../Gazetteers/UNKs.txt ../Gazetteers/UNKUs.txt > $file.ftrs
	
	1. <TrainingText.pp>
	2. <domain> 
	3- Gazetteers
		3-	GEOall
		4 	GEOFs
		5 	GEOLs
		6 	GEOMWE
		7 	GEOs
		8 	GEOUs
		9 	PRSall
		10 	PRSFs
		11 	PRSLs
		12 	PRSMWE
		13 	PRSs
		14 	PRSUs
		15 	UNKall
		16 	UNKs
		17 	UNKs
		18 	UNKMWE
		19 	UNKs
		20 	UNKUs
 """

annotation = (open(sys.argv[1]).read().splitlines())
domain = sys.argv[2]

""" Gazetteers """
GazGEOall = (open(sys.argv[3]).read().splitlines())
GazGEOFs = (open(sys.argv[4]).read().splitlines())
GazGEOLs = (open(sys.argv[5]).read().splitlines())
GazGEOMWEs = (open(sys.argv[6]).read().splitlines())
GazGEOs = (open(sys.argv[7]).read().splitlines())
GazGEOUs = (open(sys.argv[8]).read().splitlines())
GazPRSall = (open(sys.argv[9]).read().splitlines())
GazPRSFs = (open(sys.argv[10]).read().splitlines())
GazPRSLs = (open(sys.argv[11]).read().splitlines())
GazPRSMWEs = (open(sys.argv[12]).read().splitlines())
GazPRSs = (open(sys.argv[13]).read().splitlines())
GazPRSUs = (open(sys.argv[14]).read().splitlines())
GazUNKall = (open(sys.argv[15]).read().splitlines())
GazUNKFs = (open(sys.argv[16]).read().splitlines())
GazUNKLs = (open(sys.argv[17]).read().splitlines())
GazUNKMWEs = (open(sys.argv[18]).read().splitlines())
GazUNKs = (open(sys.argv[19]).read().splitlines())
GazUNKUs = (open(sys.argv[20]).read().splitlines())
gazList = [GazGEOall,GazGEOFs,GazGEOLs,GazGEOMWEs,GazGEOs,GazGEOUs,GazPRSall,GazPRSFs,GazPRSLs,GazPRSMWEs,GazPRSs,GazPRSUs,GazUNKall,GazUNKFs,GazUNKLs,GazUNKMWEs,GazUNKs,GazUNKUs]
inputfile = (open(sys.argv[-1]))

""" initialize with word, set of lems(just lem of UNK and lemma), and set of features """
nextLem = []
nextFeats = []

nextNextWord = None
nextNextLem = []
nextNextFeats = []

i = -1
for line in annotation:
	i += 1
	if len(line.split()) != 0:
		nextWord = line.split()[1]
		for item in line.split()[2:]:
			if 'POSft-lemma=' in item:
				nextLem.append(item.replace('POSft-lemma=',''))
			elif 'domain-' not in item:
				nextFeats.append(item)
#############################################################
		if len(annotation[i+1].split()) != 0:
			nextNextWord = annotation[i+1].split()[1]
			for item in annotation[i+1].split()[2:]:
				if 'POSft-lemma=' in item:
					nextNextLem.append(item.replace('POSft-lemma=',''))
				elif 'domain-' not in item:
					nextNextFeats.append(item)
##############################################################
		break
		
word = '<s>'
lem = ['<s>']
feats = []

""" Now that it is initialized, go through corpus """
i = 0
prose = True
for i, line in enumerate(annotation):
##############################
	if word != '<s>':
		prevPrevWord = prevWord
		prevPrevLem = prevLem
		prevPrevFeats = prevFeats
	else:
		prevPrevWord = None
##############################
	prevFeats = feats
	feats = nextFeats
	prevLem = lem
	lem = nextLem
	prevWord = word
	word = nextWord
	
	printline = ''
	
	if prevWord == '<s>' and len(line.split()) > 2:
		domains = []
		prose = True
		for item in line.split()[2:]:
			if 'domain-' in item:
				domains.append(item)
				#  domain-title-De_Bello_Gallico
				if item in ['domain-title-RestOfArt_of_Love']:
					prose = False
	if i+1 == len(annotation):
		nextFeats = []
		nextWord = '</s>'
		nextLem = ['</s>']
	elif len(annotation[i+1].split()) == 0:
		nextFeats = []
		nextWord = '</s>'
		nextLem = ['</s>']
	else:
		nextWord = annotation[i+1].split()[1]
		nextLem = []
		nextFeats = []
		if len(annotation[i+1].split()) > 2:
			for item in annotation[i+1].split()[2:]:
				if 'POSft-lemma=' in item:
					nextLem.append(item.replace('POSft-lemma=',''))
				elif 'domain-' not in item:
					nextFeats.append(item)
				if nextWord == '<COLON>':#
					if '<COLON>' not in nextLem:#
						nextLem.append('<COLON>')#
						
	#########################################################
	if nextWord == '</s>' or i+2 >= len(annotation):
		nextNextWord = None
	elif len(annotation[i+2].split()) == 0:
		nextNextWord = '</s>'	
	else:
		nextNextWord = annotation[i+2].split()[1]
		nextNextLem = []
		nextNextFeats = []
		if len(annotation[i+2].split()) > 2:
			for item in annotation[i+2].split()[2:]:
				if 'POSft-lemma=' in item:
					nextNextLem.append(item.replace('POSft-lemma=',''))
				elif 'domain-' not in item:
					nextNextFeats.append(item)
				if nextNextWord == '<COLON>':#
					if '<COLON>' not in nextNextLem:#
						nextNextLem.append('<COLON>')#
	#########################################################
	
	if len(line.split()) == 0:
		word = '<s>'
		lem = ['<s>']
	else:
		printline += line.split()[0]+'	'+word
		
##########################################################
##########################################################
##########################################################
##########################################################
		if prevPrevWord != None:
			list = getBbiAndTriGrams(prevPrevWord, prevWord, word)
			bBi = list[0]
			bTri = list[1]
			list = getBlemBiAndTriGrams(prevPrevLem, prevLem, lem)
			bBiLem = list[0]
			bTriLem = list[1]
			list = getBPOSbiAndTriGrams(prevPrevFeats, prevFeats, feats)
			bBiPOS = list[0]
			bTriPOS = list[1]
		else:
			bBi = getBbiGrams(prevWord, word)
			bBiLem = getBlemBiGrams(prevLem, lem)
			bBiPOS = getBPOSbiGrams(prevFeats, feats)
			bTri = None
		
		if nextNextWord != None:
			list = getFbiAndTriGrams(word, nextWord, nextNextWord)
			fBi = list[0]
			fTri = list[1]
			list = getFlemBiAndTriGrams(lem, nextLem, nextNextLem)
			fBiLem = list[0]
			fTriLem = list[1]
			list = getFPOSbiAndTriGrams(feats, nextFeats, nextNextFeats)
			fBiPOS = list[0]
			fTriPOS = list[1]		
		else:
			fBi = getFbiGrams(word, nextWord)
			fBiLem = getFlemBiGrams(lem, nextLem)
			fBiPOS = getFPOSbiGrams(feats, nextFeats)
			fTri = None
###############################################################
		
		""" TOGGLE THE FOLLOWING FEATURES ON OR OFF """
		""" BASELINE FEATURES """
		# FEATURE ENGINEERING
		printline = usePOS(printline,feats)
		# printline = addCollectivePOS(printline,feats)
		printline = useDefMorphs(printline,feats)
		printline = useLemmas(printline,lem)
		printline = useNumber(printline,feats)
		printline = addTtlPnctCrdnmAbbrv(printline, word, lem)
		LENNGRAM = 6 # max char Ngram length from word boundary
		printline = addCharacterNgrams(printline,word,LENNGRAM)
		printline = addPrevNNextWord(printline, prevWord, nextWord)
		printline = addPrevNNextLemma(printline,prevLem,nextLem)
		printline = addAllPrevNNextPOS(printline,prevFeats,nextFeats)
		""" BI AND TRIGRAM FEATURES BY WORD, LEM, AND POS """
		# if fTri != None: # FORWARD TRIGRAMS
			# printline += '\t'+fTri
			# printline += '\t'+fTriLem
			# printline += '\t'+fTriPOS
		# if bTri != None: # BACKWARD TRIGRAMS
			# printline += '\t'+bTri
			# printline += '\t'+bTriLem
			# printline += '\t'+bTriPOS
		printline += '\t'+fBi # FORWARD BIGRAMS
		printline += '\t'+fBiLem
		# printline += '\t'+fBiPOS
		printline += '\t'+bBi # BACKWARD TRIGRAMS
		printline += '\t'+bBiLem
		# printline += '\t'+bBiPOS
		""" GAZETTEER FEATURES """
		printline = useGazatteer(printline, word, gazList)
		""" DOMAIN ADAPTATION """
		# printline = DaumeDomAdap(printline, domains, False) #ONLY AUTHOR RIGHT NOW - CAN ADD TITLE LATER
		# printline = addDomain(printline, domains, prose) #ONLY AUTHOR RIGHT NOW - CAN ADD TITLE LATER
		# printline = addProsePoetry(printline, prose)
		# printline = addDaumeProsePoetry(printline, prose)
##########################################################
	
		""" PRINT THAT JANK OUT """
	print printline
