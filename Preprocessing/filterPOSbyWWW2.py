#!/usr/bin/env python

import argparse
import sys
from model import *

### Could still do some more sophisticated stuff to recognize -que tackons
## As well as prefixes like per-
## As well as syncopated forms like petierunt and cognosset
## Could also try and deduce what the correct tag is when the tag isn't correct
# but the WWW output combined with the bad tag make it easy to deduce correct tag --- okay so that's not exactly true... they mistakes from the tagger usually stay within the range of allowable tags as determined by www


def _extract_sub(s, sub, direc):
    if direc != 1 or direc != -1:
        raise ValueError('direct must be 1 or -1.')

    start = 0
    end = len(s)

    try:
        if direc == 1:
            end = s.index(sub)
        elif direc == -1:
            start = s.rindex(sub) + len(sub)
    except ValueError:
        if direc == 1:
            end = len(s)
        elif direc == -1:
            start = len(s) - len(sub)

    return s[start:end]

def extract_before_sub(s, sub):
    """
    Extract the substring in s before the first occurence of the string c.

    Args:
    s: The string from which to extract a substring.
    c: The substring to search for.

    Returns:
    The substring before the first occurence of c in s. If c is not in s, then
    the whole string is returned.
    """
    return _extract_sub(s, sub, 1)


def extract_after_sub(s, sub):
    """
    Extract the substring in s after the last occurence of the string sub.

    Args:
    s: The string from which to extract a substring.
    sub: The substring to search for.

    Returns:
    The substring after the last occurence of sub in s. If sub is not in s, then
    the whole string is returned.
    """
    return _extract_sub(s, sub, -1)


# These words cause WWW to enter into an infinite loop.
INFINITE_LOOP_WORDS = set(['decimestres'])

MORPH_ANALYSIS_DELIMETER = ':'
MORPHEME_DELIMETER = '-'


parser = argparse.ArgumentParser()
parser.add_argument('pos', help='The TreeTagger output.')
parser.add_argument('www', help='The WWW output.')
args = parser.parse_args()

pos = (open(args.pos).readlines())
www = (open(args.www).readlines())


suffList = Model('')
testSuffList = Model('')
for line in www:
    for tag in line.split():
        if ':' in tag[0:-1]:
            parsed_word = extract_after_sub(tag, MORPH_ANALYSIS_DELIMETER)
            morphemes = parsed_word.split(MORPHEME_DELIMETER)

            if len(tag.split(':')[-1].split('-')) > 2 or (len(tag.split(':')[-1].split('-')) == 2 and tag.split(':')[-1].split('-')[0] != ''):
                suffList[tag.split(':')[-1].split('-')[-1]] += 1

            if len(morphemes) > 2 or (len(morphemes) == 2 and morphemes[0] != ''):
                testSuffList[morphemes[-1]] += 1


list = []
for suff in suffList:
    list.append('issi'+suff)
    list.append(suff+'que')
for item in list:
    suffList[item] = 1


for i, line in enumerate(pos):
    pos_line_items = line.split()
    www_line_items = www[i].split()
    if len(pos_line_items) == 0:
        print
        continue

    word = pos_line_items[0]
    label = www_line_items[0]
    if word in INFINITE_LOOP_WORDS:
        print label + '\t' + word + '\tnoPOSfts'
    else:
        if len(pos_line_items) == 1 and pos_line_items[0] == '<COLON>':
            pos = 'SENT'
        else:
            pos = pos_line_items[1]

        if len(pos_line_items) > 2:
            pos_lemma = pos_line_items[2]
        else:
            pos_lemma = None

        # Extract the morphological analysis from the WWW output.
        analyses = map(lambda item: extract_before_sub(item, ':'), \
                         www_line_items[2:])

        printline = label + '\t' + word
        okay = 0
        correctTags = []

        ### Now to check if tag is valid
        ### take care of obvious errors
        n = 0
        c = 0
        y = 0
        for analysis in analyses:
            if 'CONJ' in analysis:
                c += 1
            if 'NUM' in analysis:
                n += 1
            y += 1

        if y > 0 and n == y:
            for tag in analyses:
                correctTags.append(tag)
            printline += '\tADJ:NUM'
        elif y > 0 and c == y:
            if pos in ['CC', 'CS']:
                printline += '\t' + pos
            else:
                for tag in analyses:
                    correctTags.append(tag)
                printline += '\tCC'
        ### take care of -que's
        elif word[-3:] == 'que':
            for tag in analyses:
                correctTags.append(tag)
            if 'ADJ' == pos:
                printline += '\t'+pos+':PSTV'
            elif 'V:SUP' in pos:
                printline += '\t'+pos.replace('V:SUP', 'V:SUPINE')
            elif 'ADJ:SUP' == pos:
                printline += '\t'+pos+'ER'
            else:
                printline += '\t'+pos
        ### ESSE:IND and V:IND
        elif 'IND' in pos:
            for tag in analyses:
                if 'IND' in tag:
                    okay = 1
                    correctTags.append(tag)
            if okay == 1:
                printline += '\t'+pos
            else:
                for tag in analyses:
                    if 'ACTIVE' in tag or 'PASSIVE' in tag or 'SUB' in tag or 'IND' in tag:
                        correctTags.append(tag)
                        printline += '\t'+'V'
        ### ESSE:SUB and V:SUB
        elif 'SUB' in pos:
            for tag in analyses:
                if 'SUB' in tag:
                    okay = 1
                    correctTags.append(tag)
            if okay == 1:
                printline += '\t'+pos
            else:
                for tag in analyses:
                    if 'ACTIVE' in tag or 'PASSIVE' in tag or 'IND' in tag or 'SUB' in tag:
                        correctTags.append(tag)
                        printline += '\t'+'V'
        ### ESSE:INF and V:INF
        elif 'INF' in pos:
            for tag in analyses:
                if 'INF' in tag:
                    okay = 1
                    correctTags.append(tag)
            if okay == 1:
                printline += '\t'+pos
            else:
                for tag in analyses:
                    if 'ACTIVE' in tag or 'PASSIVE' in tag or 'SUB' in tag or 'IND' in tag:
                        correctTags.append(tag)
                        printline += '\t'+'V'
        ### V:GER
        elif 'V:GER' == pos:
            for tag in analyses:
                if 'PPL' in tag:
                    okay = 1
                    correctTags.append(tag)
            if okay == 1:
                printline += '\t'+pos
            else:
                for tag in analyses:
                    if 'ACTIVE' in tag or 'PASSIVE' in tag or 'SUB' in tag or 'IND' in tag:
                        correctTags.append(tag)
                        printline += '\t'+'V'
        ### V:GED
        elif 'V:GED' == pos:
            for tag in analyses:
                if 'PPL' in tag:
                    okay = 1
                    correctTags.append(tag)
            if okay == 1:
                printline += '\t'+pos
            else:
                for tag in analyses:
                    if 'ACTIVE' in tag or 'PASSIVE' in tag or 'SUB' in tag or 'IND' in tag:
                        correctTags.append(tag)
                        printline += '\t'+'V'
        ### V:PTC*
        elif 'PTC' in pos:
            partic = 0
            cas = 0
            if len(pos.split(':')) > 2:
                case = pos.split(':')[2]
                for tag in analyses:
                    if 'PPL' in tag and case.upper() in tag:
                        okay = 1
                        correctTags.append(tag)
                if okay == 1:
                    printline += '\t'+pos
                else:
                    for tag in analyses:
                        if 'PPL' in tag:
                            partic = 1
                            correctTags.append(tag)
                    for tag in analyses:
                        if case.upper() in tag:
                            cas = 1
                            correctTags.append(tag)
                    if cas == 1 and partic == 0:
                        printline += '\t'+case
                    elif partic == 1 and cas == 0:
                        printline += '\t'+'V:PTC'
                    elif cas == 1 and partic == 1:
                        correctTags = []
            else:
                for tag in analyses:
                    if 'PPL' in tag:
                        okay = 1
                        correctTags.append(tag)
                if okay == 1:
                    printline += '\t'+pos
        ### V:SUP*
        elif 'V:SUP' in pos:
            case = pos.split(':')[2]
            for tag in analyses:
                    if 'SUPINE' in tag and case.upper() in tag:
                        okay = 1
                        correctTags.append(tag)
            if okay == 1:
                printline += '\t'+pos.replace('SUP','SUPINE')
            else:
                spn = 0
                cas = 0
                for tag in analyses:
                    if 'SUPINE' in tag:
                        spn = 1
                        correctTags.append(tag)
                for tag in analyses:
                    if case.upper() in tag:
                        cas = 1
                        correctTags.append(tag)
                if cas == 1 and spn == 0:
                    printline += '\t' + case
                elif spn == 1 and cas == 0:
                    printline += '\t' + 'V:SUPINE'
                elif cas == 1 and spn == 1:
                    correctTags = []
        ### V:IMP
        elif 'IMP' in pos:
            for tag in analyses:
                if 'IMP' in tag:
                    okay = 1
                    correctTags.append(tag)
            if okay == 1:
                printline += '\t' + pos
        ### REL, DIMOS, INDEF - CONSIDER COMBINING
        elif pos in ['REL', 'DIMOS', 'INDEF']:
            for tag in analyses:
                if 'PRON' in tag:
                    okay = 1
                    correctTags.append(tag)
            if okay == 1:
                printline += '\t' + pos
        ### POSS
        elif pos == 'POSS':
            for tag in analyses:
                if 'POS' in tag:
                    okay = 1
                    correctTags.append(tag)
            if okay == 1:
                printline += '\t' + pos
        ### N:*
        elif 'N:' in pos:
            case = pos.split(':')[1]
            for tag in analyses:
                if case.upper() in tag and 'ADJ' not in tag:
                    okay = 1
                    correctTags.append(tag)
            if okay == 1:
                printline += '\t' + pos
            else:
                cas = 0
                for tag in analyses:
                    if case.upper() in tag:
                        correctTags.append(tag)
                        cas = 1
                if cas == 1:
                    printline += '\t' + case
        ### ADJ*
        elif 'ADJ:NUM' == pos:
            for tag in analyses:
                if 'NUM' in tag:
                    okay = 1
                    correctTags.append(tag)
            if okay == 1:
                printline += '\t' + pos
        elif 'ADJ' == pos:
            for tag in analyses:
                if 'POS-ADJ' in tag:
                    okay = 1
                    correctTags.append(tag)
            if okay == 1:
                printline += '\t' + pos + ':PSTV'
        elif 'ADJ:COM' == pos:
            for tag in analyses:
                if 'COMP-ADJ' in tag:
                    okay = 1
                    correctTags.append(tag)
            if okay == 1:
                printline += '\t' + pos
            else:
                aj = 0
                for tag in analyses:
                    if 'ADJ' in tag:
                        aj = 1
                        correctTags.append(tag)
                if aj == 1:
                    printline += '\tADJ'
        elif 'ADJ:SUP' == pos:
            for tag in analyses:
                if 'SUPER-ADJ' in tag:
                    okay = 1
                    correctTags.append(tag)
            if okay == 1:
                printline += '\t' + pos + 'ER'
            else:
                aj = 0
                for tag in analyses:
                    if 'ADJ' in tag:
                        aj = 1
                        correctTags.append(tag)
                if aj == 1:
                    printline += '\tADJ'
        elif 'ADJ:abl' == pos:
            for tag in analyses:
                if 'ADJ' in tag and 'ABL':
                    okay = 1
                    correctTags.append(tag)
            if okay == 1:
                printline += '\t'+pos
            else:
                aj = 0
                cas = 0
                for tag in analyses:
                    if 'ABL' in tag:
                        cas = 1
                        correctTags.append(tag)
                    if 'ADJ' in tag:
                        aj = 1
                        correctTags.append(tag)
                if aj == 1 and cas == 0:
                    printline += '\tADJ'
                if aj == 0 and cas == 1:
                    printline += '\tabl'
                if aj == 1 and cas == 1:
                    correctTags = []
        ### CS and CC *MAY WANT TO COMBINE
        elif pos in ['CC', 'CS']:
            for tag in analyses:
                if 'CONJ' in tag:
                    okay = 1
                    correctTags.append(tag)
            if okay == 1:
                printline += '\t'+pos
        ### NPR, FW, ABBR, EXCL, SENT, PUN, SYM, CLI, PRON, DET
        elif pos in ['NPR', 'FW', 'ABBR', 'EXCL', 'SENT', 'PUN', 'SYM', 'CLI', 'PRON', 'DET']:
            printline += '\t'+pos
            for tag in analyses:
                correctTags.append(tag)
        ### ADV
        elif 'ADV' == pos:
            for tag in analyses:
                if 'ADV' in tag:
                    okay = 1
                    correctTags.append(tag)
            if okay == 1:
                printline += '\t'+pos
        ### PREP
        elif 'PREP' == pos:
            for tag in analyses:
                if 'PREP' in tag:
                    okay = 1
                    correctTags.append(tag)
            if okay == 1:
                printline += '\t'+pos
        ### INT
        elif 'INT' == pos:
            for tag in analyses:
                if 'INTERJ' in tag:
                    okay = 1
                    correctTags.append(tag)
            if okay == 1:
                printline += '\t' + pos

        """ This considers all output from www when determining number NO MATTER WHAT
            Only asserts that something is singular or plural if there is no discrepency among all the tags it considers"""

        sing = 0
        plur = 0
        for tg in analyses:
            for info in tg.split('-'):
                if info == 'S':
                    sing = 1
                if info == 'P':
                    plur = 1
        if sing == 1 and plur == 0:
            printline += '\tnum-sing'
        if sing == 0 and plur == 1:
            printline += '\tnum-plur'

        """ determine lemmas and morphs for word
            distinguish between definite and possible analyses """

        morphAnalyses = []
        for t in analyses:
            a = t.split(':')[0]
            if a in correctTags:
                morphAnalysis = t.split(':')[1]
                if morphAnalysis not in morphAnalyses:
                    morphAnalyses.append(morphAnalysis)
        if len(morphAnalyses) == 1:
            for m in morphAnalyses:
                for morph in m.split('-'):
                    printline += '\tdefMorpheme='+morph
        for m in morphAnalyses:
            for morph in m.split('-'):
                printline += '\tpotMorpheme='+morph
        if pos_lemma != None:
            printline += '\tlemma='+pos_lemma
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
            printline2 = label+'\t'+word
            for feat in iFeatures:
                printline2 += '    POSft-'+feat
            if nmb != '':
                printline2 += '\t'+nmb
            if 'lemma=<unknown>' in printline2:
                guessedLemma = None
                for n in range(2, len(word)):
                    if word[n:] in suffList:
                        guessedLemma = word[0:n].lower()
                        break
                if guessedLemma == None:
                    guessedLemma = word.lower()
                printline2 += '    POSft-lemma='+guessedLemma

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

            print printline + '\tnoPOSfts'
