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

tt=0
rdr=0
rdr_proiel=0
while getopts "trp" opt
do
  case $opt in
    t)
      tt=1
      ;;
    r)
      rdr=1
      ;;
    p)
      rdr_proiel=1
      ;;
  esac
done


if [ $(($rdr_proiel + $tt + $rdr)) -ne 1 ]; then
  echo 'You must pick exactly one POS analysis.'
  exit 1
fi

src=${@:$OPTIND:1}
dest=${@:$OPTIND+1:1}

for f in $src/*
do
  echo $f

  fn=$(basename $f)
  can_fn=${fn%.*}
  $SCRIPTPATH/./reconstruct_sent_tok.py $f > $dest/$can_fn.txt

  if [ $tt -eq 1 ]; then
    $SCRIPTPATH/../../preprocess/./analyze.sh -n -l $f $dest/$can_fn.txt
    mv $dest/$can_fn.txt.tt.final $dest/$can_fn.pp

    # Delete the other unneeded analysis.
    rm $dest/$can_fn.txt.rdr.final
  else
    if [ $rdr_proiel -eq 1 ]; then
      $SCRIPTPATH/../../preprocess/./analyze.sh -n -p -l $f $dest/$can_fn.txt
    else
      $SCRIPTPATH/../../preprocess/./analyze.sh -n -l $f $dest/$can_fn.txt
    fi
    mv $dest/$can_fn.txt.rdr.final $dest/$can_fn.pp

    # Delete the other, unneeded, analysis.
    rm $dest/$can_fn.txt.tt.final
  fi


  $SCRIPTPATH/./transfer_annotations.py $f $dest/$can_fn.pp > $dest/$can_fn.pp.tmp
  mv $dest/$can_fn.pp.tmp $dest/$can_fn.pp
done
