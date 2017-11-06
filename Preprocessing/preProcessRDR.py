#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Preprocess output from the RDRPOSTagger specifically. The name of the POS
# tagged file is passed in as the first command line argument. Preprocessing
# consists of removing the LEAVEBLANK lines, and also having one word per line.
# The output of the RDRPOSTagger has multiple words per line, it is a matter of
# putting them on separate lines.
#
# Usage of this script is as follows:
#   ./preProcessRDR.py filename.rdr > processed.rdr
#

import argparse


BLANK_MARKER = 'LEAVEBLANK'

def single_to_double_quote(token):
    return '"'


token_mappings = {
    "''": single_to_double_quote
}


QUESTION_TO_TICK = '�'


parser = argparse.ArgumentParser()
parser.add_argument('filename', help='The POS tagged file to preprocess.')
args = parser.parse_args()

with open(args.filename, 'r') as f:
    for line in f:
        line = line.strip()
        line = line.replace('!', '.')
        tags = line.split()

        for tag in tags:
            split_idx = tag.rfind('/')
            word = tag[:split_idx]
            pos = tag[split_idx + 1:]

            words = word.split(QUESTION_TO_TICK)
            words = [word]

            for word in words:
                try:
                    mapping = token_mappings[word]
                    word = mapping(word)
                except KeyError:
                    pass
                    
                if word == BLANK_MARKER:
                    print
                else:
                    print('{}\t{}'.format(word, pos))

        if len(tags) == 0:
            print
