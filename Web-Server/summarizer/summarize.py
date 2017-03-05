#!/bin/python
import sys
from tfidfSummarizer import tfidfSummarizer
from graphSummarizer import graphSummarizer

method = sys.argv[1]
compressionFactor = float(sys.argv[2])
text = sys.argv[3]

if(len(text) > 0):
    if(method == "Graph"):
        summarizer = graphSummarizer(compressionFactor)
    elif(method == "TFISF"):
        summarizer = tfidfSummarizer(compressionFactor)

    summary = summarizer.summarize(text)
    print summary

sys.stdout.flush()
exit(0)
