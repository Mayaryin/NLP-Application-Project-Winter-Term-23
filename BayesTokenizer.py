import nltk
from nltk.corpus import brown
from nltk.tokenize import TreebankWordTokenizer
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures
from conllu import parse
import random
import re
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from CustomizedTreebankTokenizer import CustomizedTreebankTokenizer
from sklearn.naive_bayes import GaussianNB

class BayesTokenizer:

    # feature codes:
    # no char present = 0
    # upper case char = 1
    # lower case char = 2
    # special character wihtout whitespace and period = 3
    # whitespace = 4
    # number = 5
    # punctuation = 6

    ambiguous_characters = ['.', ',', '-', '—', "'", '/', ':', ';', '"', '(', ')', '!', '?', '[', ']', '@']
    #model = LogisticRegression()
    model = GaussianNB()
    def importData(self, path):
        with open(path, 'r') as file:
            corpus = file.read()
        parsedData = parse(corpus)
        sentences = []
        for sentence in parsedData:
            if 'text' in sentence.metadata:
                sentences.append(sentence.metadata['text'])
        return sentences

    def unsplit(self, sentenceList):
        return " ".join(sentenceList)

    def tokenizeData(self, text):
        #return TreebankWordTokenizer().tokenize(text)
        return CustomizedTreebankTokenizer().tokenize(text, True, False, False) #tokenize without replacing urls and email with placeholders


    def isAtEndOfToken(self, token, index):
        if index == len(token) -1:
            return True
        return False

    def extractFeatures(self, text):
        features = []
        for index, char in enumerate(text):
            if char in self.ambiguous_characters:
                features.append(self.compileFeatureVector(text, index))
        print(len(features))
        return features
    def extractLabels(self, token_list):
        labels = []
        for index, token in enumerate(token_list):
            for withinSentenceIndex, char in enumerate(token):
                if char in self.ambiguous_characters:
                    labels.append(self.isAtEndOfToken(token, withinSentenceIndex))
        print(len(labels))
        return labels

    def compileFeatureVector(self, text, i):
        featureVector = [0, 0, 0, 0]
        j = i - 2  # index running on the sentence
        k = 0  # index running on the feature vector
        while j <= i + 2:  # fill an array with size i-3 to i+3
            if (j == i): j += 1  # jump over the character itself
            if j < 0: featureVector[k] = 0 #if there is no char at the position, assign 0
            if j >= len(text) - 1: featureVector[k] = 0
            if j >= 0 and j < (len(text) - 1):
                featureVector[k] = self.determineCharType(text[j])
            j += 1
            k += 1
        return featureVector

    def determineCharType(self, char):
        if re.match(r"[A-Z]", char): return 1
        if re.match(r"[a-z]", char): return 2
        if re.match(r"[^A-Za-z0-9\s\.]", char): return 3
        if re.match(r"\s", char): return 4
        if re.match(r"[0-9]", char): return 5
        if re.match(r"[\.]", char): return 6

    def train(self, path):
        trainCorpus = self.importData(path) #list of sentences
        trainCorpusString = self.unsplit(trainCorpus) #all sentences merged in one string
        trainCorpusTokens = self.tokenizeData(trainCorpusString) #tokenized text
        features = self.extractFeatures(trainCorpusString) #extract features on character level
        labels = self.extractLabels(trainCorpusTokens) #extract whether a char is at the end of a token
        self.model.fit(features, labels)

    def test(self, path):
        testCorpus = self.importData(path)
        testCorpusString = self.unsplit(testCorpus)
        testCorpusTokens = self.tokenizeData(testCorpusString)
        testFeatures = self.extractFeatures(testCorpusString)
        testLabels = self.extractLabels(testCorpusTokens)
        predictedLabels = self.model.predict(testFeatures)
        accuracy = accuracy_score(testLabels, predictedLabels)
        print("Accuracy:", accuracy)
        print(classification_report(testLabels, predictedLabels))

    def tokenize(self, inputText):
        tokens = []
        start = 0
        for i, char in enumerate(inputText):
            if char.isspace() or char in self.ambiguous_characters:
                if char in self.ambiguous_characters:
                    features = self.compileFeatureVector(inputText, i)
                    is_boundary = self.model.predict([features])[0]
                    print(features, is_boundary)
                else:
                    is_boundary = True

                if is_boundary:
                    token = inputText[start:i + 1].strip()
                    if token:  # Check to avoid adding empty strings
                        tokens.append(token)
                    start = i + 1

        # Handle any remaining text after the last boundary
        if start < len(inputText):
            remaining_token = inputText[start:].strip()
            if remaining_token:  # Check to avoid adding empty strings
                tokens.append(remaining_token)

        return tokens




