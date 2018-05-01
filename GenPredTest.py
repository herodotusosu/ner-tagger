import sys

#
# Script that takes in a test file and a parallel predictions file. This script
# slices together the two outputs and outputs both in the format:
#   `P: TAG1 A: TAG2 Ea Lemma-ea   Title-Case...`
# where the ellipses represent the annotated and featureized lines.
#
# Usage:
#   ./GenPredTest.py test.ftrs pred.txt > spliced.txt
#

Test = (open(sys.argv[1]).read().splitlines())
Pred  = (open(sys.argv[2]).read().splitlines())

for i in range(0, len(Test)):
	if len(Test[i].split()) == 0:
		print
	else:
		print 'P:', Pred[i], 'A:', Test[i]
