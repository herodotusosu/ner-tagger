args=("$@")
folder=${args[0]}
file=${args[1]}

cd ../Results

python ../AddingFeatures.py ../Preprocessing/Preprocessed/$folder/$file.txt domainPlaceHolder lemmaDictionaryPlaceHolder lexTriggerPlaceHolder1 LTPH2 LTPH3 > $file.ftrs

../crfsuite.prog tag -m ../HDT.cls $file.ftrs > predictions.txt

python ../GenPredTest.py $file.ftrs predictions.txt > predictions2.txt

python ../genNElist.py predictions2.txt > NElist.txt

mv predictions2.txt predictions.txt

