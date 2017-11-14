'''
Created on 14 Nov 2017

@author: mlecce
'''

###############################################################################################################################################
#                                                  Import section
#
###############################################################################################################################################

import networkx as nx
from networkx.algorithms import isomorphism

###############################################################################################################################################
#                                                  Functions' section
#
###############################################################################################################################################

def check_isomorphism(G1, G2):
    GM = isomorphism.DiGraphMatcher(G1, G2)
    if(GM.is_isomorphic()):
        print("The two graphs are isomorphic!")  
    else: 
        print("The two graphs are not isomorphic!")
        
def check_subgraph_isomorphism(G1, G2):
    GM = isomorphism.DiGraphMatcher(G1, G2)
    if(GM.subgraph_is_isomorphic()):
        print("A subgraph in G1 is isomorphic to G2!")  
    else: 
        print("No match found!")
        
def print_isomorphic_subgraphs(G1, G2):
    GM = isomorphism.DiGraphMatcher(G1, G2)
    i=0
    for graph in GM.subgraph_isomorphisms_iter():
        #Print the subgraph only if all the pairs of nodes have the same component type 
        node_types1 = nx.get_node_attributes(G1, "compType")
        node_types2 = nx.get_node_attributes(G2, "compType")
        i+=1
        for key , value in graph.items():
            if (node_types1[key] != node_types2[value]):
                print("SubGraph" + str(i))
                print("Not all node pairs matching the same component type")
                break #exit the for without executing the else 
        else:
            print("SubGraph" + str(i))
            print(graph)
            print("\n")