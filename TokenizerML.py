import nltk
from nltk.corpus import brown
from nltk.tokenize import TreebankWordTokenizer
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures
from conllu import parse
import random
import csv
import re
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from TokenizerRulebased import TokenizerRulebased
from sklearn.naive_bayes import GaussianNB
from BinaryNaiveBayesClassifier import BinaryNaiveBayesClassifier

class TokenizerML:

    # window feature codes:
    # no char present = 0
    # upper case char = 1
    # lower case char = 2
    # special character wihtout whitespace and period = 3
    # whitespace = 4
    # number = 5
    # punctuation = 6

    #general features:
    #taken from Daniel Jurafsky and James H. Martin, Speech and Language Processing - An Introduction to Natural Language Processing, Computational Linguistics, and Speech Recognition p.252
    #the prefix (the portion of the candidate token preceding the candidate)
    #the suffix (the portion of the candidate token following the candidate)
    #whether the prefix or suffix is an abbreviation (from a list)
    #the word preceding the candidate
    #the word following the candidate
    #whether the word preceding the candidate is an abbreviation
    # whether the word following the candidate is an abbreviation

    #features are computed for punctuation and chars that are followed by punctiation

    def __init__(self):

        self.ambiguous_characters = ['.', ',', '-', '—', "'", '/', ':', ';', '"', '(', ')', '!', '?', '[', ']', '@']
        self.logModel = LogisticRegression()
        self.bayesModel = BinaryNaiveBayesClassifier()
        self.abbreviationList = self.read_csv("abbr.csv")

    def read_csv(self, path):
        with open(path, 'r') as file:
            reader = csv.reader(file)
            data_list = [row[0] for row in reader]
        return data_list

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

    def tokenizeTrainingData(self, text):
        # tokenize without replacing urls and email with placeholders but with splitting of clitics
        return TokenizerRulebased().tokenize(text, True, False, False)

    def isAtEndOfToken(self, token, index):
        if index == len(token) -1:
            return True
        return False

    def isFollowedByPunctuation(self, text, index):
        if index + 1 < len(text):
            next_char = text[index + 1]
            return next_char in self.ambiguous_characters
        return False


    def extractFeatures(self, text, featureType):
        features = []
        for index, char in enumerate(text):
            if char in self.ambiguous_characters:
                if featureType == 1:
                    features.append(self.compileWindowFeatureVector(text, (index - 1))) # also check the char preceeding the punctuation
                    features.append(self.compileWindowFeatureVector(text, index))
                if featureType == 2:
                    features.append(self.compileGeneralFeatureVector(text, (index - 1)))  # also check the char preceeding the punctuation
                    features.append(self.compileGeneralFeatureVector(text, index))

        #print("length features: ", len(features))
        return features

    def extractLabels(self, token_list):
        labels = []
        for index, token in enumerate(token_list):
            for withinSentenceIndex, char in enumerate(token):
                if char in self.ambiguous_characters:
                    labels.append(self.isAtEndOfToken(token, (withinSentenceIndex-1))) #check the char preceeding the punctuation
                    labels.append(self.isAtEndOfToken(token, withinSentenceIndex))
        #print("length labels: ", len(labels))
        return labels

    def compileWindowFeatureVector(self, text, i):
        featureVector = [0, 0, 0, 0]
        j = i - 2  # index running on the sentence
        k = 0  # index running on the feature vector
        while j <= i + 2:  # fill an array with size i-3 to i+3
            if (j == i): j += 1  # jump over the character itself
            if j < 0: featureVector[k] = 0 #if there is no char at the position, assign 0
            if j >= len(text) - 1: featureVector[k] = 0 #if there is no char at the position, assign 0
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

    def compileGeneralFeatureVector(self, text, index):
        featureVector = []
        charItself = text[index]
        prefix = self.getPrefix(text, index)
        suffix = self.getSuffix(text, index)
        prevWord = self.getPreviousWord(text, index)
        nextWord = self.getNextWord(text, index)
        featureVector.append(charItself)
        featureVector.append(prefix)
        featureVector.append(suffix)
        featureVector.append(self.isAbbreviation(prefix))
        featureVector.append(self.isAbbreviation(suffix))
        featureVector.append(prevWord)
        featureVector.append(nextWord)
        featureVector.append(self.isAbbreviation(prevWord))
        featureVector.append(self.isAbbreviation(nextWord))
        featureVector.append(self.isCapital(nextWord))
        return featureVector

    def getPrefix(self, text, index):
        prefix = ''
        i = index - 1
        while i >= 0 and not text[i].isspace():
            prefix = text[i] + prefix
            i -= 1
        return prefix

    def getSuffix(self, text, index):
        suffix = ''
        i = index + 1
        while i < len(text) and not text[i].isspace():
            suffix += text[i]
            i += 1
        return suffix

    def getPreviousWord(self, text, index):
        # Find the start of the current word
        start = index
        while start > 0 and not text[start - 1].isspace():
            start -= 1

        # Find the start of the preceding word
        end = start
        start = end - 1
        while start > 0 and not text[start - 1].isspace():
            start -= 1

        # Extract and return the preceding word
        return text[start:end].strip()

    def getNextWord(self, text, index):
        # Find the end of the current word
        end = index
        while end < len(text) and not text[end].isspace():
            end += 1

        # Find the start of the next word
        start = end
        while start < len(text) and text[start].isspace():
            start += 1

        # Find the end of the next word
        end = start
        while end < len(text) and not text[end].isspace():
            end += 1

        # Extract and return the next word
        return text[start:end].strip()

    def isAbbreviation(self, string):
        return string in self.abbreviationList

    def isCapital(self, string):
        return string[0].isupper() if string else False


    def train(self, path, featureType):
        trainCorpus = self.importData(path) #list of sentences
        trainCorpusString = self.unsplit(trainCorpus) #all sentences merged in one string
        trainCorpusTokens = self.tokenizeTrainingData(trainCorpusString) #tokenized text
        features = self.extractFeatures(trainCorpusString, featureType) #extract features on character level
        labels = self.extractLabels(trainCorpusTokens) #extract whether a char is at the end of a token
        self.bayesModel.fit(features, labels)

    def test(self, path, featureType):
        testCorpus = self.importData(path)
        testCorpusString = self.unsplit(testCorpus)
        testCorpusTokens = self.tokenizeTrainingData(testCorpusString)
        testFeatures = self.extractFeatures(testCorpusString, featureType)
        testLabels = self.extractLabels(testCorpusTokens)
        predictedLabels = self.bayesModel.predict(testFeatures)
        accuracy = accuracy_score(testLabels, predictedLabels)
        print("Accuracy:", accuracy)
        print(classification_report(testLabels, predictedLabels))

    def tokenize(self, inputText, featureType):
        tokens = []
        start = 0
        for i, char in enumerate(inputText):
            if char.isspace() or char in self.ambiguous_characters or self.isFollowedByPunctuation(inputText, i):
                if char in self.ambiguous_characters or self.isFollowedByPunctuation(inputText, i):
                    if featureType == 1:
                        features = self.compileWindowFeatureVector(inputText, i)
                    if featureType == 2:
                        features = self.compileGeneralFeatureVector(inputText, i)
                    is_boundary = self.bayesModel.predict([features])[0]
                    #print(features, is_boundary)
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




