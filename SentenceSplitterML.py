from conllu import parse
import numpy as np
import re
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

class SentenceSplitterML:

    #feature codes:
    #no char present = 0
    #upper case char = 1
    #lower case char = 2
    #special character wihtout whitespace and period = 3
    #whitespace = 4
    #number = 5
    #punctuation = 6

    punctuationMarks = ['.', '?', '!', ':', ';']
    model = LogisticRegression()

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

    #expects a list of sentences!
    def extractLabels(self, sentenceList):
        labels = []
        for sentenceIndex, sentence in enumerate(sentenceList):
            for withinSentenceIndex, char in enumerate(sentence):
                if char in self.punctuationMarks:
                    labels.append(self.isAtEndOfSentence(sentence, withinSentenceIndex))
        return labels

    def extractFeatures(self, text):
        features = []
        for index, char in enumerate(text):
            if char in self.punctuationMarks:
                features.append(self.compileFeatureVector(text, index))
        return features

    def isAtEndOfSentence(self, sentence, index):
        if index == len(sentence) -1:
            return True
        return False

    def compileFeatureVector(self, text, i):
        featureVector = [0, 0, 0, 0, 0, 0,0,0,0,0]
        j = i - 5  # index running on the sentence
        k = 0  # index running on the feature vector
        while j <= i + 5:  # fill an array with size i-3 to i+3
            if (j == i): j += 1  # jump over the character itself
            if j < 0: featureVector[k] = 0
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
        trainCorpus = self.importData(path)
        trainCorpusString = self.unsplit(trainCorpus)
        features = self.extractFeatures(trainCorpusString)
        labels = self.extractLabels(trainCorpus)
        self.model.fit(features, labels)

    def test(self, path):
        testCorpus = self.importData(path)
        testCorpusString = self.unsplit(testCorpus)
        testFeatures = self.extractFeatures(testCorpusString)
        testLabels = self.extractLabels(testCorpus)
        predictedLabels = self.model.predict(testFeatures)
        accuracy = accuracy_score(testLabels, predictedLabels)
        print("Accuracy:", accuracy)
        print(classification_report(testLabels, predictedLabels))

    def split(self, inputText):
        sentences = []
        start = 0
        for i, char in enumerate(inputText):
            if char in self.punctuationMarks:
                features = self.compileFeatureVector(inputText, i)
                is_boundary = self.model.predict([features])[0]

                if is_boundary:
                    sentence = inputText[start:i + 1].strip()
                    sentences.append(sentence)
                    start = i + 1
        if start < len(inputText):
            sentences.append(inputText[start:].strip())

        return sentences






