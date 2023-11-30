import re
class CustomizedTreebankTokenizer():

    #todo: add rule to split don't into do and n't
    #can't is a special case and will be substituted with cannot (expansion)
    #n't: look wether ' is surrounded by n and t and then split before n
    #all other clitcs are simply separated but not expanded

    RULES = [
        (re.compile(r"([\(\)\[\]\{\}\<\>])"), r" \1 "),  # pad brackets with whitespaces
        (re.compile(r"([\"\'\´\`])"), r" \1 "),  # pad quotation marks with whitespaces
        (re.compile(r"\n"), r" "),  # replace newline by whitespace
        (re.compile(r"([.,;:!?%\"\'\)\]])(?=\s|$|\n)"), r" \1 "),  # separate punctuation that is followed by a whitespace
        (re.compile(r"^([.,;:!?%\"\'])"), r" \1 "),  # separate punctuation at the beginning of a string
        (re.compile(r"\.\.\."), r" ... "),  # separate out 3 periods as a single token
        (re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"), r"<EMAIL>"), #email placeholder
        (re.compile(r"\b(?:https?://|www\.)\S+?(?=\s|$)"), r"<URL>"), #URL placeholder
    ]

    CLITICS_RULES = [

    ]

    def tokenize(self, text: str, splitClitcsEnabled):

        for pattern, substitution in self.RULES:
            text = pattern.sub(substitution, text)
        text =  text.split()

        if splitClitcsEnabled:
            for pattern, substitution in self.CLITICS_RULES:
                text = pattern.sub(substitution, text)

        return text.split()


