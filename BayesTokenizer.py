import nltk
nltk.download('brown')
from nltk.corpus import brown
from nltk.tokenize import TreebankWordTokenizer
import random

class BayesTokenizer:
    documents = [(list(brown.words(fileid)), category)
                 for category in brown.categories()
                 for fileid in brown.fileids(category)]
    categories = brown.categories()
    fileIdAdventure = brown.fileids("adventure")
    wordsAdventure = list(brown.words(fileIdAdventure))

    def printDocuments(self):
        print("brown words: ", self.wordsAdventure)

    def splitCorpus(self):
        file_ids = list(brown.fileids())
        random.shuffle(file_ids)

        numberOfFiles = len(file_ids)
        train_split = int(numberOfFiles * 0.7) #70% of the corpus is used for training, 15% each for testing and evaluation
        test_split = int(numberOfFiles * 0.85)

        train_files = file_ids[:train_split]
        test_files = file_ids[train_split:test_split]
        eval_files = file_ids[test_split:]

        trainingCorpus = [word for fileid in train_files for word in brown.words(fileid)]
        testCorpus = [word for fileid in test_files for word in brown.words(fileid)]
        evaluationCorpus = [word for fileid in eval_files for word in brown.words(fileid)]

        return trainingCorpus, testCorpus, evaluationCorpus

    def tokenize(self, corpus):
        tokenizer = TreebankWordTokenizer
        return tokenizer.tokenize(corpus)




