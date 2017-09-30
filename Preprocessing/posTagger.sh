#!/usr/bin/env bash

#
# A caller of many different POS taggers. Pass in the location to search for
# files to tag and pass in the taggers you would like to use. This last feature
# is not made yet, and I'm not sure yet if I will add it. Right now it simply,
# does all POS analyses (TreeTagger and RDRPOSTagger).
#

cur=$(pwd)

for d in */
do
  echo $d
  for f in $d*.txt
  do
    abs_text_loc="$cur/$f"

    ### DO i Need to replace !'s with .'s before sending to Tree Tagger?
    # TreeTagger
    #
    # Use the Latin TreeTagger than split on sentences and remove double blank
    # lines.
    tree-tagger-latin < $f > $f.tmp
    python ../preProcessTree.py $f.tmp | python ../removeDoubles.py > $f.tt
    rm $f.tmp

    # RDRPOSTagger
    #
    # Head to the RDRPOSTagger and use the pretrained latin models on UD to tag
    # the current corpus file.
    python ../tokenizeRDR.py --spaces $f > $f.tok

    cd ~/RDRPOSTagger/jSCRDRtagger
    latin_trained_loc='../Models/UniPOS/UD_Latin'
    latin_model="${latin_trained_loc}/la-upos.RDR"
    latin_dict="${latin_trained_loc}/la-upos.DICT"
    java RDRPOSTagger $latin_model $latin_dict $abs_text_loc.tok
    cd $cur

    python ../preProcessRDR.py $f.tok.TAGGED | python ../removeDoubles.py > $f.rdr
    rm $f.tok
    rm $f.tok.TAGGED
  done
done

echo
echo Done POS tagging $d
echo
