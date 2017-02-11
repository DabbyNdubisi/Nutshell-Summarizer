from collections import defaultdict
import random

class GraphNode(object):
    def __init__(self, data):
        self.data = data

    def __hash__(self):
        return hash(self.data)

    def __eq__(self, other):
        return self.data == other.data


class Graph(object):
    def __init__(self, type):
        self.type = type
        self.vertices = []
        self.edges = defaultdict(dict)
        self.vertices_scores = defaultdict(float)

    def add_vertex(self, data):
        node = GraphNode(data)
        self.vertices.append(node)
        self.vertices_scores[node] = random.uniform(1.0, 2.0)

    def add_edge(self, fromV, toV, weight=1.0):
        if(fromV in self.vertices and toV in self.vertices):
            self.edges[fromV][toV] = weight
            if(self.type == 'undirected'):
                self.edges[toV][fromV] = weight

    def in_vertices(self, vertex):
        if(self.type == 'undirected'):
            return self.edges[vertex].keys()
        else:
            [ node for node in self.vertices if vertex in self.edges[node] ]

    def out_vertices(self, vertex):
        return self.edges[vertex].keys()

    def edge_weight(self, fromV, toV):
        if(toV in self.edges[fromV]):
            return self.edges[fromV][toV]

    def get_vertex_score(self, vertex):
        return self.vertices_scores[vertex]

    def set_vertex_score(self, vertex, score):
        self.vertices_scores[vertex] = score
