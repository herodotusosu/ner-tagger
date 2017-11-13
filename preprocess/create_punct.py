#!/usr/bin/env python

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('orig')
parser.add_argument('output')
args = parser.parse_args()


PUNC_ANALYSIS = '0	.	POSft-PUN	POSft-lemma=.	domain-author-Pliny_the_Younger	domain-title-RestOfLetters'


with open(args.orig, 'r') as orig, open(args.output, 'w') as output:
    for line in orig:
        line = line.strip()
        cols = line.split('\t')

        if line:
            token = cols[1]

            if len(token) > 1 and token[-1] == '.':
                cols[1] = token[:-1]
                new_line = '\t'.join(cols)
                output.write(new_line)
                output.write('\n')
                output.write(PUNC_ANALYSIS)
            else:
                output.write(line)

        output.write('\n')
