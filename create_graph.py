'''
Created on 23 Oct 2017

@author: mlecce
'''

import networkx as nx
from format_input import input_formatter

#Format the input file so that it is possible to read the edges and write it to file output
input_formatter('parse.txt', 'edgelist.txt')

#Create a directed graph 
DG=nx.DiGraph()

#Read the edge list and populate the graph
DG=nx.read_edgelist("edgelist.txt")

#Print some information on the just read graph
print("Number of nodes: ")
print(DG.number_of_nodes())

print("Edges: ")
edges = [e for e in DG.edges.data()]
print(edges)

#Trash   
print("Edges from/to node Scheme: ")
l=DG.neighbors("Scheme")

for node in l:
    print(node)

print(DG.has_edge("Msg", "Actor"))

