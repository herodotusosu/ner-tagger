### RUN FROM Preprocessed DIRECTORY ###

for d in */
do
echo $d
for f in $d*.txt
do
echo $f
cat $f | python ../removeIchars.py > $f.temp
mv $f.temp $f
cd /usr/local/words
python mainExtractPossiblePOSTagsEXP2.py ../../../home/erdmann/NER/Preprocessing/Preprocessed/$f > ../../../home/erdmann/NER/Preprocessing/Preprocessed/$f.WWW 
cd ../../../home/erdmann/NER/Preprocessing/Preprocessed/

echo William Whitakers Words is Done Analyzing $f
echo Now to filter POS tags by Analysis
echo

####################
python ../filterPOSbyWWW2.py $f $f.WWW > $f.final
cat $f.final | python ../removeColons4crf.py > $f
rm $f.WWW
rm $f.final

# python ../addMetaDataFeats.py $f $author $title > $f.txt
# mv  $f.txt $f

echo Done filtering POS tags by WWW analysis for $f
echo
####################
done
done