import re
class CustomizedTreebankTokenizer():

    #can't is a special case and will be substituted with cannot (expansion)
    #n't: look wether ' is surrounded by n and t and then split before n
    #all other clitcs are simply separated but not expanded

    RULES = [
        (re.compile(r"([\(\)\[\]\{\}\<\>])"), r" \1 "),  # pad brackets with whitespaces
        (re.compile(r"([\"\´\`])"), r" \1 "),  # pad quotation marks with whitespaces
        (re.compile(r"\n"), r" "),  # replace newline by whitespace
        (re.compile(r"([.,;:!?%\"\'\)\]])(?=\s|$|\n)"), r" \1 "),  # separate punctuation that is followed by a whitespace
        (re.compile(r"^([.,;:!?%\"\'])"), r" \1 "),  # separate punctuation at the beginning of a string
        (re.compile(r"\.\.\."), r" ... "),  # separate out 3 periods as a single token

    ]

    SPECIAL_ENTITIES_RULES = [
        (re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"), r"<EMAIL>"),  # email placeholder
        (re.compile(r"\b(?:https?://|www\.)\S+?(?=\s|$)"), r"<URL>"),  # URL placeholder
    ]

    CLITICS_RULES = [
         #regular cases will be split
        (re.compile(r"(\b\w+)(\'m)\b"), r"\1 \2"),
        (re.compile(r"(\b\w+)(\'ve)\b"), r"\1 \2"),
        (re.compile(r"(\b\w+)(\'ll)\b"), r"\1 \2"),
        (re.compile(r"(\b\w+)(\'d)\b"), r"\1 \2"),
        (re.compile(r"(\b\w+)(\'s)\b"), r"\1 \2"),
        (re.compile(r"(\b\w+)(\'re)\b"), r"\1 \2"),
        (re.compile(r"(\b\w+)(n\'t)\b"), r"\1 \2"),
    ]

    def tokenize(self, text: str, splitClitcsEnabled, specialCasesEnabled, specialEntitiesEnabled):

        if splitClitcsEnabled:
            for pattern, substitution in self.CLITICS_RULES:
                text = pattern.sub(substitution, text)

        if specialCasesEnabled:
            text = re.sub(r"\bwon\'t\b", "will not", text)
            text = re.sub(r"\bcan\'t\b", "cannot", text)

        if specialCasesEnabled:
            for pattern, substitution in self.SPECIAL_ENTITIES_RULES:
                text = pattern.sub(substitution, text)

        for pattern, substitution in self.RULES:
            text = pattern.sub(substitution, text)

        text = text.split()

        return text


