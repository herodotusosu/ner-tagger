#!/usr/bin/env bash

#
# This script combines two different analyses. The analyses here correspond to
# the folders in /data/, such as rdr, utf8, etc. These analyses from these files
# can be combined line by line. To distinguish the analysis from each other each
# feature from the analyses will be prepended with the analysis name. One caveat
# is that files are only combined if they have the same name. This means the
# files within each folder must have the same names.
#
# Usage:
#   ./combine.sh analysis-1/ analysis-2/ dest/
#

SCRIPTPATH="$( cd "$(dirname "$0")" ; pwd -P )"

dest=$3
mkdir $dest

analysis1=$1
analysis2=$2

for f in $analysis1/*
do
  bn=$(basename $f)
  echo Combining on $bn

  id1=$(basename $analysis1)
  id2=$(basename $analysis2)
  $SCRIPTPATH/./combine_analysis.py $f $analysis2/$bn $id1 $id2 > $dest/$bn
done
