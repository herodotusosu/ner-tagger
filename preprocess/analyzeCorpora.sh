#!/usr/bin/env bash

#
# A caller of many different POS taggers. Pass in the location to search for
# files to tag and pass in the taggers you would like to use. This last feature
# is not made yet, and I'm not sure yet if I will add it. Right now it simply,
# does all POS analyses (TreeTagger and RDRPOSTagger).
#

cur=$(pwd)

for d in $1/*
do
  echo $d
  for f in $d/*.txt
  do
    ./analyze.sh $f
  done
done

echo
echo Done POS tagging $d
echo
