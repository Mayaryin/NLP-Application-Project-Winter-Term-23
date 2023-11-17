#!/usr/bin/env python3
"""Module Docstring: A brief description of what this script does."""

# Imports

from CustomizedTreebankTokenizer import CustomizedTreebankTokenizer
from BayesTokenizer import BayesTokenizer
from SentenceSplitter import SentenceSplitter
from RegressionSentenceSplitter import RegressionSentenceSplitter




def main():
    print("Script started.")
    text = "(I like cats & dogs... but (I) don't like birds!)" \
           ".()345 !" \
           "\"" \
           "multi-word expression \n New York \n" \
           "blabla@email.com\n" \
           "https://www.google.com/\n" \
           "#hashtag"
   # print(text)


    tokenizer =  CustomizedTreebankTokenizer()
    bayesTokenizer = BayesTokenizer()
    #bayesTokenizer.printDocuments()
    trainingSet,_,_ = bayesTokenizer.splitCorpus()
    #print(trainingSet[:20])
   # print(tokenizer.tokenize(text))
    #text = "This is U.S. but is this a test? After abv2. I think."
    #text = text.split()
    #sentenceSplitter = SentenceSplitter()
    #print(sentenceSplitter.split(text))
    rSenSplitter = RegressionSentenceSplitter()
    rSenSplitter.train('UD_English-GUM/en_gum-ud-train.conllu')
    rSenSplitter.test('UD_English-GUM/en_gum-ud-test.conllu')
    text = "ich heiße bananenpunkt. Der nächste Tag ist eine Ab.kürzung; Ja so war das! und was ist hiermit... ? K;23. 34.5 U.S. neuer Satz begonnen."
    print(rSenSplitter.split(text))
    print("done")


# Entry-point check
if __name__ == '__main__':
    #arguments = parse_arguments()
    main()
