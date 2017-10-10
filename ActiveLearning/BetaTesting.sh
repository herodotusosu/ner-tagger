### From NER/BetaTesting

args=("$@")
train=${args[0]} #as a .pp file
test=${args[1]} #as a .pp file
beta=${args[2]} #Whatever Unique Name you want to give to this beta test

echo Getting features
echo in training set

python ../AddingFeatures.py $train domainPlaceHolder ../Gazetteers/GEOall.txt ../Gazetteers/GEOFs.txt ../Gazetteers/GEOLs.txt ../Gazetteers/GEOMWEs.txt ../Gazetteers/GEOs.txt ../Gazetteers/GEOUs.txt ../Gazetteers/PRSall.txt ../Gazetteers/PRSFs.txt ../Gazetteers/PRSLs.txt ../Gazetteers/PRSMWEs.txt ../Gazetteers/PRSs.txt ../Gazetteers/PRSUs.txt ../Gazetteers/UNKall.txt ../Gazetteers/UNKFs.txt ../Gazetteers/UNKLs.txt ../Gazetteers/UNKMWEs.txt ../Gazetteers/UNKs.txt ../Gazetteers/UNKUs.txt > train$beta.ftrs

echo in test set
python ../AddingFeatures.py $test domainPlaceHolder ../Gazetteers/GEOall.txt ../Gazetteers/GEOFs.txt ../Gazetteers/GEOLs.txt ../Gazetteers/GEOMWEs.txt ../Gazetteers/GEOs.txt ../Gazetteers/GEOUs.txt ../Gazetteers/PRSall.txt ../Gazetteers/PRSFs.txt ../Gazetteers/PRSLs.txt ../Gazetteers/PRSMWEs.txt ../Gazetteers/PRSs.txt ../Gazetteers/PRSUs.txt ../Gazetteers/UNKall.txt ../Gazetteers/UNKFs.txt ../Gazetteers/UNKLs.txt ../Gazetteers/UNKMWEs.txt ../Gazetteers/UNKs.txt ../Gazetteers/UNKUs.txt > test$beta.ftrs

echo Training and tagging with CRF model
../crfsuite.prog learn -a pa -m crf$beta.cls train$beta.ftrs
../crfsuite.prog tag -m crf$beta.cls test$beta.ftrs > pred$beta.txt

echo Generating predictions
python ../GenPredTest.py test$beta.ftrs pred$beta.txt > pred$beta.txt2
mv pred$beta.txt2 pred$beta.txt

echo Calculating Accuracy
python ../scorerLCcomplete.py pred$beta.txt train$beta.ftrs -Complete > Results/results$beta.csv
echo Khalass




