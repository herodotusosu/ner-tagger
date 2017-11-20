#!/usr/bin/env python

#
# Reconstruct the an original tokenized file given a test or train file that is
# already tokenized. This is done because there is no actual way to recover the
# authentic source from the raw corpora Perseus data. But we can reconstruct an
# approximation to yield approximate analyses. The parts that matter most likely
# won't change. The reconstruction will be partitioned by sentence as
# partitioned in the input file, where blank lines separate sentences, and will
# already be tokenized, with tokens separated by spaces.
#
# Usage:
#   ./reconstruct_sent_tok.py input.txt > output.txt
#

import argparse


COL_DELIMITER = '\t'
BLANKMARKER = 'LEAVEBLANK'
TOKEN_MAPPINGS = {
    '<COLON>': ':'
}


parser = argparse.ArgumentParser()
parser.add_argument('filename',
                    help='The tokenized, analyzed file to reconstruct')
args = parser.parse_args()

with open(args.filename, 'r') as f:
    next_tokens = []
    for line in f:
        decoded = line.decode('utf-8').strip()

        if decoded:
            cols = decoded.split(COL_DELIMITER)
            token = cols[1]

            try:
                token = TOKEN_MAPPINGS[token]
            except KeyError:
                pass

            next_tokens.append(token)
        else:
            reconstructed_line = ' '.join(next_tokens)
            del next_tokens[:]

            encoded = reconstructed_line.encode('utf-8')
            print(encoded)
            print(BLANKMARKER)
