#!/usr/bin/env bash

#
# This is the main, "main" script... I think. TBD, just a placeholder for now.
#

./processCorpora.sh /home/corpora/original/latin/canonical-latinLit/data/ Preprocessed/

cd Preprocessed
../mainPOSTagger.sh

echo Done POS Tagging all requested documents
echo Filtering Tags by Morphological Analyzer
echo

../mainFinishPPwithWWW.sh

echo Done filtering POS tags through Morphological Analyzer
echo

echo "The Requested Texts have been Preprocessed! You can find them in the direcory ~/NER/Preprocessing/Preprocessed/.

Please be sure to move said texts to another directory so that the Preprocessed subdirectory is empty the next time you choose to preprocess something.

You now have 2 choices:

1) send the preprocessed files off to get annotated for named entities

When annotation is finished and you are ready to test accuracy, place the annotated file you wish to test (This file will be referred to as FILE) in the Results folder and run the following sequence of commands from the Preprocessing directory:

../getResults.sh FILE
	(DO NOT PUT THE .TXT SUFFIX ON FILE IN THE ABOVE COMMAND)
	
This will result in multiple files being created, one with a .ftrs suffix showing what features were generated, one named predictions.txt which shows what labels were predicted vs. the actual NER labels, and one named results.csv which reports final accuracy statistics.

2) run the NER tagger on the preprocessed files without annotating (this means your only judgment of quality will be eyeballing the results)

To do (2), run the following sequence of commands from the Preprocessing directory for each file you've just preprocessed (FOLDER refers to the folder in the Preprocessed directory where the text you want to label is located and FILE refers to the actual text itself, though don't include the .txt suffix on FILE):

../getNEs.sh FOLDER FILE

This will yield a .ftrs file showing what features were used, a predictions.txt file showing which labels were predicted for each word, and an NElist.txt file showing which NE's were identified in the text.

"
