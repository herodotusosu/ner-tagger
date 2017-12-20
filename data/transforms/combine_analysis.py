#!/usr/bin/env python

#
# This script combined two individual analysis. Given two files and two
# identifiers, the script splices together the two analyses. The test label
# should be the same between the analysis. In either case, the label of the
# first analysis is used. Similarly, for the token.
#

import argparse
import sys
import itertools


FEATURE_DELIMITER = '\t'


parser = argparse.ArgumentParser()
parser.add_argument('analysis1', help='The first analysis file.')
parser.add_argument('analysis2', help='The second analysis file.')
parser.add_argument('id1', help='The id for the first analysis features.')
parser.add_argument('id2', help='The id for the second analysis features.')
args = parser.parse_args()


with open(args.analysis1, 'r') as analysis1, \
     open(args.analysis2, 'r') as analysis2:
    zipped_lines = itertools.izip(analysis1, analysis2)

    for lines in zipped_lines:
        lines1, lines2 = lines[0].strip(), lines[1].strip()

        if lines1:
            features1 = lines1.split(FEATURE_DELIMITER)
            features2 = lines2.split(FEATURE_DELIMITER)

            label = features1[0]
            token = features1[1]

            ided_features1 = map(lambda feature: args.id1 + '_' + feature,
                                 features1[2:])
            ided_features2 = map(lambda feature: args.id2 + '_' + feature,
                                 features2[2:])

            combination = [ label, token ] + ided_features1 + ided_features2
            newline = '\t'.join(combination)
            print(newline)
        else:
            print
