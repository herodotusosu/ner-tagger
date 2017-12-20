#!/usr/bin/env python

#
# This script compares two prediction files (files where the predicted and
# actual NER label are provided) and returns if they are statistically different
# with respect to NE vs non NE classification. Note that for the label to be
# used, if nothing is provided then all NE's are considered.
#

import argparse

import stats


COL_DELIMITER = '\t'
PRED_DELIMITER = ' '
NON_NE_LABEL = '0'


def extract_labels(line):
    """
    Extract the predicted and actual label from a line.

    Args:
    line: The line to extract the information from.

    Returns:
    An ordered pair where the first element is a prediction and the second is
    the actual label.
    """
    labels = line.split(COL_DELIMITER)[0]
    tokens = labels.split(PRED_DELIMITER)
    p, a = tokens[1], tokens[3]

    return (p, a)


def map_can_label(label):
    """
    Labels are marked for whether they are first or last in a sequence. To
    calculate significance across all PRS, or GEO tags, we do not care abou the
    sequencing, so get rid of it.

    Args:
    label: The label to map the canonical version.

    Returns:
    The mapped label.
    """
    if len(label) == 4:
        label = label[:-1]

    return label


parser = argparse.ArgumentParser()
parser.add_argument('pred1', help='The first prediction file.')
parser.add_argument('pred2', help='The second prediction file.')
parser.add_argument('--p', help='The p value to use in McNemar\' test',
                    type=float, default=0.05)
parser.add_argument('--label', help='The label to run McNemar\'s test on',
                    default='')
args = parser.parse_args()


pred_vectors = []
for fn in (args.pred1, args.pred2):
    pred_vec = []
    with open(fn, 'r') as f:
        for line in f:
            line = line.strip()

            if line:
                pred, actual = extract_labels(line)
                pred = map_can_label(pred)
                actual = map_can_label(actual)

                if (not args.label and actual != NON_NE_LABEL) or \
                   (actual == args.label):
                    if pred == actual:
                        pred_vec.append(1)
                    else:
                        pred_vec.append(0)

    pred_vectors.append(pred_vec)

accept_null, _, _ = stats.mcnemars(pred_vectors[0], pred_vectors[1], args.p)

if accept_null:
    print('Results are not too different after all.')
else:
    print('This is no fluke!')
