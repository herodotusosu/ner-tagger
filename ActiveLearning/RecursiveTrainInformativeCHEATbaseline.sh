### From NER/BetaTesting

### Run this 3 separate times, once for each train/test split
### Or just combine the three runs with another bash script

args=("$@")
train=${args[0]} #as a .pp file
test=${args[1]} #as a .pp file
testLength=$(cat $test | sed '/^\s*$/d' | wc -l)
sentsAtATime=${args[2]}
origbeta=${args[3]} #Whatever Unique Name you want to give to this beta test
beta=$origbeta
trainLength=$(cat $train | sed '/^\s*$/d' | wc -l)

echo GETTING RESULTS OF INITIAL FULLY SUPERVISED MODEL
./BetaTesting.sh $train $test $beta

mv test$beta.ftrs test.ftrs
mv train$beta.ftrs train.ftrs
	
echo ADDING $sentsAtATime SENTS AT A TIME TO TRAINING DATA FROM TEST SET AND PLOTTING INCREASE IN ACCURACY

while [ $testLength -gt $sentsAtATime ]
do
python getBestSents.py test.ftrs $sentsAtATime -train > delete.txt
cat train.ftrs delete.txt > delete.ftrs
mv delete.ftrs train.ftrs

python getBestSents.py test.ftrs $sentsAtATime -leftOver > newTest.ftrs
mv newTest.ftrs test.ftrs

testLength=$(cat test.ftrs | sed '/^\s*$/d' | wc -l)

echo NEW TEST LENGTH IS $testLength
	
echo Training and tagging with CRF model
../crfsuite.prog learn -a pa -m crf.cls train.ftrs
../crfsuite.prog tag -m crf.cls test.ftrs > pred.txt

echo Generating predictions
python ../GenPredTest.py test.ftrs pred.txt > pred.txt2
mv pred.txt2 pred.txt

echo Calculating Accuracy
python ../scorerLCcomplete.py pred.txt train.ftrs -Complete > Results/results$testLength.csv
echo Khalass

done
