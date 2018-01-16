#!/usr/bin/env python

#
# Splices together the output of CRFSuite after tagging, which is just tags
# with the featurized input.
#

import argparse
import itertools

FEATURE_DELIMITER = '\t'

parser = argparse.ArgumentParser()
parser.add_argument('raw_labels', help='The raw label output from CRFSuite.')
parser.add_argument('original', help='The original file that was tagged.')
args = parser.parse_args()


with open(args.raw_labels, 'r') as raw, open(args.original, 'r') as original:
    for raw_line, orig_line in itertools.izip(raw, original):
        raw_line, orig_line = raw_line.strip(), orig_line.strip()
        orig_items = orig_line.split(FEATURE_DELIMITER)

        orig_items[0] = raw_line
        new_line = FEATURE_DELIMITER.join(orig_items)
        print(new_line)
