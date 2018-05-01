#!/usr/bin/env python

#
# Takes in a tokenized file of sentences that are to be annotated by some
# oracle. For now, the oracle must manually annotate all tokens since I'm not
# sure how to identify which ones are the unknowns of the sentence. Plus, this
# can not possibly hurt and simply possibly gives the system more information
# than it was asking for.
#
# TODO: One has to ask how this matches with the graphs in the original paper
# and if it matters.
#

import argparse

VALID_ANNOTATIONS = ('GRPU', 'GRPL', 'GRPF', 'PRSU', 'PRSF', 'PRSL', 'GEOU',
                     'GEOF', 'GEOL', '0')
COL_DELIMITER = '\t'

def extract_token_from_line(line):
    cols = line.split(COL_DELIMITER)
    return cols[1]

parser = argparse.ArgumentParser()
parser.add_argument('tb_annotated', help='The file with tokens to be annotated')
args = parser.parse_args()

with open(args.tb_annotated, 'r') as f:
    new_lines = []
    sent_tokens = []
    sent_lines = []

    for line in f:
        line = line.strip()

        if line:
            sent_lines.append(line)
            sent_tokens.append(extract_token_from_line(line))

        if not line:
            sent = ' '.join(sent_tokens)
            print('Next sentence')
            print(sent)

            for sent_line in sent_lines:
                print(sent_line)
                annotation = raw_input('>')

                while annotation not in VALID_ANNOTATIONS:
                    print('NOT A VALID INPUT')
                    annotation = raw_input('>')

                cols = sent_line.split(COL_DELIMITER)
                cols[0] = annotation
                new_line = COL_DELIMITER.join(cols)
                new_lines.append(new_line)

            new_lines.append('')
            print

            del sent_tokens[:]
            del sent_lines[:]

    sent = ' '.join(sent_tokens)
    print('Next sentence')
    print(sent)

    for sent_line in sent_lines:
        print(sent_line)
        annotation = raw_input('>')

        while annotation not in VALID_ANNOTATIONS:
            print('NOT A VALID INPUT')
            annotation = raw_input('>')

        cols = sent_line.split(COL_DELIMITER)
        cols[0] = annotation
        new_line = COL_DELIMITER.join(cols)
        new_lines.append(new_line)

    new_lines.append('')
    print

    del sent_tokens[:]
    del sent_lines[:]

print('\n'.join(new_lines))
