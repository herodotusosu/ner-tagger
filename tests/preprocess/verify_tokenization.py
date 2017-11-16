#!/usr/bin/env python

#
# Given a folder of preprocessed results, i.e. it has subfolders of authors,
# that have the collection of works of that author, and each file's extension is
# marked for what processing was done on it. The preprocessing folder obviously
# has to have all temporary files still, and not just the final file.
#

import collections
import itertools
import os


POS_EXTENSIONS = set(['tt', 'rdr'])
PRE_PROCESSING_LOCATION = '../../preprocess/Preprocessed'
RDR_ERROR_MATCH = 'null'


def is_ascii(s):
    """
    Checks if a given string is a valid ascii string.

    Args:
    s: The string to check.

    Returns:
    True if the string is a valid ascii string, and False othewise.
    """
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
    folder basis. Files that are counted must have a txt extension. The
    canonical name will be the part before it.

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
            extension = parts[-1]
            try:
                canonical_name = ''.join(parts[:parts.index('txt')])

                if extension in extensions:
                    full_path = os.path.join(root, filename)
                    canonical_names[canonical_name].append(full_path)
            except ValueError:
                pass

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


def test_matching_tokenizations():
    """
    Test that all the preprocessed files are appropriately tokenized. This is
    useful after changing around POS taggers, morphological analyzers, and want
    to make sure that the tokens still line up. So after running the
    preprocessing script you can check that your changes still line up.
    """
    all_matches = True
    failures = []

    for files in walk_canonical_names(PRE_PROCESSING_LOCATION, *POS_EXTENSIONS):
        line_mismatch = match_tokenizations(*files)
        if line_mismatch < 0:
            failures.append('{} not okay at line {}'.format(','.join(files), line_mismatch))

        all_matches = all_matches and line_mismatch < 0

    
    assert all_matches, msg
