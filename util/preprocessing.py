import pandas as pd
import re
import nltk
import string


class PreProcessing:
    def __init__(self, language="english"):
        self.stopwords = nltk.corpus.stopwords.words(language)

    def remove_punct(self, text):
        text_nonpunct = "".join([char for char in text if char not in string.punctuation])
        return text_nonpunct

    def tokenize(self, text):
        tokens = re.split('\W+', text)
        return tokens

    def remove_stopwords(self, tokenized_list):
        # Stemming
        ps = nltk.PorterStemmer()
        text = [ps.stem(word) for word in tokenized_list if word not in self.stopwords]
        return text

    def clean_text(self, text):
        # Removing Punctuations
        text = self.remove_punct(text)

        # tokenizing the texts
        tokens = self.tokenize(text)

        # removing stopwords
        text = self.remove_stopwords(tokens)

        # returning the cleaned data
        return text

