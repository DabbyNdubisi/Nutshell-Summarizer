# Tokenizer for brown corpus
import re
from nltk.corpus import stopwords;

class Tokenizer:
    def sentences(self, text):
        return [ self.words(x) for x in text.strip().split('. ') ]

    def words(self, text):
        return self.__filter_words([ self.extract_word_tag(x)[0] for x in text.strip().split(' ') ], [""])

    def extract_word_tag(self, text):
        m = re.match(r"\s*(.+/?.*)/(.+)", text)
        if(m):
            return (m.group(1, 2))
        else:
            return ("", "")

    def filter_stop_words(self, words, stopwords=stopwords.words("english")):
        return self.__filter_words(words, stopwords)

    def __filter_words(self, words, toRemove):
        to_remove = set(toRemove)
        return [ x for x in words if not x.lower() in to_remove ]
