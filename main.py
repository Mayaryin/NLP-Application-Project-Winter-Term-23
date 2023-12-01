#!/usr/bin/env python3
"""Module Docstring: A brief description of what this script does."""

# Imports

from TokenizerRulebased import TokenizerRulebased
from TokenizerML import TokenizerML
from SentenceSplitterRulebased import SentenceSplitter
from SentenceSplitterML import RegressionSentenceSplitter
from Normalizer import Normalizer
from LexiconComplier import LexiconCompiler
from nltk.tokenize import TreebankWordTokenizer
from StopwordEliminatorDynamic import DynamicStopwordEliminator
from BinaryNaiveBayesClassifier import BinaryNaiveBayesClassifier




def main():
    print("Script started.")
    text = "(I like cats & dogs... but (I) don't like birds!)" \
           ".()345 !" \
           "\"" \
           "multi-word expression \n New York \n" \
           "blabla@email.com\n" \
           "https://www.google.com/\n" \
           "#hashtag"

    #sentences = TokenizerML().importData("UD_English-GUM/en_gum-ud-train.conllu")
    #text2 = TokenizerML().unsplit(sentences)

    ##Bayes Tokenizer
    texttest = " this that the U.S. but is haven't aren't test? After abv2. I think. U.S.A USA usa I'm aren't"
    TokenizerML().train("UD_English-GUM/en_gum-ud-train.conllu")
    TokenizerML().test("UD_English-GUM/en_gum-ud-test.conllu")
    print("rulebased: ", TokenizerRulebased().tokenize(texttest, True, False, False))
    print("ML       : ", TokenizerML().tokenize(texttest))

    ##Sentence Splitter
    #print(SentenceSplitter().split(text))

    #text = " this  that the U.S. but is  a test? After abv2. I think. U.S.A USA usa I'm are'nt"
    #text = "ich heiße bananenpunkt. Der nächste Tag ist eine Ab.kürzung; Ja so war das! und was ist hiermit... ? K;23. 34.5 U.S. neuer Satz begonnen."
    #text = rSenSplitter.unsplit(rSenSplitter.importData("UD_English-GUM/en_gum-ud-dev.conllu"))
    #text = ["I", "'m", "U.S.A", "usa", "test", "."]



    ###Dyn. Stopwords

    #tokens = CustomizedTreebankTokenizer().tokenize(text, True, True, True)
    #print(DynamicStopwordEliminator(tokens).deriveStopwords(tokens))

    ##Bayes Tokenizer
    #BayesTokenizer().train("UD_English-GUM/en_gum-ud-train.conllu")
    #BayesTokenizer().test("UD_English-GUM/en_gum-ud-test.conllu")
    #text3 = "I don't like food (apples)! My mail's ding@ding.com 3.5$"
    #print(BayesTokenizer().tokenize(text3))
    #print(CustomizedTreebankTokenizer().tokenize(text3, True, False, False))

    print("done")

    #LexiconCompiler().compile()



# Entry-point check
if __name__ == '__main__':
    #arguments = parse_arguments()
    main()
