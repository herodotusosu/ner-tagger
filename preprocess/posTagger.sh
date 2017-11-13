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
    # convert to iso-8859-1 to appease crappy TreeTagger
    iconv -f utf-8 -t iso-8859-1//TRANSLIT $f > $f.conv
    .././sentize.py $f.conv > $f.sent
    .././utf8-tokenize.perl -s $f.sent > $f.tok
    rm $f.sent
    abs_text_loc="$cur/$f"

    # TreeTagger
    #
    # Use the Latin TreeTagger than split on sentences and remove double blank
    # lines.
    tree-tagger-latin < $f.tok > $f.tt.tagged
    python ../processTT.py $f.tt.tagged | python ../removeDoubles.py > $f.tmp
    .././tokenMapping.py $f.tmp > $f.tt
    rm $f.tt.taggged
    rm $f.tmp

    # RDRPOSTagger
    #
    # Head to the RDRPOSTagger and use the pretrained latin models on UD to tag
    # the current corpus file.
    cd ~/RDRPOSTagger/jSCRDRtagger
    latin_trained_loc='../Models/UniPOS/UD_Latin'
    latin_model="${latin_trained_loc}/la-upos.RDR"
    latin_dict="${latin_trained_loc}/la-upos.DICT"
    java RDRPOSTagger $latin_model $latin_dict $abs_text_loc.tok
    cd $cur

    python ../processRDR.py $f.tok.TAGGED | python ../removeDoubles.py > $f.tmp
    .././tokenMapping.py $f.tmp > $f.rdr
    rm $f.tmp
    rm $f.tok.TAGGED

    # rm $f.tok
  done
done

echo
echo Done POS tagging $d
echo
