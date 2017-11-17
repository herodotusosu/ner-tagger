#!/usr/bin/env python

#
# Post processing on the pos tagged output. This basically maps the POS tagged
# tokens to something else if necessary. For example, ':' is mapped to '<COLON>',
# two double quotes are mapped to a single double quote and so on.
#
# Usage:
#   ./tokenMapping.py input.txt > output.txt
#

import argparse


BLANKMARKER = 'LEAVEBLANK'


def single_to_double_quote(token):
    return '"'


def colon_to_marker(token):
    return '<COLON>'


def excl_to_period(token):
    return '.'


TOKEN_MAPPINGS = {
    "''": single_to_double_quote,
    ':': colon_to_marker,
    '!': excl_to_period
}
COL_DELIMITER = '\t'


parser = argparse.ArgumentParser()
parser.add_argument('filename', help='The file whose tokens to map.')
args = parser.parse_args()


with open(args.filename, 'r') as f:
    for line in f:
        line = line.strip()

        if line:
            cols = line.split(COL_DELIMITER)
            token = cols[0]
            try:
                mapping = TOKEN_MAPPINGS[token]
                token = mapping(token)
                cols[0] = token
            except KeyError:
                pass

            if token == BLANKMARKER:
                print
            else:
                new_line = COL_DELIMITER.join(cols)
                print(new_line)
        else:
            print
