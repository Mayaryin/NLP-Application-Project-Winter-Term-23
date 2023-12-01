#!/usr/bin/env python3
"""Module Docstring: A brief description of what this script does."""

# Imports

from TokenizerRulebased import TokenizerRulebased
from TokenizerML import TokenizerML
from SentenceSplitterRulebased import SentenceSplitter
from SentenceSplitterML import SentenceSplitterML
from Normalizer import Normalizer
from LexiconComplier import LexiconCompiler
from nltk.tokenize import TreebankWordTokenizer
from StopwordEliminatorDynamic import DynamicStopwordEliminator
from BinaryNaiveBayesClassifier import BinaryNaiveBayesClassifier




def main():
    print("NLP Text Processing Pipeline")

    #LexiconCompiler().compile()

    ##Tokenizer
    ##1: window features
    #2: general features
    print("\nTOKENIZER")
    mlTokenizer = TokenizerML()
    texttest = " this that the U.S. but is haven't aren't test? After abv2. I think. U.S.A USA usa I'm aren't"
    texttest2 = " I haven't lived in the U.S. but I'll do it. What about you?"
    mlTokenizer.train("UD_English-GUM/en_gum-ud-train.conllu", 2)
    mlTokenizer.test("UD_English-GUM/en_gum-ud-test.conllu", 2)
    print("rulebased: ", TokenizerRulebased().tokenize(texttest2, True, False, False))
    print("Bayes    : ", mlTokenizer.tokenize(texttest2, 2))

    ##Sentence Splitter
    print("\nSENTENCE SPLITTER")
    textForSentSplitter = "I like cats. Do you like cats, too? I hate #hashtags!"
    mlSentenceSplitter = SentenceSplitterML()
    mlSentenceSplitter.train("UD_English-GUM/en_gum-ud-train.conllu")
    mlSentenceSplitter.test("UD_English-GUM/en_gum-ud-test.conllu")
    print("Rulebased : \n", SentenceSplitter().split(textForSentSplitter))
    print("Regression: \n", mlSentenceSplitter.split(textForSentSplitter))

    #text = " this  that the U.S. but is  a test? After abv2. I think. U.S.A USA usa I'm are'nt"
    #text = "ich heiße bananenpunkt. Der nächste Tag ist eine Ab.kürzung; Ja so war das! und was ist hiermit... ? K;23. 34.5 U.S. neuer Satz begonnen."
    #text = rSenSplitter.unsplit(rSenSplitter.importData("UD_English-GUM/en_gum-ud-dev.conllu"))
    #text = ["I", "'m", "U.S.A", "usa", "test", "."]

    ##Normalizer
    print("\nNORMALIZER")
    normalizerText = "The U.S.A are large, i made a speling mistak."
    print("Misspelled text: ", normalizerText)
    normalizer = Normalizer("english_lexicon.csv")
    tokens = TokenizerRulebased().tokenize(normalizerText, True, True, True)
    print("Normalized text: ", normalizer.normalize(tokens, True))


    ###Dyn. Stopwords
    print("\nSTOPWORDS")
    sentences = TokenizerML().importData("UD_English-GUM/en_gum-ud-train.conllu")
    stopwordsText = TokenizerML().unsplit(sentences)
    tokens = TokenizerRulebased().tokenize(stopwordsText, True, True, True)
    print("Dynamically derived stopwords: \n", DynamicStopwordEliminator(tokens).deriveStopwords(tokens))



    print("done")

    #



# Entry-point check
if __name__ == '__main__':
    #arguments = parse_arguments()
    main()
