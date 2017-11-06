#!/usr/bin/env python
# -*- coding: utf-8 -*-

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

IGNORE_RDR_PROBLEMS = set(['«', '»', 'Â'])

SPACE = ' '
COL_DELIMETER = '\t'


parser = argparse.ArgumentParser()
parser.add_argument('filename', help='The TreeTagger POS file to process.')
args = parser.parse_args()


with open(args.filename, 'r') as f:
    for i, line in enumerate(f):
        line = line.strip()
        if line:
            line = line.replace('!', '.')
            cols = line.split(COL_DELIMETER)

            # Change any blank intentions with actual blank lines.
            # TODO: WHY THE FUCK IS THERE A LEAVEMOTHERFUCKINGBLANK?
            if cols[0] == 'LEAVEBLANK':
                print
            elif cols[0] not in IGNORE_RDR_PROBLEMS:
                if SPACE in cols[0]:
                    sub_words = cols[0].split(SPACE)
                    for sub_word in sub_words:
                        new_line_cols = [sub_word]
                        new_line_cols.extend(cols[1:])
                        new_line = COL_DELIMETER.join(new_line_cols)

                        print(new_line)
                else:
                    print(line)
