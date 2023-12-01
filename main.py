#!/usr/bin/env python3

# Imports

from TokenizerRulebased import TokenizerRulebased
from TokenizerML import TokenizerML
from SentenceSplitterRulebased import SentenceSplitter
from SentenceSplitterML import SentenceSplitterML
from Normalizer import Normalizer
from LexiconComplier import LexiconCompiler
from StopwordEliminatorDynamic import DynamicStopwordEliminator

import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords

def main():
    print("NLP Text Processing Pipeline")

    #LexiconCompiler().compile()

    ##Tokenizer
    ##1: window features
    #2: general features
    print("\nTOKENIZER")
    mlTokenizer = TokenizerML()
    texttest = "I split aren't in 2.3 tokens. After an abbr. you shouldn't split£."
    texttest2 = " I haven't lived in the U.S. but I'll do it. What about you?"
    print("Accuracy of Bayes Tokenizer with standard feature set:\n")
    mlTokenizer.train("UD_English-GUM/en_gum-ud-train.conllu", 2)
    mlTokenizer.test("UD_English-GUM/en_gum-ud-test.conllu", 2)
    windowTokenizer = TokenizerML()
    print("Accuracy of Bayes Tokenizer with window feature set (n=4):\n")
    windowTokenizer.train("UD_English-GUM/en_gum-ud-train.conllu", 1)
    windowTokenizer.test("UD_English-GUM/en_gum-ud-test.conllu", 1)
    print("Rulebased: \n", TokenizerRulebased().tokenize(texttest, True, False, False))
    print("Bayes with general features:\n ", mlTokenizer.tokenize(texttest2, 2))
    print("Bayes with window features:\n ", windowTokenizer.tokenize(texttest2, 1))

    ##Sentence Splitter
    print("\nSENTENCE SPLITTER")
    textForSentSplitter = "I like cats. Do you like cats, too? I hate 3.5 cats."
    mlSentenceSplitter = SentenceSplitterML()
    mlSentenceSplitter.train("UD_English-GUM/en_gum-ud-train.conllu")
    mlSentenceSplitter.test("UD_English-GUM/en_gum-ud-test.conllu")
    print("Regression: \n", mlSentenceSplitter.split(textForSentSplitter))
    tokenizedTextForSentSplitter = textForSentSplitter.split()
    print("Rulebased : \n", SentenceSplitter().split(tokenizedTextForSentSplitter))

    ##Normalizer
    print("\nNORMALIZER")
    normalizerText = "The U.S.A are large, i'm mad and made a speling mistak."
    print("Misspelled text: ", normalizerText)
    normalizer = Normalizer("english_lexicon.csv")
    tokens = TokenizerRulebased().tokenize(normalizerText, True, True, True)
    print("Normalized text: ", normalizer.normalize(tokens, True))

    ###Stopwords
    print("\nSTOPWORDS")
    sentences = TokenizerML().importData("UD_English-GUM/en_gum-ud-train.conllu")
    stopwordsText = TokenizerML().unsplit(sentences)
    tokens = TokenizerRulebased().tokenize(stopwordsText, True, True, True)

    dynStopwords = set(DynamicStopwordEliminator(tokens).deriveStopwords(tokens))
    nltkStopwords = set(stopwords.words('english'))
    # Calculate the portion of nltkStopwords contained in dynamic stopwords
    overlap = dynStopwords.intersection(nltkStopwords)
    portion = len(overlap) / len(dynStopwords)

    print("Dynamically derived stopwords: \n", dynStopwords)
    print("Stopwords from NLTK: \n", nltkStopwords)
    print("Overlap: ", portion)

    print("done")

if __name__ == '__main__':
    #arguments = parse_arguments()
    main()
