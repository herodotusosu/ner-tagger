#!/usr/bin/env python

import argparse
import sys


parser = argparse.ArgumentParser()
parser.add_argument('orig')
parser.add_argument('tba')
parser.add_argument('output')
args = parser.parse_args()


with open(args.orig, 'r') as orig, open(args.tba, 'r') as tba, open(args.output, 'w') as output:
    orig_lines = orig.readlines()
    tba_lines = tba.readlines()

    orig_index = 0
    tba_index = 0

    while orig_index < len(orig_lines) and tba_index < len(tba_lines):
        orig_line = orig_lines[orig_index].strip()
        tba_line = tba_lines[tba_index].strip()

        if not tba_line and orig_line:
            output.write('\n')
            tba_index += 1
        else:
            output.write(orig_line)
            output.write('\n')
            tba_index += 1
            orig_index += 1
