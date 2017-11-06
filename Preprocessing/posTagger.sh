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

    # TreeTagger
    #
    # Use the Latin TreeTagger than split on sentences and remove double blank
    # lines.
    python ../tokenizeRDR.py --spaces $f > $f.tt_tok
    tree-tagger-latin < $f.tt_tok > $f.tmp
    python ../preProcessTree.py $f.tmp | python ../removeDoubles.py > $f.tt
    rm $f.tmp
    rm $f.tt_tok

    # RDRPOSTagger
    #
    # Head to the RDRPOSTagger and use the pretrained latin models on UD to tag
    # the current corpus file.
    python ../tokenizeRDR.py --lines --spaces $f > $f.rdr_tok
    iconv -f iso-8859-1 -t utf-8 $f.rdr_tok > $f.rdr_tok.u
    cd ~/RDRPOSTagger/jSCRDRtagger
    latin_trained_loc='../Models/UniPOS/UD_Latin'
    latin_model="${latin_trained_loc}/la-upos.RDR"
    latin_dict="${latin_trained_loc}/la-upos.DICT"
    java RDRPOSTagger $latin_model $latin_dict $abs_text_loc.rdr_tok
    cd $cur

    python ../preProcessRDR.py $f.rdr_tok.TAGGED | python ../removeDoubles.py > $f.rdr
    rm $f.rdr_tok
    rm $f.rdr_tok.TAGGED
  done
done

echo
echo Done POS tagging $d
echo
