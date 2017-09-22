#!/usr/bin/env bash

#
# A preprocessing script which takes in data from the corpus directory on brutus
# and does its "thang". This "thang" is to extract the author title and text
# from the latin documents stored as XML.
#
# NOTE: This file should be called from the NER/Preprocessing directory as
#       several periphery scripts for this are in here.
#

echo Preprocessing from Perseus XML Data
echo

# Find latin corpora files recursively in first command line argument.
corpora=$(find $1 -name "*-lat*.xml")

for corpus in $corpora
do
	author=$(python authorExtractorXML.py < $corpus)
	title=$(python titleExtractorXML.py < $corpus)

	mkdir -p Preprocessed/$author
	cd Preprocessed/$author
	while [ -e $title.txt ]
	do
		newInt='9'
		title=$title$newInt
	done
	cd ../..

	python perseusExtractorXML.py < $corpus | python removeDoubles.py | python holdBlanks.py > Preprocessed/$author/$title.txt

	echo $author, $title, "is ready for POS tagging and Morphological Analysis!"
done
