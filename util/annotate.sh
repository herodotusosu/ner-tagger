#!/usr/bin/env sh

#
# Annotate a given file that is already featurized and processed. The main model
# that is used is the HDT.cls model which has achieved the best results to data.
# Usage is as follows:
#
#   ./annotate.sh model.cls file.txt > output.txt
#


SCRIPTPATH="$( cd "$(dirname "$0")" ; pwd -P )"

$SCRIPTPATH/.././crfsuite.prog tag -m $1 $2 > $2_annotated_tmp.txt
$SCRIPTPATH/./splice.py $2_annotated_tmp.txt $2
rm $2_annotated_tmp.txt
