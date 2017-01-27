# A summarizer that uses the statistical tfidf
# to summarize text
from __future__ import division
import os
import math
import nltk
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords

class tfidfSummarizer:
    def __init__(self, threshold):
        self.sents_vects = []
        self.inverse_sents_frequency_map = dict()
        self.summary_threshold = threshold

    def summarize(self, text):
        text = " ".join(text.split("\n"))
        original_sents = nltk.sent_tokenize(text)
        processed_sentences = self.preprocess_sents(original_sents, 'n-gram')
        # build sparse vectors
        self.create_sents_vects(processed_sentences)
        # transform sentence vectors to tfidf values
        self.tfidf_transform()

        # compute average tfidf for each sentence
        sents_scores = []
        for i in range(len(self.sents_vects)):
            vect = self.sents_vects[i]
            total = 0
            for term in vect:
                total += vect[term]
            sents_scores.append((i, total/len(vect)))

        # create summarized text
        sents_scores.sort(self.__compare)
        avg_max = sents_scores[0][1]
        threshold = self.summary_threshold * avg_max
        sents_idx_for_summary = []
        for i in range(len(sents_scores)):
            if sents_scores[i][1] >= threshold:
                sents_idx_for_summary.append(sents_scores[i][0])
            else:
                break

        # sort summary index to create some form of cohesion
        sents_idx_for_summary.sort()

        print " ".join(original_sents[i] for i in sents_idx_for_summary)
        print("Original len: %d" %(len(original_sents)))
        print("Summary len: %d" %(len(sents_idx_for_summary)))

    def preprocess_sents(self, sentences, method=''):
        # Case folding step. Put all words in lower case
        processed_sentences = [ sent.lower() for sent in sentences ]
        if(method == 'n-gram'):
            return self.n_gram_process(processed_sentences)
        else:
            return self.stop_and_stem_process(processed_sentences)

    def create_sents_vects(self, sentences):
        for i in range(len(sentences)):
            sentence = sentences[i]
            map = dict()
            for word in sentence:
                #update number of sentences containing term
                if(not word in self.inverse_sents_frequency_map):
                    self.inverse_sents_frequency_map[word] = set([])
                self.inverse_sents_frequency_map[word].add(i)

                # update term frequency in current sentence
                if(not word in map):
                    map[word] = 0
                map[word] += 1
            self.sents_vects.append(map)

    def tfidf_transform(self):
        count = len(self.sents_vects)
        for vector in self.sents_vects:
            for term in vector:
                vector[term] *= (math.log10(count / len(self.inverse_sents_frequency_map[term])))

    def stop_and_stem_process(self, sentences):
        stemmer = SnowballStemmer("english")
        toRemove = set([ w.encode('ascii') for w in stopwords.words("english") ])
        new_sents = []
        for sent in sentences:
            new_sents.append([ stemmer.stem(word).encode('ascii') for word in sent.split() if not word in toRemove ])
        return new_sents

    def n_gram_process(self, sentences, ngram=5):
        new_sents = []
        stemmer = SnowballStemmer("english")
        for sent in sentences:
            ngram_sent = []
            for word in sent.split():
                ngram_sent += self.__ngrams_for_word__(stemmer.stem(word).encode('ascii'), ngram)
            new_sents.append(ngram_sent)
        return new_sents

    def __ngrams_for_word__(self, word, ngram):
        if(len(word) < ngram):
            return [word]
        else:
            word = "_" + word + "_"
            ngrams = []
            start = 0
            for i in range(ngram, len(word)+1):
                ngrams.append(word[start:i])
                start += 1
            return ngrams

    def __compare(self, x, y):
        if(x[1] > y[1]):
            return -1
        elif x[1] < y[1]:
            return 1
        else:
            return 0

summarizer = tfidfSummarizer(0.8)
summarizer.summarize(open("./text.txt", 'r').read())
