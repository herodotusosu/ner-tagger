#!/usr/bin/env bash

#
# This script does a reanalysis of provided files and outputs them into a
# provided directory. By tuning the values used in this script, evaluation data
# can undergo different analyses which can be then be easily compared through
# evaluation script as all data is parallel, but with different analyses.
#
# Usage:
#   ./reanalyze.sh src/ dest/
#

SCRIPTPATH="$( cd "$(dirname "$0")" ; pwd -P )"

for f in $1/*
do
  echo $f

  fn=$(basename $f)
  can_fn=${fn%.*}
  $SCRIPTPATH/./reconstruct_sent_tok.py $f > $2/$can_fn.txt
  $SCRIPTPATH/../../preprocess/./analyze.sh -n $2/$can_fn.txt
  $SCRIPTPATH/./transfer_annotations.py $f $2/$can_fn.txt.final > $2/$can_fn.txt.tmp
  mv $2/$can_fn.txt.tmp $2/$can_fn.txt.final
done
