import numpy as np
class BinaryNaiveBayesClassifier:
    def __init__(self):
        self.classes = [False,True]
        self.number_of_positive_samples = 0
        self.number_of_negative_samples = 0
        self.prior_probability_positive = 0
        self.prior_probability_negative = 0
        self.class_conditionals_positive = []
        self.class_conditionals_negative = []

    def countSamplesInClasses(self, labels):
        self.number_of_positive_samples = sum(labels) #positive = 1, negative = 0, sum gives the count of positive labels
        self.number_of_negative_samples = (len(labels) - sum(labels))

    def calculatePriorProbabilies(self,labels):
        self.prior_probability_positive = self.number_of_positive_samples/len(labels)
        self.prior_probability_negative = self.number_of_negative_samples/len(labels)

    def computeClassConditionals(self, features, labels):
        features = np.array(features)
        labels = np.array(labels)
        positive_class = features[labels == True]
        negative_class = features[labels == False]
        number_of_features = len(features[0])
        self.class_conditionals_positive = [{} for _ in range(number_of_features)]
        self.class_conditionals_negative = [{} for _ in range(number_of_features)]

        #Count the occurences of each feature value in each class
        for vector in positive_class:
            for feature_type, value in enumerate(vector):
                self.class_conditionals_positive[feature_type][value] = self.class_conditionals_positive[feature_type].get(value, 0) + 1

        for vector in negative_class:
            for feature_type, value in enumerate(vector):
                self.class_conditionals_negative[feature_type][value] = self.class_conditionals_positive[feature_type].get(value, 0) + 1

        #print("positive counts: ", self.class_conditionals_positive)
        #print("negative counts: ", self.class_conditionals_negative)

        #convert counts to probabilites by dividing them by the total number of samples in the class
        for dictionary in self.class_conditionals_positive:
            for value in dictionary:
                dictionary[value] /= self.number_of_positive_samples

        for dictionary in self.class_conditionals_negative:
            for value in dictionary:
                dictionary[value] /= self.number_of_negative_samples

    def computePosterior(self, feature_vector, classType):
        if classType == True:
            conditionals = self.class_conditionals_positive
            prior = np.log(self.prior_probability_positive) #apply logarithm for avoiding underflow
        else:
            conditionals = self.class_conditionals_negative
            prior = np.log(self.prior_probability_negative)

        for feature_type, value in enumerate(feature_vector): #sum the log of the probablities
            prior += np.log(conditionals[feature_type].get(value, 1e-10)) #avoid log of zero (Laplace)

        posterior = prior

        return posterior

    def fit(self, features, labels):
        self.countSamplesInClasses(labels)
        self.calculatePriorProbabilies(labels)
        self.computeClassConditionals(features, labels)
        #print("positive probs: ", self.class_conditionals_positive)
        #print("negative probs: ", self.class_conditionals_negative)

    def predict(self, features):
        predictionResults = []
        for featureVector in features:
            posteriors = []
            for classType in self.classes:
                posteriors.append(self.computePosterior(featureVector, classType))
            if posteriors[0] >= posteriors[1]:
                predictionResults.append(False)
            else: predictionResults.append(True)
        return predictionResults


