### RUN FROM Preprocessed DIRECTORY ###

for d in */
do
  echo $d
  for f in $d*.txt
  do
    echo $f
    cat $f.tt | python ../removeIchars.py > $f.temp
    cd /usr/local/words
    python mainExtractPossiblePOSTagsEXP2.py ~/NER/Preprocessing/Preprocessed/$f.temp > ~/NER/Preprocessing/Preprocessed/$f.WWW
    cd ~/NER/Preprocessing/Preprocessed/

    echo William Whitakers Words is Done Analyzing $f
    echo Now to filter POS tags by Analysis
    echo

    ####################
    python ../filterPOSbyWWW2.py $f.temp $f.WWW > $f.final
    cat $f.final | python ../removeColons4crf.py > $f.no_colon
    # rm $f.WWW
    # rm $f.final
    rm $f.temp

    # python ../addMetaDataFeats.py $f $author $title > $f.txt
    # mv  $f.txt $f

    echo Done filtering POS tags by WWW analysis for $f
    echo
    ####################
  done
done
