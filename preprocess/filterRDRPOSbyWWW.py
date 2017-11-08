#!/usr/bin/env python

#
# This script takes in a file tagged by the RDRPOSTagger and a file tagged by
# a morphological analyzer, in this case WWW, and creates an output that matches
# these two analyses. The output will have each word labeled with definite and
# possible lemmas, morphemes, and pos. Usage is as follows:
#


import argparse
import itertools

from analysismatcher import AnalysisMatcher
from featurestore import FeatureStore


RDR_ERROR_MATCH = 'null'
COL_DELIMETER = '\t'
ANALYSIS_DELIMETER = ':'
MORPH_FEATURE_DELIMETER = '-'
MORPHEME_DELIMETER = '-'


# The different ways these POS are identified in the WWW output.
# TODO: How to handle part, det
NOUN_CASES = ['NOM', 'DAT', 'GEN', 'LOC', 'ACC', 'ABL', 'VOC']
VERB_CASES = ['IND', 'SUB', 'INF', 'PPL', 'ACTIVE', 'PASSIVE', 'IMP']
ADJ_CASES = ['POS-ADJ', 'COMP-ADJ', 'SUPER-ADJ', 'ADJ', 'POS']
WHITE_LIST_POS = ['PROPN', 'X', 'PUNCT', 'SYM', 'PART']


parser = argparse.ArgumentParser()
parser.add_argument('rdr', help='The location of the rdr pos tagged file.')
parser.add_argument('www', help='The location of the www analyzed file.')
args = parser.parse_args()

rdr_matcher = AnalysisMatcher(morph_feature_splitter=MORPH_FEATURE_DELIMETER)

# POS tags for which we have an answer in WWW output.
rdr_matcher.add_rule('VERB', *VERB_CASES)
rdr_matcher.add_rule('AUX', *VERB_CASES)
rdr_matcher.add_rule('PRON', 'PRON')

rdr_matcher.add_rule('NOUN', *NOUN_CASES)
rdr_matcher.add_neg('NOUN', 'ADJ')

rdr_matcher.add_rule('NUM', 'NUM')
rdr_matcher.add_rule('ADJ', *ADJ_CASES)
rdr_matcher.add_rule('CCONJ', 'CONJ')
rdr_matcher.add_rule('SCONJ', 'CONJ')
rdr_matcher.add_rule('ADV', 'ADV')
rdr_matcher.add_rule('ADP', 'PREP')
rdr_matcher.add_rule('INTJ', 'INTERJ')

# POS tags for which we have no answer in WWW output.
for pos in WHITE_LIST_POS:
    rdr_matcher.add_white_list(pos)


with open(args.rdr, 'r') as rdr, open(args.www, 'r') as www:
    for rdr_line, www_line in itertools.izip(rdr, www):
        rdr_line = rdr_line.strip()
        www_line = www_line.strip()

        if rdr_line and www_line:
            rdr_cols = rdr_line.split(COL_DELIMETER)
            www_cols = www_line.split(COL_DELIMETER)
            feature_store = FeatureStore()

            if len(www_cols) > 2:
                # TODO: Some repetitive structure between these code blocks (if and else).
                pos = rdr_cols[1]
                morph_analyses = www_cols[2:]

                if rdr_cols[1] == RDR_ERROR_MATCH:
                    feature_store.add_singleton('RDR-NO-ANALYSIS', 0)
                    break
                else:
                    feature_store.add_key('RDR-POS', 1)
                    feature_store.add_feature('RDR-POS', pos)

                feature_store.add_key('WWW-POT-MORPHEMES', 2)

                for morph_analysis in morph_analyses:
                    morphology, morpheme_raw = morph_analysis.split(ANALYSIS_DELIMETER)
                    morphemes = morpheme_raw.split(MORPHEME_DELIMETER)

                    # The pos analysis matched the morphological analysis in
                    # some way. Now add the morphemes here to the features.
                    if rdr_matcher.match(pos, morphology):
                        for morpheme in morphemes:
                            feature_store.add_feature('WWW-POT-MORPHEMES', morpheme)

            else:
                pos = rdr_cols[1]
                feature_store.add_key('RDR-POS', 1)
                feature_store.add_feature('RDR-POS', pos)

            feat_output = feature_store.output()
            new_line = '0\t{}\t{}'.format(rdr_cols[0], feat_output)
            print(new_line)
        else:
            print
