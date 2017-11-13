#!/usr/bin/env python

#
# Preprocess output from the RDRPOSTagger specifically. The name of the POS
# tagged file is passed in as the first command line argument. Preprocessing
# consists of removing the LEAVEBLANK lines, and also having one word per line.
# The output of the RDRPOSTagger has multiple words per line, it is a matter of
# putting them on separate lines.
# Usage of this script is as follows:
#   ./preProcessRDR.py filename.rdr > processed.rdr
#

import argparse


parser = argparse.ArgumentParser()
parser.add_argument('filename', help='The POS tagged file to preprocess.')
args = parser.parse_args()


with open(args.filename, 'r') as f:
    for line in f:
        line = line.strip()
        tags = line.split()

        for tag in tags:
            split_idx = tag.rfind('/')
            word = tag[:split_idx]
            pos = tag[split_idx + 1:]

            print('{}\t{}'.format(word, pos))
        if len(tags) == 0:
            print
