#!/bin/python
import sys
from tfidfSummarizer import tfidfSummarizer
from graphSummarizer import graphSummarizer

method = sys.argv[1]
compressionFactor = float(sys.argv[2])
text = ""
filpath = ""

if(len(sys.argv) == 4):
    text = sys.argv[3];
elif(len(sys.argv) == 5):
    text = open(sys.argv[4], 'r').read().decode('utf8').encode('ascii', 'replace')

if(len(text) > 0):
    if(method == "Graph"):
        summarizer = graphSummarizer(compressionFactor)
    elif(method == "TFISF"):
        summarizer = tfidfSummarizer(compressionFactor)

    summary = summarizer.summarize(text)
    print summary

sys.stdout.flush()
exit(0)
