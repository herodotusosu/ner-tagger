#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This is a simple tokenizer. The tokenizer splits on all punctuation and non
# word characters. Punctuation includes basic elements such as '.', ',', '!'
# but also unicode punctuation and more obscure punctuation. This is to ensure
# all downstream tokenizers will understand it the same way even if it is not
# optimal, i.e. some tokenizers might keep abbreviations or acronyms.
#
# Usage:
#   ./tokenize.py input.txt > output.txt
#


import argparse
import re


PUNCTUATION = u'<>.?!-"\'[](){}¿¡„†‡‹‘’“”•–—›»«`%;:,„\\‰'
SPACE = ' '


def space_punc(s):
    new_chars = []
    for i, char in enumerate(s):
        if char in PUNCTUATION:
            if new_chars and new_chars[-1] != SPACE:
                new_chars.append(' ')

            new_chars.append(char)

            if i + 1 < len(s) and s[i + 1] != SPACE:
                new_chars.append(' ')
        else:
            new_chars.append(char)

    new_s = ''.join(new_chars)
    return new_s


parser = argparse.ArgumentParser()
parser.add_argument('filename', help='The file to tokenize')
args = parser.parse_args()

with open(args.filename, 'r') as f:
    for line in f:
        decoded = line.decode('utf-8').strip()
        decoded = space_punc(decoded)
        encoded = decoded.encode('utf-8')
        print(encoded)
