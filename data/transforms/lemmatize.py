#!/usr/bin/env python

import argparse

#
# This script provides two options for lemmatizing a given annotated NER file.
# The first is to simply use no options, and pass in the file to lemmatize. This
# will simply use the wordform as the lemma and add it as a feature in the form
# of `POSft-lemma={wordform}` in matching to what is expected downstream. Note
# that I will probably change the exact format later to be more general.
#
# The second option is to provide a file through the command line option, --gold.
# This is a parallel file to the to be lemmatized file and features of the form
# `POSft-lemma={lemma}` from this file are transferred to the original file.
#


COL_DELIMITER = '\t'
LEMMA_FEATURE_LABEL = 'POSft-lemma='


def wordform_to_lemma(line):
    return line.split()[1]


def extract_lemma_feat(line):
    cols = line.split(COL_DELIMITER)

    lemma_feat = None
    for col in cols:
        if col.startswith(LEMMA_FEATURE_LABEL):
            lemma_feat = col[len(LEMMA_FEATURE_LABEL):]
            break

    return lemma_feat


parser = argparse.ArgumentParser()
parser.add_argument('input_fn', help='The file to be lemmatized.')
parser.add_argument('--gold', help='The optional, parallel gold standard.')
args = parser.parse_args()


lemmatizer = wordform_to_lemma
if args.gold:
    lemmatizer = extract_lemma_feat


with open(args.input_fn, 'r') as f:
    # In file_pointers, the first pointer will be the file to get the lemma
    # annotation from, and the last pointer will be the file to add the feature
    # to.
    file_pointers = []
    if args.gold:
        gold = open(args.gold, 'r')
        file_pointers.append(gold)
    file_pointers.append(f)

    # For each non empty line in the file, add the lemma annotations.
    for lines in zip(*file_pointers):
        # Since the files are parallel we can just check if the first file has
        # an empty line.
        decoded = [line.decode('utf-8').strip() for line in lines]
        if decoded[0]:
            lemma = lemmatizer(decoded[0])

            if lemma:
                feat = '{}{}'.format(LEMMA_FEATURE_LABEL, lemma)
                decoded[-1] += '\t' + feat

            encoded = decoded[-1].encode('utf-8')
            print(encoded)

    if args.gold:
        gold.close()
