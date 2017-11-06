#!/usr/bin/env bash

#
# A preprocessing script which takes in data from the corpus directory on brutus
# and does its "thang". This "thang" is to extract the author title and text
# from the latin documents stored as XML.
#
# NOTE: This file should be called from the NER/Preprocessing directory as
#       several periphery scripts for this are in here.
#
# Call this script in this format:
#   ./processCorpora.sh corpora/ output/
#
#   corpora: The folder in which to search for files of the form *-lat*.xml
#            which are assumed to be latin corpora.
#   output:  The folder in which to output the results formatted by author and
#            title. This folder will be created if it does not already exist.
#            Note that this folder is in reference to the calling folder for
#            this script, not the folder that contains it.
#

cur=$(pwd)

echo Preprocessing from Perseus XML Data
echo

# Find latin corpora files recursively in first command line argument.
corpora=$(find $1 -name "*-lat*.xml")

for corpus in $corpora
do
	author=$(python authorExtractorXML.py < $corpus)
	title=$(python titleExtractorXML.py < $corpus)

	mkdir -p $cur/$2/$author
	cd $cur/$2/$author
	while [ -e $title.txt ]
	do
		newInt='9'
		title=$title$newInt
	done
	cd $cur

	python perseusExtractorXML.py < $corpus | python removeDoubles.py | python holdBlanks.py > Preprocessed/$author/$title.txt

  # convert to iso-8859-1 to appease crappy TreeTagger
  cp Preprocessed/$author/$title.txt Preprocessed/$author/$title.txt.conv
  iconv -f utf-8 -t iso-8859-1//TRANSLIT Preprocessed/$author/$title.txt.conv > Preprocessed/$author/$title.txt
  #rm Preprocessed/$author/$title.txt.conv

	echo $author, $title, "is ready for POS tagging and Morphological Analysis!"
done
