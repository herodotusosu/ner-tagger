import argparse
import cPickle as pickle
import collections


parser = argparse.ArgumentParser()
parser.add_argument('train', help='The trained file with added features.')
parser.add_argument('test', help='The test file with added features.')
args = parser.parse_args()

words = collections.defaultdict(int)
priority2testUNKs = {}
highPriorityUNKs = collections.defaultdict(int)
lowPriorityUNKs = collections.defaultdict(int)

# Word count for train.
with open(args.train, 'r') as train:
    for line in train:
        line = line.strip()
        cols = line.split()
        if len(cols) > 0:
            word = cols[1]
            words[word] += 1

with open(args.test, 'r') as test:
    for line in test:
        line = line.strip()
        cols = line.split()

        if len(cols) > 0:
            word = cols[1]
            if word not in words:
                # If this is a word we have not seen in training and is capitalized
                # this it is of interest. If it is not a proper noun that is of
                # high priority, since it a non NER that is capitalized and can cause
                # confusion. Similarly, a lower priority would be a capitalized word
                # that is a proper noun.
                if word[0].isupper() and 'NotAProperNoun' not in line:
                    highPriorityUNKs[word.lower()] += 1
                if word[0].isupper() and 'NotAProperNoun' in line:
                    lowPriorityUNKs[word.lower()] += 1

priority2testUNKs[1] = highPriorityUNKs
priority2testUNKs[2] = lowPriorityUNKs

with open("testUNKs.dat",'w') as of:
        pickle.dump(priority2testUNKs,of)

with open("trainWords.dat",'w') as of:
        pickle.dump(words,of)
