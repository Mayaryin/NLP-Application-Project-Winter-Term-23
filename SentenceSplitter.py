import re
class SentenceSplitter:

    #detect different types of end-of-sentence markers
    #markers: . ? !
    #we need to filter out exclamation and question marks that appear in brackets
    #we need to detect any markers that are followed by quotation marks
    #we need an abbreviation dictionary to filter out periods that follow an abbreviation

    #todo: r"[a-zA-Z.] matches every word that ends with a period. this should be changed so that it matches sequences of letters and periods (U.S.)

    def isAbbreviation(self, word, abbreviations ):
        return word in abbreviations or re.match(r"[a-zA-Z.]+", word) or re.match(r"[^aeiouAEIOU]*\.", word)

    def thereIsANextWord(self, text, index):
        return index + 1 < len(text)

    def nextWordIsCapitalized(self,text, index):
        if self.thereIsANextWord(text, index):
            return re.match(r"\b[A-Z][a-zA-Z]*\b", text[index+1])
        else: return True

    def wordIsFollowedByPeriod(self, word):
        return re.match(r".*\.", word)


    def split(self, text):
        abbreviations = ["abv1.", "abv2."]
        splitText = []
        text = text.split()
        startIndex = 0
        for i, word in enumerate(text[:]):


            if self.wordIsFollowedByPeriod(word):
                if not self.isAbbreviation(word, abbreviations):
                    splitText.append(text[startIndex:i+1])
                    startIndex = i+1
                else:
                    if self.isAbbreviation(word, abbreviations):
                        if self.nextWordIsCapitalized(text, i):
                            splitText.append(text[startIndex:i + 1])
                            startIndex = i + 1
        if startIndex < len(text):
            splitText.append(text[startIndex:])

        return splitText



