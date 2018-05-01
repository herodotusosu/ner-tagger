### From NER/BetaTesting

#
# This script takes in a train, test, and identifier for results files. It then
# adds features to the train and test file and proceeds to train and tag these
# files with the CRF.
#
# Usage:
#   ./BetaTesting.sh train.pp test.pp id
#

args=("$@")
train=${args[0]} #as a .pp file
test=${args[1]} #as a .pp file
id=${args[2]} #Whatever Unique Name you want to give to this beta test

echo Getting features
echo in training set

python ../AddingFeatures.py $train domainPlaceHolder ../Gazetteers/GEOall.txt ../Gazetteers/GEOFs.txt ../Gazetteers/GEOLs.txt ../Gazetteers/GEOMWEs.txt ../Gazetteers/GEOs.txt ../Gazetteers/GEOUs.txt ../Gazetteers/PRSall.txt ../Gazetteers/PRSFs.txt ../Gazetteers/PRSLs.txt ../Gazetteers/PRSMWEs.txt ../Gazetteers/PRSs.txt ../Gazetteers/PRSUs.txt ../Gazetteers/UNKall.txt ../Gazetteers/UNKFs.txt ../Gazetteers/UNKLs.txt ../Gazetteers/UNKMWEs.txt ../Gazetteers/UNKs.txt ../Gazetteers/UNKUs.txt > train$id.ftrs

echo in test set
python ../AddingFeatures.py $test domainPlaceHolder ../Gazetteers/GEOall.txt ../Gazetteers/GEOFs.txt ../Gazetteers/GEOLs.txt ../Gazetteers/GEOMWEs.txt ../Gazetteers/GEOs.txt ../Gazetteers/GEOUs.txt ../Gazetteers/PRSall.txt ../Gazetteers/PRSFs.txt ../Gazetteers/PRSLs.txt ../Gazetteers/PRSMWEs.txt ../Gazetteers/PRSs.txt ../Gazetteers/PRSUs.txt ../Gazetteers/UNKall.txt ../Gazetteers/UNKFs.txt ../Gazetteers/UNKLs.txt ../Gazetteers/UNKMWEs.txt ../Gazetteers/UNKs.txt ../Gazetteers/UNKUs.txt > test$id.ftrs

echo Training and tagging with CRF model
../crfsuite.prog learn -a pa -m crf$id.cls train$id.ftrs
../crfsuite.prog tag -m crf$id.cls test$id.ftrs > pred$id.txt

echo Generating predictions
python ../GenPredTest.py test$id.ftrs pred$id.txt > pred$id.txt2
mv pred$id.txt2 pred$id.txt

echo Calculating Accuracy
python ../scorerLCcomplete.py pred$id.txt train$id.ftrs -Complete > Results/results$id.csv
echo Khalass
