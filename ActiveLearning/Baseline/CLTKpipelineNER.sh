### From NER/BetaTesting

args=("$@")
test=${args[0]} #as a .pp file
beta=${args[1]} #Whatever Unique Name you want to give to this beta test
train=${args[2]}

echo REFORMATTING TEXT AND RUNNING BASELINE CLTK
cat $test | python reformat4CLTK.py | python3 runCLTKner.py > pred$beta.txt

echo GENERATING PREDICTIONS CALCULATING ACCURACY
python scorerCLTK.py $test pred$beta.txt $train > Results/results$beta.csv none

echo CALCULATING ACCURACY





# echo Calculating Accuracy
# python ../scorerLCcomplete.py pred$beta.txt train$beta.ftrs -Complete > Results/results$beta.csv
# echo Khalass




