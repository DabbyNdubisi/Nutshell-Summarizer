# A summarizer that uses the statistical tfidf
# to summarize text
from __future__ import division
import os
import math
import nltk
import string
from collections import defaultdict
from Summarizer import Summarizer

class tfidfSummarizer(Summarizer):
    def __init__(self, threshold=0.8):
        super(self.__class__, self).__init__()
        self.sents_vects = []
        self.inverse_sents_frequency_map = defaultdict(set)
        self.summary_threshold = threshold

    def summarize(self, text):
        text = " ".join(text.split("\n"))
        original_sents = nltk.sent_tokenize(text)
        processed_sentences = self.preprocess_sents(original_sents)
        # build sparse vectors
        self.create_sents_vects(processed_sentences)
        # score sentece vectors
        sents_scores = self.score_sents_vects()
        sents_scores = [ (i, sents_scores[i]) for i in range(len(sents_scores)) ]

        # create summarized text
        sents_scores.sort(self.compare)
        num_sents_threshold = int((1 - self.summary_threshold) * len(sents_scores))
        sents_idx_for_summary = []
        for i in range(len(sents_scores)):
            if len(sents_idx_for_summary) <= num_sents_threshold:
                sents_idx_for_summary.append(sents_scores[i][0])
            else:
                break

        # sort summary index to create some form of cohesion
        sents_idx_for_summary.sort()

        return " ".join(original_sents[i] for i in sents_idx_for_summary)
        # print("Original len: %d" %(len(original_sents)))
        # print("Summary len: %d" %(len(sents_idx_for_summary)))

    """ sentence vectors scoring """
    def score_sents_vects(self):
        # Score sentence vectors using:
        #  - tf-isf
        #  - sentence position (sentences at beginning and ending get higher ranks)
        #  - sentence similarity with other sentences
        #  - number of keywords in sentence
        # To handle overfitting, the weights of each sentece are normalized
        # using the average length of a sentence.

        key_words = self.compute_key_words()
        sent_similarity_scores = self.sents_to_sents_similarity()
        num_sents = len(self.sents_vects)
        num_words = reduce((lambda x, y: x + y), map((lambda x: len(x)), self.sents_vects))
        avg_sent_length = num_words / num_sents
        num_key_words = len(key_words)

        # compute average tfisf for each sentence
        self.tfidf_transform()
        sents_scores = []
        for i in range(len(self.sents_vects)):
            vect = self.sents_vects[i]
            count = len(vect)
            total = 0
            for term in vect:
                total += vect[term]
            sents_scores.append(total/count)

        # - add sentence position weight to sentence scores
        # - add sentence similarity weight
        # for i in range(len(self.sents_vects)):
        #     sents_scores[i] += len([ w for w in self.sents_vects[i] if w in key_words ])/len(self.sents_vects[i])

        # handle overfitting
        for i in range(len(self.sents_vects)):
            sents_scores[i] *= len(self.sents_vects[i]) / avg_sent_length

        return sents_scores

    def create_sents_vects(self, sentences):
        # Turns each sentence into a vector of
        # their containing terms frequencies
        for i in range(len(sentences)):
            sentence = sentences[i]
            map = defaultdict(int)
            for word in sentence:
                #update number of sentences containing term
                self.inverse_sents_frequency_map[word].add(i)
                # update term frequency in current sentence
                map[word] += 1
            self.sents_vects.append(map)

    def compute_key_words(self):
        # keywords are terms which have frequency
        # above the average term frequency
        termFreqs = defaultdict(int)
        avg = 0
        for sent_vect in self.sents_vects:
            for term in sent_vect:
                termFreqs[term] += sent_vect[term]
                avg += sent_vect[term]

        avg /= len(termFreqs)
        return set([ w for w in termFreqs if termFreqs[w] >= avg ])

    def sents_to_sents_similarity(self):
        # two sentences are similar if they have at least one shared word
        # return a map of sentence index to similarity number
        similarity_map = defaultdict(int)
        for i in range(len(self.sents_vects)):
            for j in range(i+1, len(self.sents_vects)):
                if(len([x for x in self.sents_vects[i] if x in set(self.sents_vects[j]) ]) > 0):
                    similarity_map[i] += 1
                    similarity_map[j] += 1
        return similarity_map

    def tfidf_transform(self):
        # Compute the tf-isf weighting of each sentence vector
        count = len(self.sents_vects)
        for vector in self.sents_vects:
            for term in vector:
                vector[term] *= (1 + math.log10(count/len(self.inverse_sents_frequency_map[term])))
