#!/usr/bin/env python3

#
# Takes in a list of files and a NE type (GRP, PRS, GEO) without the F / L
# moniker and provides all words and lists of words that were annotated as such.
#

import argparse

COL_DELIMITER = '\t'

def extract_annotation_from_line(line):
    cols = line.split(COL_DELIMITER)
    return cols[0]

def extract_token_from_line(line):
    cols = line.split(COL_DELIMITER)
    return cols[1]

def map_cannonical_annotation(annotation):
    if len(annotation) >= 4:
        return annotation[:3]

    return annotation

parser = argparse.ArgumentParser()
parser.add_argument('ne_type', help='The type of NE type to look for.')
parser.add_argument('files', nargs='+', help='The files to look over for NEs.')
args = parser.parse_args()

nes = set()
for fn in args.files:
    with open(fn, 'r') as f:
        cur_ne = []
        for line in f:
            line = line.strip()

            label = extract_annotation_from_line(line)
            can_label = map_cannonical_annotation(label)

            if can_label == args.ne_type:
                token = extract_token_from_line(line)
                cur_ne.append(token)
            elif cur_ne:
                nes.add(' '.join(cur_ne))
                del cur_ne[:]

for ne in nes:
    print(ne)
