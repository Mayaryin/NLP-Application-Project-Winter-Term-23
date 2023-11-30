from nltk.tokenize.stanford import StanfordTokenizer
from nltk.tokenize.treebank import TreebankWordTokenizer
from english_dictionary.scripts.read_pickle import get_dict
import nltk
nltk.download('wordnet')
from nltk.corpus import wordnet
import string
import csv
class Normalizer():

    #the normalizer works on tokenized text
    #applies lowercasing if enabled
    #removes all tokens that are punctuation marks
    #removes clitics if enabled
    #non-standard words will be identified by looking up each token in an english dictionary

    #https://en.wikibooks.org/wiki/Algorithm_Implementation/Strings/Levenshtein_distance#Python

    def __init__(self, file_path):
        self.file_path = file_path
        self.dictionary = self.read_csv()
        self.clitics_dictionary = {
            "'ll": "will",
            "'d": "would/had",
            "'s": "is/has",
            "'re": "are",
            "'ve": "have",
            "'m": "am",
            "n't": "not"
    }

    def read_csv(self):
        with open(self.file_path, 'r') as file:
            reader = csv.reader(file)
            data_list = [row[0] for row in reader]
        return data_list


    def isStandardWord(self, token):
        if not bool(wordnet.lemmas(token)):
            return self.dictionary.get(token, "not found") != "not found" #true if word is found
        return True

    def returnClosestWord(self, token):
        distance = 1000
        closestWord = "xxxxxx"
        for word in self.dictionary:
            currentDistance = self.levenshtein(token, word)
            if currentDistance < distance:
                distance = currentDistance
                closestWord = word
                #print(closestWord)
        return closestWord

    def levenshtein(self, word1, word2):
        if len(word1) < len(word2):
            return self.levenshtein(word2, word1)

        # len(word1) >= len(word2)
        if len(word2) == 0:
            return len(word1)

        previous_row = range(len(word2) + 1)
        for i, c1 in enumerate(word1):
            current_row = [i + 1]
            for j, c2 in enumerate(word2):
                insertions = previous_row[
                                 j + 1] + 1  # j+1 instead of j since previous_row and current_row are one character longer
                deletions = current_row[j] + 1  # than word2
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row

        return previous_row[-1]

    def normalize(self, token_list, lowercaseEnabled, expansionEnabled):

        #convert to lowercase if enabled
        if lowercaseEnabled:
           token_list = [token.lower() for token in token_list]

        #remove all punctuation tokens
        token_list = [token for token in token_list if token not in string.punctuation]

        #expand clitics if enabled
        if expansionEnabled:
            token_list = [self.clitics_dictionary.get(token, token) for token in token_list]

        #replace misspelled words by their most similar one from the dictionary
        normalized_tokens = []
        for token in token_list:
            if not token in self.dictionary:
                print(token + " is not a standard word")
                substitution = self.returnClosestWord(token)
                normalized_tokens.append(substitution)
                print(substitution + " is the conversion")
            else: normalized_tokens.append(token)


        return normalized_tokens
