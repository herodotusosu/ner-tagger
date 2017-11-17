#!/usr/bin/env python

#
# Given two files, determine if there are tokenizations are equivalent and if
# they aren't where do they differ.
#


import itertools


aliases = {
    'Chianti': 'cenatio'
}


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


def match_tokenizations(*files, **kwargs):
    """
    Verifies that the tokenization for the given files is the same. Each token
    in the preprocessed file is on its own line and sentences are separated by
    new lines. All of this must match between the files.

    Args:
    files: The names of files whose tokenization should be matched.

    Returns:
    The index of the first line where the tokens did not match.
    """
    col_indices = kwargs.get('col_indices')
    if col_indices is None:
        col_indices = [1] * len(files)

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
        for j, line in enumerate(lines):
            line = line.strip()

            if line:
                cols = line.split('\t')
                index = col_indices[j]
                token = cols[index]

                if is_ascii(token):
                    if token in aliases:
                        token = aliases[token]
                    tokens.append(token.lower())
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


def test_tokenizations(file1, column1, file2, column2):
    """
    Test that all the preprocessed files are appropriately tokenized. This is
    useful after changing around POS taggers, morphological analyzers, and want
    to make sure that the tokens still line up. So after running the
    preprocessing script you can check that your changes still line up.
    """
    if column1 and column2:
        indices = (int(column1), int(column2))
    else:
        indices = None
    line_mismatch = match_tokenizations(file1, file2, col_indices=indices)
    matches = line_mismatch < 0

    if not matches:
        msg = 'FAILED at line #{}'.format(line_mismatch)
    assert matches, msg
