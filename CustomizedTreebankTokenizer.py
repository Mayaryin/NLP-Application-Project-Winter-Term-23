import re
class CustomizedTreebankTokenizer():

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

    def tokenize(self, text: str):

        for pattern, substitution in self.RULES:
            text = pattern.sub(substitution, text)
        return text.split()


