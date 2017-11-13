#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# A very crude tokenizer based to parse an input into sentences. A sentence is
# delimited by some end punctuation: '.', '!', '?', followed by a space, or
# by the end of line. With the argument --spaces, spaces are added between words
# and punctuation as well. The argument --lines, tokenizes the input so that
# each line in the input is broken up into one sentence per line.
#
# If the character in front of the period is upper case this is not defined as
# end punctuation, since it is likely an abbreviation for a name in Latin. The
# next character after the end punctuation and space also has to be upper case.
#

import argparse


OPEN_BRACKETS = '([{"'
CLOSED_BRACKETS = '([{"'
END_PUNCTUATION = '.!?'


def is_end_punc(s):
    return s in END_PUNCTUATION


parser = argparse.ArgumentParser()
parser.add_argument('filename', help='The file to tokenize for the RDRPOSTagger')
args = parser.parse_args()

with open(args.filename, 'r') as f:
    for line in f:
        line = line.strip()

        if line:
            bracket_count = 0

            last_sentence = 0
            last_end_punctuation = -1
            for i, char in enumerate(line):
                if is_end_punc(char):
                    last_end_punctuation = i
                elif char in OPEN_BRACKETS:
                    bracket_count += 1
                elif char in CLOSED_BRACKETS:
                    bracket_count = min(0, bracket_count - 1)

                # Consider it the end of the sentence if we are after the
                # last end punctuation, and there is a space after it, and
                # the character before the punc is lower case, and the
                # character after the space is upper case.
                if bracket_count == 0 and \
                   (last_end_punctuation + 1 == i and char == ' ') and \
                   (last_end_punctuation > 0 and line[last_end_punctuation - 1].islower()) and \
                   (last_end_punctuation + 2 < len(line) and line[last_end_punctuation + 2].isupper()):
                    raw = line[last_sentence:last_end_punctuation + 1]
                    sentence = raw

                    print(sentence)

                    # Move last_sentence to where the start of the next sentence
                    # would start assuming a space between the period and next
                    # sentence.
                    last_sentence = last_end_punctuation + 2

            # Print out the remainder of the sentence, since printing stops one
            # sentence short, since either there is no end period or it is the
            # last character.
            remainder = line[last_sentence:]
            print(remainder)
        else:
            print
