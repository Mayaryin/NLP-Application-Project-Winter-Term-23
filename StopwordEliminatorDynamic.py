from collections import Counter
class DynamicStopwordEliminator:

    #defines the most frequent words as stopwords

    def __init__(self, token_list):
        self.stopwords = self.deriveStopwords(token_list)

    def deriveStopwords(self, token_list):
        word_frequency = Counter(token_list)
        threshold = len(token_list) * 0.001
        return [word for word, freq in word_frequency.items() if freq > threshold]

    def eliminateStopwords(self, text):
        return [word for word in text if word.lower() not in self.stopWords]