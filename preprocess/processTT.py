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


IGNORE_TOKENS = set(['«', '»', 'Â'])
COL_DELIMETER = '\t'


parser = argparse.ArgumentParser()
parser.add_argument('filename', help='The TreeTagger POS file to process.')
args = parser.parse_args()


with open(args.filename, 'r') as f:
    for line in f:
        line = line.strip()
        if line:
            # Ignore all characters that are not appearing in the RDR output.
            cols = line.split(COL_DELIMETER)
            if cols[0] not in IGNORE_TOKENS:
                print(line)
        else:
            print
