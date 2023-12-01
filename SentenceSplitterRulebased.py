import re
import csv
class SentenceSplitter:

    #detect different types of end-of-sentence markers
    #markers: . ? !
    #we need to detect any markers that are followed by quotation marks
    #we need an abbreviation dictionary to filter out periods that follow an abbreviation
    #sentences like He said "I don't care." are syntactically wrong. they would be spliited
    #incorrectly by this splitter

    def __init__(self):
        self.abbreviationList = self.read_csv("abbr.csv")

    def read_csv(self, path):
        with open(path, 'r') as file:
            reader = csv.reader(file)
            data_list = [row[0] for row in reader]
        return data_list

    def isAbbreviation(self, word):
        return word in self.abbreviationList \
            or re.match(r"[a-zA-Z]+(\.[a-zA-Z.]+)+", word) \
            or re.match(r"[^aeiouAEIOU]*\.", word)

    def thereIsANextWord(self, text, index):
        return index + 1 < len(text)

    def nextWordIsCapitalized(self,text, index):
        if self.thereIsANextWord(text, index):
            return re.match(r"\b[A-Z][a-zA-Z]*\b", text[index+1])
        else: return True

    def wordEndsWithEOSMarker(self, word):
        return re.match(r".*[\.?!]", word)

    def wordEndsWithEOSMarkerAndQuotationMark(self, word):
        return re.match(r".*[\.\?!][\"\'\´\`]", word)

    def nextWordStartsWithQuotationMark(self, text, index):
        if self.thereIsANextWord(text, index):
            return re.match(r"[\"\'\´\`].*", text[index + 1])
        else:
            return True


    def split(self, token_list):
        splitText = []
        startIndex = 0
        for i, word in enumerate(token_list):

            if self.wordEndsWithEOSMarker(word) or self.wordEndsWithEOSMarkerAndQuotationMark(word):
                if not self.isAbbreviation(word):
                    splitText.append(token_list[startIndex:i+1])
                    startIndex = i+1
                else:
                    if self.isAbbreviation(word):
                        if self.nextWordIsCapitalized(token_list, i) or self.nextWordStartsWithQuotationMark(token_list, i):
                            splitText.append(token_list[startIndex:i + 1])
                            startIndex = i + 1
        if startIndex < len(token_list):
            splitText.append(token_list[startIndex:])
        concatenated_sentences = [' '.join(sentence) for sentence in splitText]

        return concatenated_sentences



