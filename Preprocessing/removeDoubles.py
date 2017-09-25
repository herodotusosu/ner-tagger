#!/usr/bin/env python

#
# This script removes duplicate blank lines. If the input contains one blank
# line after another one they are collapsed into one. This script uses stdin so,
# input must be piped, redirected or typed.
#

import sys

blankline_prior = False
for line in sys.stdin:
    if len(line.split()) != 0:
        print line.replace('\n','')
        blankline_prior = False
    else:
        if not blankline_prior:
            print
        blankline_prior = True
