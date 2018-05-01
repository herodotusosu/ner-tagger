#!/usr/bin/env python

#
# Ask for annotations of the sentences in the given file.
#

import argparse

def extract_token_from_line(line):
    return line.split('\t')[1]

parser = argparse.ArgumentParser()
parser.add_argument('tb_annotated', help='The file to be annotated')
args = parser.parse_args()

with open(args.tb_annotated, 'r') as f:
    sent_lines = []
    for line in f:
        line = line.strip()

        if line:
            sent_lines.append(line)
        else:
            sent = ' '.join([extract_token_from_line(line) for line in sent_lines])
            print(sent)
            sent_lines = []
