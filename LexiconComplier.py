import nltk
from nltk.corpus import wordnet
nltk.download('wordnet')
from english_dictionary.scripts.read_pickle import get_dict
import csv
class LexiconCompiler:
    dictionary = get_dict()



    def compile(self):
        all_words = set()  # Using a set to avoid duplicates
        for synset in wordnet.all_synsets():
            for lemma in synset.lemmas():
                all_words.add(lemma.name())
        all_words.add(self.dictionary.keys())

        words_list = list(all_words)

        with open('english_dictionary.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            for word in words_list:
                writer.writerow([word])


