### RUN FROM Preprocessed DIRECTORY ###

for d in */
do
  echo $d
  for f in $d*.txt
  do
    echo $f
    cat $f.rdr | python ../removeIchars.py > $f.temp
    cd /usr/local/words
    python mainExtractPossiblePOSTagsEXP2.py ~/NER/preprocess/Preprocessed/$f.temp > ~/NER/preprocess/Preprocessed/$f.WWW
    cd ~/NER/preprocess/Preprocessed/

    echo William Whitakers Words is Done Analyzing $f
    echo Now to filter POS tags by Analysis
    echo

    ####################
    python ../filterRDRPOSbyWWW.py $f.temp $f.WWW > $f.coloned
    cat $f.coloned | python ../removeColons4crf.py > $f.final
    rm $f.WWW
    rm $f.coloned
    rm $f.temp

    # python ../addMetaDataFeats.py $f $author $title > $f.txt
    # mv  $f.txt $f

    echo Done filtering POS tags by WWW analysis for $f
    echo
    ####################
  done
done
