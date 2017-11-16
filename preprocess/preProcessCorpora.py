#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Before any processing such as sentizing, tokenizing, or tagging, we need to do
# some light processing. This includes:
#   - Removing certain characters.
#
# This preprocessing will be done on retrieving the original corpora. This
# separates data extraction into a ready to tag and analyze file, from the
# actual analysis.
#
# Usage:
#   ./preTaggingProcess.py input.txt > output.txt
#


import argparse
import sys
import re


REMOVE_CHARS = u'[〈〉]'


parser = argparse.ArgumentParser()
parser.add_argument('filename', help='The file to process')
args = parser.parse_args()


with open(args.filename, 'r') as f:
    for line in f:
        decoded = line.decode('utf-8').strip()

        # Remove the characters we don't want.
        decoded = re.sub(REMOVE_CHARS, '', decoded)
        encoded = decoded.encode('utf-8')
        print(encoded)
