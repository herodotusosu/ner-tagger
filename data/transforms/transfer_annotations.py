#!/usr/bin/env python

#
# Transfer annotations from one file to another. These files are in the format
# of the combined analyses from the morphological analyzer and pos tagger. This
# means each line is a token with a list of relevant features and a NER
# annotation. This script facilitates transferring these annotations between
# different analyses, such as when swapping out the pos tagger. Note that the
# two files must be exactly aligned, token for token.
#
# Usage:
#   ./transfer_annotations.py source.txt dest.txt > output.txt
#

import argparse
import itertools


COL_DELIMITER = '\t'


parser = argparse.ArgumentParser()
parser.add_argument('source', help='The file with the original annotations.')
parser.add_argument('dest', help='The file to transfer the annotations to.')
parser.add_argument('--n', default=-1, type=int,
    help='The number of lines to traverse')
args = parser.parse_args()


with open(args.source, 'r') as source, open(args.dest, 'r') as dest:
    i = 0
    for source_line, dest_line in itertools.izip_longest(source, dest):
        if args.n > 0 and i > args.n and dest_line:
            print(dest_line.strip())
        elif dest_line and source_line:
            source_line = source_line.strip()
            dest_line = dest_line.strip()

            if source_line and dest_line:
                source_cols = source_line.split(COL_DELIMITER)
                dest_cols = dest_line.split(COL_DELIMITER)

                # Transfer the analysis. Note this assumes the two files are
                # aligned!
                dest_cols[0] = source_cols[0]
                new_dest_line = COL_DELIMITER.join(dest_cols)
            else:
                new_dest_line = dest_line

            print(new_dest_line)
            
            i += 1
        else:
            break
