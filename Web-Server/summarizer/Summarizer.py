# A summarizer class
from __future__ import division
import os
import math
import nltk
import string
from collections import defaultdict
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords

class Summarizer(object):
    def __init__(self):
        self.stemmer = SnowballStemmer("english")
        self.stopwords = set([ w.encode('ascii') for w in stopwords.words("english") ])

    def summarize(self, text):
        pass

    """ Text Processing """
    def preprocess_sents(self, sentences):
        # Case folding step. Put all words in lower case and remove punctuations
        processed_sentences = [ sent.lower().translate(None, string.punctuation) for sent in sentences ]
        processed_sentences = self.stop_and_stem_process(processed_sentences)
        return [ sent for sent in processed_sentences if len(sent) > 0]

    def stop_and_stem_process(self, sentences):
        new_sents = []
        for sent in sentences:
            new_sents.append([ self.stemmer.stem(word).encode('ascii') for word in sent.split() if not word in self.stopwords ])
        return new_sents

    """ Miscellaneous """
    def __compare(self, x, y):
        if(x[1] > y[1]):
            return -1
        elif x[1] < y[1]:
            return 1
        else:
            return 0
