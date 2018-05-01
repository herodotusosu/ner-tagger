#!/usr/bin/env bash

#
# This is the main analysis script. This script takes in a text file does POS
# tagging, morphological analysis, and filtering of these results to create a
# combined analysis. This is the main preprocessing logic. There are currently
# three available option flags, n, l, and p. If n is set, the input file will
# not be sentized and tokenized, and will be used as is in the analysis. If n is
# set then l must be set, which will provide a lemmatized file. This is necessary
# for now because if you are providing a pretokenized file then the tokenization
# from the TreeTagger analysis here might not match. In which case, the lemmas
# would not correspond between analyses. The p flag uses the UD_Latin-PROIEL
# data rather than the UD_Latin data in the RDR model.
#
# Note that the -n flag must be before the filename, and -l after -n!
#
# Usage:
#   ./analyze.sh [-n] [-p] [-l] lemma.txt input.txt
#

cur=$(pwd)
SCRIPTPATH="$( cd "$(dirname "$0")" ; pwd -P )"
no_tok=0
lemmas_provided=0

# These are the locations of the UD_Latin POS models for RDRPOSTagger. These
# locations can be swapped out with the locations of the UD_Latin-PROIEL model
# with the -p flag.
latin_model_loc='../Models/UniPOS/UD_Latin'
latin_rdr="${latin_model_loc}/la-upos.RDR"
latin_dict="${latin_model_loc}/la-upos.DICT"

while getopts "npl" opt
do
  case $opt in
    n)
      no_tok=1
      ;;
    l)
      lemmas_provided=1
      ;;
    p)
      latin_model_loc='../Models/UniPOS/UD_Latin-PROIEL'
      latin_rdr="${latin_model_loc}/la_proiel-upos.RDR"
      latin_dict="${latin_model_loc}/la_proiel-upos.DICT"
      ;;
  esac
done

# You can not have no_tok and lemmas_provided be different values.
if [ $no_tok -ne $lemmas_provided ]; then
  echo You can not choose no tokenization and not provide a parallel lemma file
  echo for the RDR analysis.
  exit 1
fi

if [ $lemmas_provided -ne 0 ]; then
  f=${@:$OPTIND+1:1}
  fl=${@:$OPTIND:1}
else
  # If there is no preprovided lemma file, then just use the result of the
  # TreeTagger analysis.
  f=${@:$OPTIND:1}
  fl=$f.tt.final
fi

if  [ $no_tok -eq 0 ]; then
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
#abs_tok_loc="$cur/$tokenized_file"
#cd ~/RDRPOSTagger/jSCRDRtagger
#java RDRPOSTagger $latin_rdr $latin_dict $abs_tok_loc
#cd $cur
#
#python $SCRIPTPATH/processRDR.py $tokenized_file.TAGGED > $f.tmp
#$SCRIPTPATH/./tokenMapping.py $f.tmp > $f.rdr
#rm $f.tmp
#rm $tokenized_file.TAGGED
#
#if [ ! $no_tok ]; then
#  rm $tokenized_file
#fi


# William Whittaker's Words
#
# Now time for morphological analysis that will be combined with the POS tagging
# output. First do tree tagger combination then do rdr combination.

# TreeTagger combination
cat $f.tt | python $SCRIPTPATH/removeIchars.py > $f.tt.temp
cd /usr/local/words
python mainExtractPossiblePOSTagsEXP2.py $cur/$f.tt.temp > $cur/$f.tt.WWW
cd $cur

echo William Whitakers Words is Done Analyzing $f TreeTagger analysis
echo Now to filter POS tags by Analysis
echo

python $SCRIPTPATH/filterPOSbyWWW2.py $f.tt.temp $f.tt.WWW > $f.tt.final
rm $f.tt.WWW
rm $f.tt.temp
rm $f.tt

# RDRPOSTagger combination
#cat $f.rdr | python $SCRIPTPATH/removeIchars.py > $f.rdr.temp
#cd /usr/local/words
#python mainExtractPossiblePOSTagsEXP2.py $cur/$f.rdr.temp > $cur/$f.rdr.WWW
#cd $cur
#
#echo William Whitakers Words is Done Analyzing $f RDRPOSTagger analysis
#echo Now to filter POS tags by Analysis
#echo
#
#python $SCRIPTPATH/filterRDRPOSbyWWW.py $f.rdr.temp $f.rdr.WWW > $f.rdr.final
#rm $f.rdr.WWW
#rm $f.rdr.temp
#rm $f.rdr

# Now transfer the lemma analysis from the TreeTagger based files to the
# RDRPOSTagger based files. If the lemma file was provided then use that.
#$SCRIPTPATH/./lemmatize.py $f.rdr.final --gold $fl > $f.rdr.final.lem
#mv $f.rdr.final.lem $f.rdr.final
