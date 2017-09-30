#!/usr/bin/env python

#
# A very crude tokenizer based to parse an input into sentences. A sentence is
# delimited by some end punctuation: '.', '!', '?', followed by a space, or
# by the end of line. With the argument --spaces, spaces are added between words
# and punctuation as well.
#
# If the character in front of the period is upper case this is not defined as
# end punctuation, since it is likely an abbreviation for a name in Latin. The
# next character after the end punctuation and space also has to be upper case.
#

import argparse
import string


def is_punc(s):
    return s in string.punctuation


def add_spaces_between_punc(s):
    chars = []
    for j, tbp in enumerate(s):
        if is_punc(tbp):
            if j > 0 and s[j - 1] != ' ':
                chars.append(' ')

        if j > 0 and is_punc(s[j - 1]) and tbp != ' ':
            chars.append(' ')

        chars.append(tbp)
    return ''.join(chars)


parser = argparse.ArgumentParser()
parser.add_argument('filename', help='The file to tokenize for the RDRPOSTagger')
parser.add_argument('--spaces', help='Insert spaces between words and punctuation',
                    action='store_true')
args = parser.parse_args()

with open(args.filename, 'r') as f:
    for line in f:
        line = line.strip()

        last_sentence = 0
        last_end_punctuation = -1
        for i, char in enumerate(line):
            if char == '.' or char == '!' or char == '?':
                last_end_punctuation = i

            if (last_end_punctuation + 1 == i and char == ' ') and \
               (last_end_punctuation > 0 and line[last_end_punctuation - 1].islower()) and \
               (last_end_punctuation + 2 < len(line) and line[last_end_punctuation + 2].isupper()):
                raw = line[last_sentence:last_end_punctuation + 1]

                # Surround punctuation with spaces if desired.
                if args.spaces:
                    sentence = add_spaces_between_punc(raw)
                else:
                    sentence = raw
                print(sentence)

                # Move last_sentence to where the start of the next sentence
                # would start assuming a space between the period and next
                # sentence.
                last_sentence = last_end_punctuation + 2


        if args.spaces:
            remainder = add_spaces_between_punc(line[last_sentence:])
        else:
            remainder = line[last_sentence:]
        print(remainder)
