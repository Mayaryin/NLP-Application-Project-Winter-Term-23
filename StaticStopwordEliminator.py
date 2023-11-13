import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
class StaticStopwordEliminator:

    stopWords = set(stopwords.words('english'))

    #expects a tokenized text, that is, a list of words
    #returns a list of words
    def eliminateStopwords(self, text):
        return [word for word in text if word.lower() not in self.stopWords]
