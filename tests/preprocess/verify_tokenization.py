#!/usr/bin/env python

#
# Given a folder of preprocessed results, i.e. it has subfolders of authors,
# that have the collection of works of that author, and each file's extension is
# marked for what processing was done on it. The preprocessing folder obviously
# has to have all temporary files still, and not just the final file.
#

import argparse
import collections
import itertools
import sys
import os


POS_EXTENSIONS = set(['tt', 'rdr'])
RDR_ERROR_MATCH = 'null'


def is_ascii(s):
    try:
        s.decode('ascii')
    except UnicodeDecodeError:
        return False

    return True


def walk_canonical_names(folder, *extensions):
    """
    Walks through a folder hierarchy to provide filenames of files that match a
    given extension. The files are returned based on canonical name (the name
    before the first '.'), and by folder. So batches of files with the same
    canonical name, and extensions from the provided list will be returned on a
    folder basis.

    Args:
    folder: The folder to walk through.
    extensions: The extensions to look for in files.

    Returns:
    Yields batches of files with the same canonical name and desired extensions
    on a folder basis.
    """
    canonical_names = collections.defaultdict(list)

    for root, dirs, files in os.walk(folder):
        canonical_names.clear()

        for filename in files:
            parts = filename.split('.')
            canonical_name, extension = parts[0], parts[-1]

            if extension in extensions:
                full_path = os.path.join(root, filename)
                canonical_names[canonical_name].append(full_path)

        for files in canonical_names.values():
            yield files


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

    res = -1
    for i, lines in enumerate(itertools.izip_longest(*fs)):
        # Get the tokens for the current line in each file. If a file ran short
        # or there is a blankline in some file, that is no problem for this
        # logic. Also RDRPOSTagger has a weird error, where a null POS is given
        # for some words, and no token is provided in the output. We can ignore
        # these lines for now as long as everything else matches.
        tokens = []
        error_on_line = False
        for line in lines:
            line = line.strip()

            if line:
                cols = line.split('\t')
                if len(cols) < 2 or cols[1] != RDR_ERROR_MATCH:
                    token = cols[0]
                    if is_ascii(token):
                        tokens.append(token)
                    else:
                        error_on_line = True
                        break
                else:
                    error_on_line = True
                    break
                    
            else:
                tokens.append('')

        if error_on_line:
            continue

        same = reduce(lambda acc, token: acc and token == tokens[0], tokens, True)
        if not same:
            res = i + 1
            break

    for f in fs:
        f.close()

    return res

def test_tokenizations():
    pass



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('loc', help='The file that has the preprocessed content.')
    args = parser.parse_args()

    all_matches = True
    line_index = -1
    canonical_names = collections.defaultdict(list)
    failed_files = []

    for root, dirs, files in os.walk(args.loc):
        canonical_names.clear()

        for filename in files:
            parts = filename.split('.')
            extension = parts[-1]
            try:
                canonical_name = ''.join(parts[:parts.index('txt')])
            except ValueError:
                print(filename)
                sys.exit(1)

            if extension in POS_EXTENSIONS:
                full_path = os.path.join(root, filename)
                canonical_names[canonical_name].append(full_path)

        for canonical_name, pos_files in canonical_names.items():
            line_index = match_tokenizations(*pos_files)
            all_matches = line_index < 0
            if not all_matches:
                failed_files = pos_files
                break

        if not all_matches:
            break

    if not all_matches:
        print('FAILED at line #{} for files {}'.format(line_index, ','.join(failed_files)))
    else:
        print('***PASSED***')
