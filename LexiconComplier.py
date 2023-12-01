import nltk
from nltk.corpus import wordnet
nltk.download('wordnet')
from english_dictionary.scripts.read_pickle import get_dict
import csv
class LexiconCompiler:

    #compiles all words from nltk wordnet and https://pypi.org/project/english-dictionary/ into one csv
    #all words are lowercase
    #all underscores are removed

    dictionary = get_dict()

    def compile(self):
        all_words = set()  # Using a set to avoid duplicates
        for synset in wordnet.all_synsets():
            for lemma in synset.lemmas():
                all_words.add(lemma.name())
        for key in self.dictionary.keys():
            all_words.add(key)

        with open('abbr.csv', 'r') as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                all_words.add(row[0])

        words_list = list(all_words)

        words_list = [word.replace("_", " ") for word in words_list]
        lowercase_list = [item.lower() for item in words_list]

        with open('english_lexicon.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            for word in lowercase_list:
                writer.writerow([word])
