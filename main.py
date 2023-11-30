#!/usr/bin/env python3
"""Module Docstring: A brief description of what this script does."""

# Imports

from CustomizedTreebankTokenizer import CustomizedTreebankTokenizer
from BayesTokenizer import BayesTokenizer
from SentenceSplitter import SentenceSplitter
from RegressionSentenceSplitter import RegressionSentenceSplitter
from Normalizer import Normalizer
from LexiconComplier import LexiconCompiler
from nltk.tokenize import TreebankWordTokenizer




def main():
    print("Script started.")
    text = "(I like cats & dogs... but (I) don't like birds!)" \
           ".()345 !" \
           "\"" \
           "multi-word expression \n New York \n" \
           "blabla@email.com\n" \
           "https://www.google.com/\n" \
           "#hashtag"


    #text = "I'm you're youre im won't can't don't"
    #print(CustomizedTreebankTokenizer().tokenize(text, True))

    #text = " this  that the U.S. but is  a test? After abv2. I think. U.S.A USA usa I'm are'nt"
    #text = "ich heiße bananenpunkt. Der nächste Tag ist eine Ab.kürzung; Ja so war das! und was ist hiermit... ? K;23. 34.5 U.S. neuer Satz begonnen."
    #text = rSenSplitter.unsplit(rSenSplitter.importData("UD_English-GUM/en_gum-ud-dev.conllu"))
    #text = ["I", "'m", "U.S.A", "usa", "test", "."]

    #print(TreebankWordTokenizer().tokenize(text))
    text2 = "New-York"
    #print(TreebankWordTokenizer().tokenize(text2))

    sentences = BayesTokenizer().importData("UD_English-GUM/en_gum-ud-train.conllu")
    text = BayesTokenizer().unsplit(sentences)

    #print(BayesTokenizer().tokenizeTrainingData(text))

    BayesTokenizer().train("UD_English-GUM/en_gum-ud-train.conllu")
    #BayesTokenizer().test("UD_English-GUM/en_gum-ud-test.conllu")
    text3 = "I don't like food (apples)!"
    print(BayesTokenizer().tokenize(text3))

    print("done")

    #LexiconCompiler().compile()



# Entry-point check
if __name__ == '__main__':
    #arguments = parse_arguments()
    main()
