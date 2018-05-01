### From NER/BetaTesting

### Run this 3 separate times, once for each train/test split
### Or just combine the three runs with another bash script

args=("$@")
train=${args[0]} #as a .pp file
test=${args[1]} #as a .pp file
sentsAtATime=${args[2]}
origbeta=${args[3]} #Whatever Unique Name you want to give to this beta test

testLength=$(sed '/^\s*$/d' $test | wc -l)
trainLength=$(sed '/^\s*$/d' $train | wc -l)
beta=$origbeta$testLength
echo FULL TEST LENGTH IS $testLength

echo GETTING RESULTS OF INITIAL FULLY SUPERVISED MODEL
# This file outputs various files after execution. These are, train$beta.ftrs,
# test$beta.ftrs, pred$beta.ftrs, Results/results$beta.csv. The train and test
# files are augmented original files with more features. The prediction file has
# the predictions, predictably, in the CRFSuite format.
./BetaTesting.sh $train $test $beta
cp train$beta.ftrs origTrain.ftrs

echo GETTING CAPPED TEST UNKS AND PRINTING NUMBER OF CAPPED TEST UNKS WHICH WE WILL THEN LOOK FOR IN THE UNANNOTATED CORPUS
# This file outputs two files, trainWords.dat, and testUNKs.dat. trainWords.dat
# is a pickled dict that represents a word count dictionary for the training
# file. testUNKs is a dictionary where testUNKs[k], represents unknown words of
# priority k. The result is another dict of word counts for the given priority.
python gettingTestUNKs.py train$beta.ftrs test$beta.ftrs

echo HARVESTING FROM TEST SET ONLY SENTS CONTAINING CAPPED TEST UNKS
python harvestSentsWithTestUNKsCHEAT.py test$beta.ftrs testUNKs.dat trainWords.dat -normal > LeftOver.ftrs
python harvestSentsWithTestUNKsCHEAT.py test$beta.ftrs testUNKs.dat trainWords.dat -rest LeftOver.ftrs > unImportantTestSet.ftrs
unImportantLength=$(sed '/^\s*$/d' unImportantTestSet.ftrs | wc -l)
lLength=$(sed '/^\s*$/d' LeftOver.ftrs | wc -l)
echo LIMITED LENGTH IS $lLength

### pickles out a sentID2origUNKcounts.dat file which is dictionary where the sentIDs of the sentences will be updated constantly to match their position in LeftOverUnannotated.txt as it evolves each iteration, still allowing us to access the count for how many words were originally UNK before recursive training.

cat LeftOver.ftrs unImportantTestSet.ftrs > test$beta.ftrs

echo TAGGING TEST SET WITHOUT EVALUATING IT IN ORDER TO SEE WHICH TEST UNKS WE ARE THE MOST UNCERTAIN ABOUT
../crfsuite.prog tag -m crf$beta.cls -p -i -r test$beta.ftrs > predStats$beta.txt
	
echo TAGGING LEFT OVER SENTS
../crfsuite.prog tag -m crf$beta.cls -p -i -r LeftOver.ftrs > predLeftOver$beta.txt

echo REFORMATING TAGGED OUTPUT FOR EASIER DATA MINING
python ../GenPredTestSentStatsInformCHEAT.py LeftOver.ftrs sentID2origUNKcounts.dat predLeftOver$beta.txt predStats$beta.txt testUNKs.dat test$beta.ftrs train$beta.ftrs False 7 #This last variable represents the most allowable number of UNK words in a sentence
	### Pickles out sentID2tUNK2listStats.dat
	# rm predUnannotated$beta.txt
	# rm predStats$beta.txt

echo IDENTIFYING SENTS FROM TEST SET WHICH ARE THE MOST INFORMATIVE
	### Takes in sentID2wordID2margProb.dat &&& sentID2sentProb2sents.dat &&& $TrainLength &&& 'run'
		# identifies all sents where there is exactly one TestUNK and no other generalUNKs
			# ranks these by log(SP)/len(sent)
				# 0 probabilities get SP of -1000000
		# pulls all sents in order of there normalizedSP ranking for unsupervised training until reach recursivelyAddedPortion% of the already existing training data
			# writes out these recursivelyAddedPortion% sents to trainNew.ftrs
			# prints new LeftOverUnannotated.txt
python getInformativeSentsCHEAT.py sentID2tUNK2listStats.dat LeftOver.ftrs $sentsAtATime > Results/orderedTestSents.ftrs 
orderedLength=$(sed '/^\s*$/d' Results/orderedTestSents.ftrs | wc -l)
cp Results/orderedTestSents.ftrs newTest.ftrs

echo ADDING $sentsAtATime SENTS AT A TIME TO TRAINING DATA FROM TEST SET AND PLOTTING INCREASE IN ACCURACY

rm added2train.ftrs
touch added2train.ftrs

# colon returns 0, which is de facto like true
while :
do
  echo BETA is $beta
	python getBestSents.py newTest.ftrs $sentsAtATime -train > delete.txt
  python getBestSentsAnnotation.py delete.txt
  break

	cat added2train.ftrs delete.txt > added2train.ftrs_tmp
	mv added2train.ftrs_tmp added2train.ftrs
	python getBestSents.py newTest.ftrs $sentsAtATime -leftOver > newTest.ftrs_tmp
	mv newTest.ftrs_tmp newTest.ftrs

	delLength=$(sed '/^\s*$/d' delete.txt | wc -l)
  if [ $delLength -eq 0 ]; then
    echo WE ARE DONE. NOTHING LEFT TO DELETE.
    break
  fi

	echo REMOVING SENTS FROM TEST FILE
  # delete.txt consists of sentences (words with features on each line) separated
  # by a newline which are to be removed from test$beta.ftrs.
	python removeExtractedTestSents.py test$beta.ftrs delete.txt > test$beta.ftrs_tmp
	mv test$beta.ftrs_tmp test$beta.ftrs
	rm delete.txt
	testLength=$(sed '/^\s*$/d' test$beta.ftrs | wc -l)

	echo NEW TEST LENGTH IS $testLength

	### TAKE TEST UNKS AND ADDED2TRAIN TO FIND OUT PROP
	### PRINTS TUNKS IN ADDED2TRAIN / LEN(TUNKS)
	proportion=$(python getPropTUNKsInAddedSents.py testUNKs.dat added2train.ftrs)
	echo PROPORTION OF TOTAL TUNKS IN ADDEDSENTS IS $proportion

	echo UPDATING TRAINING SET
	newBeta=$origbeta$testLength

	python augmentAddedSents4train.py origTrain.ftrs added2train.ftrs $proportion > train$newBeta.ftrs	
	rm train$beta.ftrs
	rm crf$beta.cls
	rm pred$beta.txt
	mv test$beta.ftrs test$newBeta.ftrs
	beta=$newBeta

	echo TRAINING NEW MODEL
	../crfsuite.prog learn -a pa -m crf$beta.cls train$beta.ftrs

	echo TESTING NEW MODEL
	../crfsuite.prog tag -m crf$beta.cls test$beta.ftrs > pred$beta.txt

	echo GENERATING PREDICTIONS
	python ../GenPredTest.py test$beta.ftrs pred$beta.txt > pred$beta.txt_tmp
	mv pred$beta.txt_tmp pred$beta.txt

	echo CALCULATING ACCURACY
	python ../scorerLCcomplete.py pred$beta.txt train$beta.ftrs -Complete > Results/results$beta.csv
done
