#!/usr/bin/env bash

cur=$(pwd)
SCRIPTPATH="$( cd "$(dirname "$0")" ; pwd -P )"

$SCRIPTPATH/./sentize.py $1 > $1.sent
$SCRIPTPATH/./tokenize.py $1.sent > $1.tok
#rm $1.sent


# TreeTagger
#
# Use the Latin TreeTagger than split on sentences and remove double blank
# lines.
tree-tagger-latin < $1.tok > $1.tt.tagged
python $SCRIPTPATH/removeDoubles.py $1.tt.tagged > $1.tmp
$SCRIPTPATH/./tokenMapping.py $1.tmp > $1.tt
#rm $1.tt.tagged
#rm $1.tmp


# RDRPOSTagger
#
# Head to the RDRPOSTagger and use the pretrained latin models on UD to tag
# the current corpus file.
abs_text_loc="$cur/$1"
cd ~/RDRPOSTagger/jSCRDRtagger
latin_trained_loc='../Models/UniPOS/UD_Latin'
latin_model="${latin_trained_loc}/la-upos.RDR"
latin_dict="${latin_trained_loc}/la-upos.DICT"
java RDRPOSTagger $latin_model $latin_dict $abs_text_loc.tok
cd $cur

python $SCRIPTPATH/processRDR.py $1.tok.TAGGED | python $SCRIPTPATH/removeDoubles.py > $1.tmp
$SCRIPTPATH/./tokenMapping.py $1.tmp > $1.rdr
#rm $1.tmp
#rm $1.tok.TAGGED


# William Whitteker's Words
#
# Now time for morphological analysis that will be combined with
#cat $1.rdr | python $SCRIPTPATH/removeIchars.py > $1.temp
#cd /usr/local/words
#python mainExtractPossiblePOSTagsEXP2.py $cur/$1.temp > $cur/$1.WWW
#cd $cur
#
#echo William Whitakers Words is Done Analyzing $1
#echo Now to filter POS tags by Analysis
#echo
#
#python $SCRIPTPATH/filterRDRPOSbyWWW.py $1.temp $1.WWW > $1.final
##rm $1.WWW
##rm $1.temp
