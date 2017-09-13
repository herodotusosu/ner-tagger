### From NER/BetaTesting

args=("$@")
beta=${args[0]} #Whatever Unique Name you want to give to this beta test

./BetaTesting.sh GWOvidTrain.pp PlinyTest.pp testPliny$beta
./BetaTesting.sh GWPlinyTrain.pp OvidTest.pp testOvid$beta
./BetaTesting.sh GWPlinyOvidTrain.pp GWTest.pp testGW$beta
