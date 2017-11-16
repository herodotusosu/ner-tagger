#!/usr/bin/env python

#
# TODO:
#

import argparse


def single_to_double_quote(token):
    return '"'


def colon_to_marker(token):
    return '<COLON>'


def excl_to_period(token):
    return '!'


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

            new_line = COL_DELIMITER.join(cols)
            print(new_line)
        else:
            print
