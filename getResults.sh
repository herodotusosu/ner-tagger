args=("$@")
file=${args[0]}

cd ../Results

python ../AddingFeatures.py $file.txt domainPlaceHolder lemmaDictionaryPlaceHolder lexTriggerPlaceHolder1 LTPH2 LTPH3 > $file.ftrs

../crfsuite.prog tag -m ../HDT.cls $file.ftrs > predictions.txt

python ../GenPredTest.py $file.ftrs predictions.txt > predictions2.txt

python ../scorerLCcomplete.py predictions2.txt ../BackUpTexts/corpusNoDomAdapNoLT2.ftrs -Complete > results.csv

cat template.csv results.csv > results2.csv

mv results2.csv > results.csv
mv predictions2.txt > predictions.txt