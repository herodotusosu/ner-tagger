#!/usr/bin/env python

#
# Provided a main file and a file with sentences to delete, delete the sentences
# found in the second file, from the first file, and print the rest of the
# contents.
#

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('main', help='The main file.')
parser.add_argument('delete', help='The file with sentences to delete.')
args = parser.parse_args()

sents = []
sent = []
with open(args.delete, 'r') as delete:
    for line in delete:
        line = line.strip()
        cols = line.split()
        if len(cols) > 0:
            word = cols[1]
            sent.append(word)
        else:
            sents.append(sent)
            sent = []

sent = []
printlines = []		
with open(args.main, 'r') as main:
    for line in main:
        line = line.strip()
        cols = line.split()

        if len(cols) > 0:
            word = cols[1]
            sent.append(word)
            printlines.append(line)
        else:
            if sent in sents:
                sents.remove(sent)
            else:
                for l2 in printlines:
                    print l2
                print		
            sent = []
            printlines = []

if sent != []:
    if sent not in sents:
        for l2 in printlines:
            print l2
        print
