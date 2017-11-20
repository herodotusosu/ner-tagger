#!/usr/bin/env bash

#
# This is the main analysis script. This script takes in a text file does POS
# tagging, morphological analysis, and filtering of these results to create a
# combined analysis. This is the main preprocessing logic. There is currently
# one available option flag, n. If set, the input file will not be sentized and
# tokenized, and will be used as is in the analysis.
#
# Note that the -n flag must be before the filename!
#
# Usage:
#   ./analyze.sh [-n] input.txt
#

cur=$(pwd)
SCRIPTPATH="$( cd "$(dirname "$0")" ; pwd -P )"
no_tok=false

while getopts "n" opt
do
  case $opt in
    n)
      no_tok=true
      ;;
  esac
done

f=${@:$OPTIND:1}
if  [ ! $no_tok ]; then
  $SCRIPTPATH/./sentize.py $f > $f.sent
  $SCRIPTPATH/./tokenize.py $f.sent > $f.tok
  rm $f.sent

  tokenized_file=$f.tok
else
  tokenized_file=$f
fi


# TreeTagger
#
# Use the Latin TreeTagger than split on sentences and remove double blank
# lines.
tree-tagger-latin < $tokenized_file > $f.tt.tagged
$SCRIPTPATH/./tokenMapping.py $f.tt.tagged > $f.tt
rm $f.tt.tagged


# RDRPOSTagger
#
# Head to the RDRPOSTagger and use the pretrained latin models on UD to tag
# the current corpus file.
abs_tok_loc="$cur/$tokenized_file"
cd ~/RDRPOSTagger/jSCRDRtagger
latin_trained_loc='../Models/UniPOS/UD_Latin'
latin_model="${latin_trained_loc}/la-upos.RDR"
latin_dict="${latin_trained_loc}/la-upos.DICT"
java RDRPOSTagger $latin_model $latin_dict $abs_tok_loc
cd $cur

python $SCRIPTPATH/processRDR.py $tokenized_file.TAGGED > $f.tmp
$SCRIPTPATH/./tokenMapping.py $f.tmp > $f.rdr
rm $f.tmp
rm $tokenized_file.TAGGED


# William Whitteker's Words
#
# Now time for morphological analysis that will be combined with the POS tagging
# output.
cat $f.rdr | python $SCRIPTPATH/removeIchars.py > $f.temp
cd /usr/local/words
python mainExtractPossiblePOSTagsEXP2.py $cur/$f.temp > $cur/$f.WWW
cd $cur

echo William Whitakers Words is Done Analyzing $f
echo Now to filter POS tags by Analysis
echo

python $SCRIPTPATH/filterRDRPOSbyWWW.py $f.temp $f.WWW > $f.final
rm $f.WWW
rm $f.temp
