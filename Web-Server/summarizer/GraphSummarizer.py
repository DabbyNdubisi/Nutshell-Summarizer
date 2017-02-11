from __future__ import division
import os
import math
import nltk
import string
from collections import defaultdict
from Summarizer import Summarizer
from Graph import Graph
from Graph import GraphNode

class graphSummarizer(Summarizer):
    def __init__(self, damping=0.85, compression=0.8):
        super(self.__class__, self).__init__()
        self.damping = damping
        self.compression = compression

    def summarize(self, text):
        text = " ".join(text.split("\n"))
        original_sents = nltk.sent_tokenize(text)
        processed_sentences = self.preprocess_sents(original_sents)
        # create sentence graph
        graph = self.create_sents_graph(processed_sentences)

        # compute textRank on graph
        self.text_rank_transform(graph)

        # make summary
        ranked_sents = sorted(graph.vertices_scores, key=graph.vertices_scores.get, reverse=True)
        summ_len = int(len(original_sents) * (1 - self.compression))
        summIdx = []
        for i in range(min(summ_len, len(ranked_sents))):
            summIdx.append(ranked_sents[i].data)

        summary = [original_sents[idx] for idx in sorted(summIdx)]
        print " ".join(summary)
        print("summary length: %d" %(len(summary)))
        print("original length: %d" %(len(original_sents)))



    " Text Transormation stage functions"
    def create_sents_graph(self, sents):
        graph = Graph('undirected')

        # add vertices
        # use original sentence location as vertex
        for i in range(len(sents)):
            graph.add_vertex(i)

        # add edges
        for i in range(len(sents)):
            sentI_len = len(sents[i])
            for j in range(i+1, len(sents)):
                sentJ_len = len(sents[j])
                common_words_len = len([ word for word in sents[i] if word in set(sents[j]) ])
                if(common_words_len > 0):
                    simm_score = common_words_len/(1 + math.log(sentI_len, 2) + math.log(sentJ_len, 2))
                    graph.add_edge(GraphNode(i), GraphNode(j), simm_score)

        return graph

    def text_rank_transform(self, graph):
        temp_map = defaultdict(dict)
        convergence_const = 0.001
        has_converged = False
        count = 0
        while(not has_converged):
            has_converged = True
            for v_i in graph.vertices:
                old_score = graph.get_vertex_score(v_i)
                total = 0.0
                for v_j in graph.in_vertices(v_i):
                    if(not(v_i in temp_map and v_j in temp_map[v_i])):
                        temp_map[v_i][v_j] = reduce((lambda x, y: x + y), map((lambda v_k: graph.edge_weight(v_k, v_j)), graph.out_vertices(v_j)))
                    total += (graph.edge_weight(v_j, v_i) * graph.get_vertex_score(v_j) / temp_map[v_i][v_j])
                graph.set_vertex_score(v_i, (1 - self.damping) + (self.damping * total))
                has_converged = has_converged and abs(graph.get_vertex_score(v_i) - old_score) < convergence_const

summarizer = graphSummarizer()
summarizer.summarize(open("./text.txt", 'r').read())
