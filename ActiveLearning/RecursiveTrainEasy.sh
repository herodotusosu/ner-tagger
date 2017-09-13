### From NER/BetaTesting

### Run this 3 separate times, once for each train/test split
### Or just combine the three runs with another bash script

args=("$@")
train=${args[0]} #as a .pp file
TrainLength=$(cat $train | sed '/^\s*$/d' | wc -l)
test=${args[1]} #as a .pp file
recursivelyAddedPortion=${args[2]}
origbeta=${args[3]} #Whatever Unique Name you want to give to this beta test
beta=$origbeta$TrainLength

echo GETTING RESULTS OF INITIAL FULLY SUPERVISED MODEL
./BetaTesting.sh $train $test $beta

echo GETTING CAPPED TEST UNKS
python gettingTestUNKs.py train$beta.ftrs test$beta.ftrs # pickle out two models: trainWords[word]=freqInTraining &&& testUNKs[priorityLevel:1=highest,2=next,etc.][testUNK]=freqInTesting

echo GETTING UNANNOTATED CORPUS
cat ../Preprocessed/*/*.txt | python ../Preprocessing/removeDoubles.py > LeftOverUnannotated.txt # IMPORTANT - BUT MAYBE FOR FUTURE WORK!!! Consider adding step here where metadata features get added to identify author, text, editor, time period, domain/genre, etc.
echo ORIGINAL LENGTH WAS
cat LeftOverUnannotated.txt | sed '/^\s*$/d' | wc -l

echo LIMITING UNANNOTATED CORPUS TO ONLY SENTS WITHOUT UNKS
python harvestSentsEasy.py LeftOverUnannotated.txt testUNKs.dat trainWords.dat > LeftOverUnannotated2.txt
mv LeftOverUnannotated2.txt LeftOverUnannotated.txt
echo LIMITED LENGTH IS
cat LeftOverUnannotated.txt | sed '/^\s*$/d' | wc -l
### pickles out a sentID2origUNKcounts.dat file which is dictionary where the sentIDs of the sentences will be updated constantly to match their position in LeftOverUnannotated.txt as it evolves each iteration, still allowing us to access the count for how many words were originally UNK before recursive training.

echo GETTING FEATURES FOR NEWLY LIMITED UNANNOTATED CORPUS
python ../AddingFeatures.py LeftOverUnannotated.txt domainPlaceHolder ../Gazetteers/GEOall.txt ../Gazetteers/GEOFs.txt ../Gazetteers/GEOLs.txt ../Gazetteers/GEOMWEs.txt ../Gazetteers/GEOs.txt ../Gazetteers/GEOUs.txt ../Gazetteers/PRSall.txt ../Gazetteers/PRSFs.txt ../Gazetteers/PRSLs.txt ../Gazetteers/PRSMWEs.txt ../Gazetteers/PRSs.txt ../Gazetteers/PRSUs.txt ../Gazetteers/UNKall.txt ../Gazetteers/UNKFs.txt ../Gazetteers/UNKLs.txt ../Gazetteers/UNKMWEs.txt ../Gazetteers/UNKs.txt ../Gazetteers/UNKUs.txt w2v/sims.txt w2v/simsLemmedSmall.txt words.dat > LeftOverUnannotated.ftrs
rm LeftOverUnannotated.txt
#cp LeftOverUnannotated.ftrs origLeftOverUnannotated.ftrs

echo BEGINNING RECURSIVE INCLUSION OF ADDITIONAL TRAINING DATA
# We start the while loop with the following files:
	# $train
		# just supervised
		# This will recursively update with unsup'd additions
	# $test
		# just supervised testing
	# LeftOverUnannotated.txt
		# Unannotated corpus eligible for semisupervised training
		# This recursively shrinks as parts move to train
origTrainLength=$TrainLength
newlyUnsupervisedLength='1'

while [ $newlyUnsupervisedLength -ne 0 ]
do
	LeftOverUnannotedCorpusLength=$(cat LeftOverUnannotated.ftrs | sed '/^\s*$/d' | wc -l)
	echo "SIZE OF REMAINING UNANNOTATED TEXT WHICH IS NOT BEING USED FOR TRAINING", $LeftOverUnannotedCorpusLength 
	echo "MINING UNANNOTATED TEXT FOR EASILY TAGGABLE SENTENCES"
	
	echo TAGGING TEST SET WITHOUT EVALUATING IT FOR NO APPARENT REASON
	../crfsuite.prog tag -m crf$beta.cls -p -i -r test$beta.ftrs > predStats$beta.txt
	
	echo TAGGING LEFT OVER UNANNOTATED DATA
	../crfsuite.prog tag -m crf$beta.cls -p -i -r LeftOverUnannotated.ftrs > predUnannotated$beta.txt
	
	echo REFORMATING TAGGED OUTPUT FOR EASIER DATA MINING
	python ../GenPredTestSentStats.py LeftOverUnannotated.ftrs sentID2origUNKcounts.dat predUnannotated$beta.txt predStats$beta.txt testUNKs.dat test$beta.ftrs train$beta.ftrs True
	### Pickles out sentID2tUNK2listStats.dat
	rm predUnannotated$beta.txt
	rm predStats$beta.txt
	
	echo IDENTIFYING NEWLY TAGGED SENTS WHICH WE ARE THE MOST CONFIDENT IN
	### Takes in sentID2wordID2margProb.dat &&& sentID2sentProb2sents.dat &&& $TrainLength &&& 'run'
		# identifies all sents where there is exactly one TestUNK and no other generalUNKs
			# ranks these by log(SP)/len(sent)
				# 0 probabilities get SP of -1000000
		# pulls all sents in order of there normalizedSP ranking for unsupervised training until reach recursivelyAddedPortion% of the already existing training data
			# writes out these recursivelyAddedPortion% sents to trainNew.ftrs
			# prints new LeftOverUnannotated.txt

	python getEasiestSents.py sentID2tUNK2listStats.dat LeftOverUnannotated.ftrs $TrainLength $recursivelyAddedPortion sentID2origUNKcounts.dat > LeftOverUnannotated2.ftrs
	### Writes out trainNew.ftrs, pickles out updated sentID2origUNKcounts.dat, prints out LeftOverUnannotated2.ftrs
	mv LeftOverUnannotated2.ftrs LeftOverUnannotated.ftrs
	mv sentID2origUNKcounts2.dat sentID2origUNKcounts.dat
	rm sentID2tUNK2listStats.dat
	
	LeftOverUnannotedCorpusLength=$(cat LeftOverUnannotated.ftrs | sed '/^\s*$/d' | wc -l)
	newlyUnsupervisedLength=$(cat trainNew.ftrs | sed '/^\s*$/d' | wc -l)
	TrainLength=$(($TrainLength+$newlyUnsupervisedLength))
	
	echo "WE FOUND", $newlyUnsupervisedLength, "EASILY TAGGABLE UNSUPERVISED LINES TO ADD TO THE TRAINING SET"
	
	echo "SIZE OF SUPERVISED TRAINING DATA", $origTrainLength
	num=$(($TrainLength-$origTrainLength))
	echo "SIZE OF ADDITIONAL UNSUPERVISED TRAINING DATA", $num
	echo "TOTAL SIZE OF TRAINING DATA", $TrainLength
	if [ $newlyUnsupervisedLength -ne 0 ]
	then
		echo "UPDATING TRAINING SET"
		newBeta=$origbeta$TrainLength
		cat train$beta.ftrs trainNew.ftrs > train$newBeta.ftrs
		rm train$beta.ftrs
		rm crf$beta.cls
		
		#rm trainNew.ftrs
		rm trainNew.ftrs # DeBug/trainNew$beta.ftrs
		# cp train$newBeta.ftrs DeBug/train$newbeta.ftrs
		
		rm pred$beta.txt
		mv test$beta.ftrs test$newBeta.ftrs
		beta=$newBeta
		
		echo "TRAINING NEW MODEL"
		../crfsuite.prog learn -a pa -m crf$beta.cls train$beta.ftrs
		
		echo "TESTING NEW MODEL"
		../crfsuite.prog tag -m crf$beta.cls test$beta.ftrs > pred$beta.txt
	
		echo "GENERATING PREDICTIONS"
		python ../GenPredTest.py test$beta.ftrs pred$beta.txt > pred$beta.txt2
		mv pred$beta.txt2 pred$beta.txt

		echo "CALCULATING ACCURACY"
		python ../scorerLCcomplete.py pred$beta.txt train$beta.ftrs -Complete > Results/results$beta.csv
	
	else
		echo 'KHALASS, WE COULD NOT ADD ANY MORE HIGH PROBABILITY SENTENCES TO THE TRAINING SET... THIS IS THE FINAL MODEL'
	fi	
done


