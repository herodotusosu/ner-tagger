import sys
from model import *
### Could still do some more sophisticated stuff to recognize -que tackons
## As well as prefixes like per-
## As well as syncopated forms like petierunt and cognosset
## Could also try and deduce what the correct tag is when the tag isn't correct
# but the WWW output combined with the bad tag make it easy to deduce correct tag --- okay so that's not exactly true... they mistakes from the tagger usually stay within the range of allowable tags as determined by www

pos = (open(sys.argv[1]).read().splitlines())
www = (open(sys.argv[2]).read().splitlines())
suffList = Model('')
for line in www:
	for tag in line.split():
		if ':' in tag[0:-1]:
			if len(tag.split(':')[-1].split('-')) > 2 or (len(tag.split(':')[-1].split('-')) == 2 and tag.split(':')[-1].split('-')[0] != ''):
				#if tag.split(':')[-1].split('-')[-1] not in suffList:
				suffList[tag.split(':')[-1].split('-')[-1]] += 1
					#print tag.split(':')[-1].split('-')[-1],
					# print tag.split(':')[-1]
					# print
list = []
for suff in suffList:
	list.append('issi'+suff)
	list.append(suff+'que')
for item in list:
	suffList[item] = 1

i = 0
for line in pos:
	if len(line.split()) == 0:
		print
	else:
		word = line.split()[0]
		label = www[i].split()[0]
		if word in ['decimestres']:### for whatever reason this word causes wwwords to get stuck in an infinite loop
			print label+'	'+word+'	noPOSfts'
		else:
			if len(line.split()) == 1 and line.split()[0] == '<COLON>':
				pTag = 'SENT'
			else:
				pTag = line.split()[1]
			if len(line.split()) > 2:
				POSlemma = line.split()[2]
			else:
				POSlemma = None
			tagChoices = www[i].split()[2:]
			tChoices = tagChoices
			TagChoices = []
			for tg in tagChoices:
				TagChoices.append(tg.split(':')[0])
			tagChoices = TagChoices
			n = 0
			c = 0
			y = 0
			for g in tagChoices:
				if 'CONJ' in g.split(':')[0]:
					c += 1
				if 'NUM' in g.split(':')[0]:
					n += 1
				y += 1
			printline = label+'	'+word
			### Now to check if tag is valid
			okay = 0
			correctTags = []
			### take care of obvious errors
			if y > 0 and n == y:
				for tag in tagChoices:
					correctTags.append(tag)
				printline += '	ADJ:NUM'
			elif y > 0 and c == y:
				if pTag in ['CC', 'CS']:
					printline += '	'+pTag
				else:
					for tag in tagChoices:
						correctTags.append(tag)
					printline += '	CC'
			### take care of -que's
			elif word[-3:] == 'que':
				for tag in tagChoices:
					correctTags.append(tag)
				if 'ADJ' == pTag:
					printline += '	'+pTag+':PSTV'
				elif 'V:SUP' in pTag:
					printline += '	'+pTag.replace('V:SUP', 'V:SUPINE')
				elif 'ADJ:SUP' == pTag:
					printline += '	'+pTag+'ER'
				else:
					printline += '	'+pTag
			### ESSE:IND and V:IND
			elif 'IND' in pTag:
				for tag in tagChoices:
					if 'IND' in tag:
						okay = 1
						correctTags.append(tag)
				if okay == 1:
					printline += '	'+pTag
				else:
					for tag in tagChoices:
						if 'ACTIVE' in tag or 'PASSIVE' in tag or 'SUB' in tag or 'IND' in tag:
							correctTags.append(tag)
							printline += '	'+'V'
			### ESSE:SUB and V:SUB
			elif 'SUB' in pTag:
				for tag in tagChoices:
					if 'SUB' in tag:
						okay = 1
						correctTags.append(tag)
				if okay == 1:
					printline += '	'+pTag
				else:
					for tag in tagChoices:
						if 'ACTIVE' in tag or 'PASSIVE' in tag or 'SUB' in tag or 'IND' in tag:
							correctTags.append(tag)
							printline += '	'+'V'
			### ESSE:INF and V:INF
			elif 'INF' in pTag:
				for tag in tagChoices:
					if 'INF' in tag:
						okay = 1
						correctTags.append(tag)
				if okay == 1:
					printline += '	'+pTag
				else:
					for tag in tagChoices:
						if 'ACTIVE' in tag or 'PASSIVE' in tag or 'SUB' in tag or 'IND' in tag:
							correctTags.append(tag)
							printline += '	'+'V'
			### V:GER
			elif 'V:GER' == pTag:
				for tag in tagChoices:
					if 'PPL' in tag:
						okay = 1
						correctTags.append(tag)
				if okay == 1:
					printline += '	'+pTag
				else:
					for tag in tagChoices:
						if 'ACTIVE' in tag or 'PASSIVE' in tag or 'SUB' in tag or 'IND' in tag:
							correctTags.append(tag)
							printline += '	'+'V'
			### V:GED
			elif 'V:GED' == pTag:
				for tag in tagChoices:
					if 'PPL' in tag:
						okay = 1
						correctTags.append(tag)
				if okay == 1:
					printline += '	'+pTag
				else:
					for tag in tagChoices:
						if 'ACTIVE' in tag or 'PASSIVE' in tag or 'SUB' in tag or 'IND' in tag:
							correctTags.append(tag)
							printline += '	'+'V'
			### V:PTC*
			elif 'PTC' in pTag:
				partic = 0
				cas = 0
				if len(pTag.split(':')) > 2:
					case = pTag.split(':')[2]
					for tag in tagChoices:
						if 'PPL' in tag and case.upper() in tag:
							okay = 1
							correctTags.append(tag)
					if okay == 1:
						printline += '	'+pTag		
					else:
						for tag in tagChoices:
							if 'PPL' in tag:
								partic = 1
								correctTags.append(tag)
						for tag in tagChoices:
							if case.upper() in tag:
								cas = 1
								correctTags.append(tag)
						if cas == 1 and partic == 0:
							printline += '	'+case
						elif partic == 1 and cas == 0:
							printline += '	'+'V:PTC'
						elif cas == 1 and partic == 1:
							correctTags = []
				else:
					for tag in tagChoices:
						if 'PPL' in tag:
							okay = 1
							correctTags.append(tag)
					if okay == 1:
						printline += '	'+pTag
			### V:SUP*
			elif 'V:SUP' in pTag:
				case = pTag.split(':')[2]
				for tag in tagChoices:
						if 'SUPINE' in tag and case.upper() in tag:
							okay = 1
							correctTags.append(tag)
				if okay == 1:
					printline += '	'+pTag.replace('SUP','SUPINE')
				else:
					spn = 0
					cas = 0
					for tag in tagChoices:
						if 'SUPINE' in tag:
							spn = 1
							correctTags.append(tag)
					for tag in tagChoices:
						if case.upper() in tag:
							cas = 1
							correctTags.append(tag)
					if cas == 1 and spn == 0:
						printline += '	'+case
					elif spn == 1 and cas == 0:
						printline += '	'+'V:SUPINE'
					elif cas == 1 and spn == 1:
						correctTags = [] 					
			### V:IMP
			elif 'IMP' in pTag:
				for tag in tagChoices:
					if 'IMP' in tag:
						okay = 1
						correctTags.append(tag)
				if okay == 1:
					printline += '	'+pTag
			### REL, DIMOS, INDEF - CONSIDER COMBINING
			elif pTag in ['REL', 'DIMOS', 'INDEF']:
				for tag in tagChoices:
					if 'PRON' in tag:
						okay = 1
						correctTags.append(tag)
				if okay == 1:
					printline += '	'+pTag
			### POSS
			elif pTag == 'POSS':
				for tag in tagChoices:
					if 'POS' in tag:
						okay = 1
						correctTags.append(tag)
				if okay == 1:
					printline += '	'+pTag
			### N:*
			elif 'N:' in pTag:
				case = pTag.split(':')[1]
				for tag in tagChoices:
					if case.upper() in tag and 'ADJ' not in tag:
						okay = 1
						correctTags.append(tag)
				if okay == 1:
					printline += '	'+pTag
				else:
					cas = 0
					for tag in tagChoices:
						if case.upper() in tag:
							correctTags.append(tag)
							cas = 1
					if cas == 1:
						printline += '	'+case
			### ADJ*
			elif 'ADJ:NUM' == pTag:
				for tag in tagChoices:
					if 'NUM' in tag:
						okay = 1
						correctTags.append(tag)
				if okay == 1:
					printline += '	'+pTag
			elif 'ADJ' == pTag:
				for tag in tagChoices:
					if 'POS-ADJ' in tag:
						okay = 1
						correctTags.append(tag)
				if okay == 1:
					printline += '	'+pTag+':PSTV'
			elif 'ADJ:COM' == pTag:
				for tag in tagChoices:
					if 'COMP-ADJ' in tag:
						okay = 1
						correctTags.append(tag)
				if okay == 1:
					printline += '	'+pTag
				else:
					aj = 0
					for tag in tagChoices:
						if 'ADJ' in tag:
							aj = 1
							correctTags.append(tag)
					if aj == 1:
						printline += '	ADJ'						
			elif 'ADJ:SUP' == pTag:
				for tag in tagChoices:
					if 'SUPER-ADJ' in tag:
						okay = 1
						correctTags.append(tag)
				if okay == 1:
					printline += '	'+pTag+'ER'
				else:
					aj = 0
					for tag in tagChoices:
						if 'ADJ' in tag:
							aj = 1
							correctTags.append(tag)
					if aj == 1:
						printline += '	ADJ'
			elif 'ADJ:abl' == pTag:
				for tag in tagChoices:
					if 'ADJ' in tag and 'ABL':
						okay = 1
						correctTags.append(tag)
				if okay == 1:
					printline += '	'+pTag
				else:
					aj = 0
					cas = 0
					for tag in tagChoices:
						if 'ABL' in tag:
							cas = 1
							correctTags.append(tag)
						if 'ADJ' in tag:
							aj = 1
							correctTags.append(tag)
					if aj == 1 and cas == 0:
						printline += '	ADJ'
					if aj == 0 and cas == 1:
						printline += '	abl'
					if aj == 1 and cas == 1:
						correctTags = []
			### CS and CC *MAY WANT TO COMBINE
			elif pTag in ['CC', 'CS']:
				for tag in tagChoices:
					if 'CONJ' in tag:
						okay = 1
						correctTags.append(tag)
				if okay == 1:
					printline += '	'+pTag
			### NPR, FW, ABBR, EXCL, SENT, PUN, SYM, CLI, PRON, DET
			elif pTag in ['NPR', 'FW', 'ABBR', 'EXCL', 'SENT', 'PUN', 'SYM', 'CLI', 'PRON', 'DET']:
				printline += '	'+pTag
				for tag in tagChoices:
					correctTags.append(tag)
			### ADV
			elif 'ADV' == pTag:
				for tag in tagChoices:
					if 'ADV' in tag:
						okay = 1
						correctTags.append(tag)
				if okay == 1:
					printline += '	'+pTag
			### PREP
			elif 'PREP' == pTag:
				for tag in tagChoices:
					if 'PREP' in tag:
						okay = 1
						correctTags.append(tag)
				if okay == 1:
					printline += '	'+pTag
			### INT
			elif 'INT' == pTag:
				for tag in tagChoices:
					if 'INTERJ' in tag:
						okay = 1
						correctTags.append(tag)
				if okay == 1:
					printline += '	'+pTag	
#########################################################################
			""" This considers all output from www when determining number only when no correct tag was found
				However, if one or more correct tags were found, only considers number as proposed by those tags 
				Only asserts that something is singular or plural if there is no discrepency among all the tags it considers"""
			""" ### Determine Number for unsuccessful tags
			if len(correctTags) == 0:
				sing = 0
				plur = 0
				for tg in tagChoices:
					for info in tg.split('-'):
						if info == 'S':
							sing = 1
						if info == 'P':
							plur = 1
				if sing == 1 and plur == 0:
					printline += '	num-sing'
				if sing == 0 and plur == 1:
					printline += '	num-plur'
			
			### Determine Number for successful tags
			else:
				sing = 0
				plur = 0
				for t in correctTags:
					for info in t.split('-'):
						if info == 'S':
							sing = 1
						if info == 'P':
							plur = 1
				if sing == 1 and plur == 0:
					printline += '	num-sing'
				if sing == 0 and plur == 1:
					printline += '	num-plur' """
			
			### Print without dividing up features
			#print printline.replace(':', '-')
#########################################################################
			""" This considers all output from www when determining number NO MATTER WHAT
				Only asserts that something is singular or plural if there is no discrepency among all the tags it considers"""
			
			sing = 0
			plur = 0
			for tg in tagChoices:
				for info in tg.split('-'):
					if info == 'S':
						sing = 1
					if info == 'P':
						plur = 1
			if sing == 1 and plur == 0:
				printline += '	num-sing'
			if sing == 0 and plur == 1:
				printline += '	num-plur'

#########################################################################
			
			#####################################################
			""" determine lemmas and morphs for word
				distinguish between definite and possible analyses """
			
			morphAnalyses = []
			for t in tChoices:
				a = t.split(':')[0]
				if a in correctTags:
					morphAnalysis = t.split(':')[1]
					if morphAnalysis not in morphAnalyses:
						morphAnalyses.append(morphAnalysis)
			if len(morphAnalyses) == 1:
				for m in morphAnalyses:
					for morph in m.split('-'):
						printline += '	defMorpheme='+morph
			for m in morphAnalyses:
				for morph in m.split('-'):
					printline += '	potMorpheme='+morph
			if POSlemma != None:
				printline += '	lemma='+POSlemma
			#####################################################
			
			### Print by dividing up POS info into individual components
			if len(printline.split()) > 2:
				nmb = ''
				iFeatures = []
				for fts in printline.split()[2:]:
					if fts not in ['num-sing', 'num-plur']:
						FtS = fts.replace(':', '-').split('-')
						for FTS in FtS:
							iFeatures.append(FTS)
					else:
						nmb = fts
				printline2 = label+'	'+word
				for feat in iFeatures:
					printline2 += '	POSft-'+feat
				if nmb != '':
					printline2 += '	'+nmb
				if 'lemma=<unknown>' in printline2:
					guessedLemma = None
					for n in range(2, len(word)):
						if word[n:] in suffList:
							guessedLemma = word[0:n].lower()
							break
					if guessedLemma == None:
						guessedLemma = word.lower()
					printline2 += '	POSft-lemma='+guessedLemma
					
				### Don't add null lemmas or morphemes
				if len(printline2.split()) > 0:
					wrd = printline2.split()[1]
					printline3 = printline2.split()[0]
					for ft in printline2.split()[1:]:
						if len(ft) > 5 and 'lemma=' == ft[-6:]:
							printline3 += '\t'+ft+wrd
						elif len(ft) > 8  and 'Morpheme=' == ft[-9:]:
							pass
						elif len(ft) > 5 and 'POSft-' == ft[-6:]:
							pass
						else:
							printline3 += '\t'+ft
					printline2 = printline3
					
				print printline2
					
			else:### Doesn't do anything right now because lemma feature will always at least return unknown... which is essentially the same feature as noPOSfts
			
				### Don't add null lemmas or morphemes
				if len(printline.split()) > 0:
					wrd = printline.split()[1]
					printline2 = printline.split()[0]
					for ft in printline.split()[1:]:
						if len(ft) > 5 and 'lemma=' == ft[-6:]:
							printline2 += '\t'+ft+wrd
						elif len(ft) > 8  and 'Morpheme=' == ft[-9:]:
							pass
						elif len(ft) > 5 and 'POSft-' == ft[-6:]:
							pass
						else:
							printline2 += '\t'+ft
					printline = printline2
				
				print printline+'	noPOSfts'

	i += 1