### RUN FROM Preprocessed DIRECTORY ###

for d in */
do
  echo $d
  for f in $d*.txt
  do
    echo $f
    cat $f.rdr | python ../removeIchars.py > $f.temp_rdr
    cat $f.tt | python ../removeIchars.py > $f.temp_tt
    cd /usr/local/words
    python mainExtractPossiblePOSTagsEXP2.py ~/NER/preprocess/Preprocessed/$f.temp_rdr > ~/NER/preprocess/Preprocessed/$f.WWW
    cd ~/NER/preprocess/Preprocessed/

    echo William Whitakers Words is Done Analyzing $f
    echo Now to filter POS tags by Analysis
    echo

    ####################
    python ../filterRDRPOSbyWWW.py $f.temp_rdr $f.WWW > $f.final_rdr
    python ../filterPOSbyWWW2.py $f.temp_tt $f.WWW > $f.final_tt
    cat $f.final_rdr | python ../removeColons4crf.py > $f.no_colon_rdr
    # rm $f.WWW
    # rm $f.final
    rm $f.temp_rdr
    rm $f.temp_tt

    # python ../addMetaDataFeats.py $f $author $title > $f.txt
    # mv  $f.txt $f

    echo Done filtering POS tags by WWW analysis for $f
    echo
    ####################
  done
done
