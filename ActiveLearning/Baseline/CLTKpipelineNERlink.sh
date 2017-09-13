### From NER/BetaTesting

args=("$@")
beta=${args[0]} #Whatever Unique Name you want to give to this beta test

./CLTKpipelineNER.sh PlinyTest.pp testPliny$beta
./CLTKpipelineNER.sh OvidTest.pp testOvid$beta
./CLTKpipelineNER.sh GWTest.pp testGW$beta
