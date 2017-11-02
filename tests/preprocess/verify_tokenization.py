#!/usr/bin/env python

#
# Given a folder of preprocessed results, i.e. it has subfolders of authors,
# that have the collection of works of that author, and each file's extension is
# marked for what processing was done on it. The preprocessing folder obviously
# has to have all temporary files still, and not just the final file.
#

import argparse
import itertools
import os


POS_EXTENSIONS = set(['tt', 'rdr'])


def match_tokenizations(*files):
    """
    Verifies that the tokenization for the given files is the same. Each token
    in the preprocessed file is on its own line and sentences are separated by
    new lines. All of this must match between the files.

    Args:
    files: The names of files whose tokenization should be matched.

    Returns:
    The index of the first line where the tokens did not match.
    """
    fs = [open(f) for f in files]

    for i, lines in enumerate(itertools.izip_longest(*fs)):
        # Get the tokens for the current line in each file. If a file ran short
        # or there is a blankline in some file, that is no problem.
        tokens = [line.split('\t')[0] if line else '' for line in lines]

        same = reduce(lambda acc, token: acc and token == tokens[0], tokens)
        if not same:
            return i

    for f in fs:
        f.close()

    return -1


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('loc', help='The file that has the preprocessed content.')
    args = parser.parse_args()

    all_matches = True
    line_index = -1
    pos_tagged = []
    for root, dirs, files in os.walk(args.loc):
        del pos_tagged[:]

        for filename in files:
            extension = filename.split('.')[-1]

            if extension in POS_EXTENSIONS:
                full_path = os.path.join(root, filename)
                pos_tagged.append(full_path)

        line_index = match_tokenizations(*pos_tagged)
        all_matches = line_index < 0
        if not all_matches:
            break

    if not all_matches:
        print('FAILED at line #{} for files {}'.format(line_index, ','.join(pos_tagged)))
    else:
        print('***PASSED***')
