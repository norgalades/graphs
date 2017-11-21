'''
Created on 14 Nov 2017

@author: mlecce
'''
###############################################################################################################################################
#                                                  Description
#
###############################################################################################################################################

''' 
This file provides functions to operate on the graphs. Each function has a paragraph at the beginning to explain its purpose
'''

###############################################################################################################################################
#                                                  Import section
#
###############################################################################################################################################

import networkx as nx
import os
from networkx.algorithms import isomorphism

###############################################################################################################################################
#                                                  Variable assignment
#
###############################################################################################################################################

#Threshold for the number of nodes on subgraphs matching isomorphism criterias
T = 3 

###############################################################################################################################################
#                                                  Functions' section
#
###############################################################################################################################################

def print_graph(G):
    nodes = [n for n in G.nodes()]
    #compTypes = nx.get_node_attributes(G, "compType")
    for node in nodes: 
        #print(node + ": " + compTypes[node])
        print(node + ": ")
        for nb in nx.all_neighbors(G, node): 
            print(nb)
        print("\n")

def check_isomorphism(G1, G2):
    GM = isomorphism.DiGraphMatcher(G1, G2)
    if(GM.is_isomorphic()):
        print("The two graphs are isomorphic!")  
    else: 
        print("The two graphs are not isomorphic!")

'''
This function checks if there is any subgraph in G1 that is isomorph to G2, and returns the number of nodes of the biggest subgraph matching 
G2 (if any)
'''        
def check_subgraph_isomorphism(G1, G2):
    GM = isomorphism.DiGraphMatcher(G1, G2)
    if(GM.subgraph_is_isomorphic()):
        nodes = []
        #An iterator of the type: nodeA_in_G1 : nodeA_prime_in_G2 over all the subgraphs that match G2
        for G in GM.subgraph_isomorphisms_iter():
            print("All subgraphs of G1 matching G2: ")
            print(G)
            nodes.append(len(G))
        return max(nodes)
    else: 
        return 0

'''
Check if the node type is the same for each couple of corresponding nodes in G1 and G2. 
It also receives the mapping between the nodes (a dictionary with all the the couples of corresponding nodes) 
''' 
def check_nodes_criteria(G1, G2, mapping):
    node_types1 = nx.get_node_attributes(G1, "compType")
    node_types2 = nx.get_node_attributes(G2, "compType")
    for key , value in mapping:
        if (node_types1[key] != node_types2[value]):
            return 0
    else:
        return 1                   
      
'''
Prints the subgraphs matching the criteria 
'''            
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
            print_graph(graph)
            print("\n")  

'''
Given two graphs, find if there are common isomorphic subgraphs and return the biggest one as a mapping of type nodeA_in_G1 : nodeA_prime_in_G2
'''
def find_max_subgraph(G1, G2):
    CSG = isomorphism.DiGraphMatcher(G1, G2)
    MCSG = {}
    if(CSG.subgraph_is_isomorphic()):
        #Find the max subgraph
        nodes = 0
        for G in CSG.subgraph_isomorphisms_iter():
            if len(G) > nodes:
                MCSG = G
                nodes = len(G)
    return MCSG 

'''
Given the list of malware graphs it searches for the biggest common isomorphic subgraph 
#FIXME: MCSG is no more a Graph!!!!!!!!!!!!!!!!!
'''   
def find_max_common_subgraph(DGs):
    MCSG = find_max_subgraph(DGs[1], DGs[2])   
    for DG in DGs[3:]:
        MCSG = find_max_subgraph(MCSG, DG)     
    return MCSG

'''
It checks if the application graph G has some subgraphs in common with the Common SubGraph CSG.
CSG is the biggest common subgraph of malware family X
'''
def check_common_subgraph_with_family_X(G, CSG):
    M = isomorphism.DiGraphMatcher(G, CSG)
    if(M.subgraph_is_isomorphic()):
        for mapping in M.subgraph_isomorphisms_iter():
            if(check_nodes_criteria(G, CSG, mapping) != 1 ):
                return 0
        else: 
            return 1
    else: 
        return 0
    
'''
Check for the number of graphs in G1 isomorph with malwares from family X (considering the threshold, a subgraph has to contain at least T nodes
in order to be considered as a match)
'''            
def check_number_of_matches_with_family_X(G1, family_X_list):            
    sample_counter = 0
    for GS in family_X_list:
        if(check_subgraph_isomorphism(G1, GS) > T):
            sample_counter+=1
    return sample_counter
          
            
            
            
            
            
            
            
            