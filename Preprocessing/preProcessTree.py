#!/usr/bin/env python

#
# Do preprocessing on the Latin TreeTagger output. The two main items this
# accomplishes are:
#
# (1) Replace LEAVEBLANKs from the Perseus data with actual blank lines.
# (2) Put a blank line between sentences as well, such as end punctuation.
#
# Usage of this script is as follows:
#   ./preProcessTree.py filename > processed.txt
#

import argparse


parser = argparse.ArgumentParser()
parser.add_argument('filename', help='The TreeTagger POS file to process.')
args = parser.parse_args()


CW = (open(args.filename).read().splitlines())
# CW = sys.argv[1].splitlines()
# CW = sys.stdin #Use this version of CW if running perseusExtractor.sh

for i, line in enumerate(CW):
    line = line.replace('!','.')

    # Change any blank intentions with actual blank lines.
    if line.split()[0] == 'LEAVEBLANK':
        print
    else:
        print line.replace('\n','')

        if line.split()[1] == 'SENT':
        # Print out a blank line if a sentence end and the next token is not
        # another punctuation.

            if len(CW[i + 1].split()) > 0 and CW[i + 1].split()[1]:
                if CW[i + 1].split()[1] != 'PUN':
                    print
            else:
                print
        elif line.split()[1] == 'PUN':
        # Consecutive punctuation should be separated by blank lines, except
        # for the first two punctuation marks.
        # TODO: Ask Alex why this is in place.

            if i > 0 and len(CW[i-1].split()) > 0 and CW[i-1].split()[1] == 'SENT':
                print
            elif i > 1 and len(CW[i-1].split()) > 0 and len(CW[i-2].split()) > 0 and CW[i-1].split()[1] == 'PUN' and CW[i-2].split()[1] == 'SENT':
                print
