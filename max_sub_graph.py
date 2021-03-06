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
T = 1 
DGs = list()

###############################################################################################################################################
#                                                  Functions' section
#
###############################################################################################################################################

def print_graph(G):
    nodes = [n for n in G.nodes()]
    compTypes = nx.get_node_attributes(G, "compType")
    neighbors = []
    for node in nodes: 
        #Find all the neighbors: the functions returns predecessors as well as successors
        neighbors = nx.all_neighbors(G, node)
        filtered_neighbors = set(neighbors)
        #print(node + ": " + compTypes[node])
        print(node + " type: " + compTypes[node] + " neighbors: ")
        for nb in filtered_neighbors: 
            print(nb)
        print("\n")

def print_subgraph(G):
    nodes = [n for n in G.nodes()]
    neighbors = []
    for node in nodes: 
        neighbors = nx.all_neighbors(G, node)
        filtered_neighbors = set(neighbors)
        print(node + " neighbors: ")
        for nb in filtered_neighbors: 
            print(nb)
        print("\n")

def check_isomorphism(G1, G2):
    GM = isomorphism.DiGraphMatcher(G1, G2)
    if(GM.is_isomorphic()):
        print("The two graphs are isomorphic!")  
    else: 
        print("The two graphs are not isomorphic!")

'''
This function builds the graph starting from the mapping. Therefore, it saves the mapping between a subgraph and the application_under_analysis as a group of nodes and edges connecting them, then stores it in the list of subgraphs DGs 
'''        
def save_sub_graph(G, mapping, b):
    DG = nx.DiGraph()
    #Add all the nodes in the subgraph
    if b :
        for key , value in mapping.items():
            DG.add_node(key)
    else:
        for key , value in mapping.items():
            DG.add_node(value)
    #For all the edges of G connect the nodes in the subgraph
    for (u, v) in G.edges():
        if DG.has_node(u) and DG.has_node(v):
            DG.add_edge(u, v)
    DGs.append(DG)

def compute_signature():
    Sig = nx.DiGraph()
    for G in DGs:
        for (u, v) in G.edges():
            if G.has_edge(u, v) == False:
                Sig.add_edge(u, v, weight=1)
            else: 
                Sig.edge[u][v]['weight'] += 1
    print("Signature: ")
    for n,nbrs in Sig.adjacency():
        for nbr,eattr in nbrs.items():
            data=eattr['weight']
            print('(%s, %s, %d)' % (n,nbr,data)) 

'''
This function checks if there is any subgraph in G1 that is isomorph to the whole G2, and returns the number of nodes of the biggest subgraph matching G2 (if any). The boolean b indicates if the application_under_analysis is G1 or G2 (according to how this function has been called by check_number_of_matches_with_family_X)
'''        
def check_subgraph_isomorphism(G1, G2, b):
    GM = isomorphism.DiGraphMatcher(G1, G2)
    if(GM.subgraph_is_isomorphic()):
        nodes = [0]
        #An iterator of the type: nodeA_in_G1 : nodeA_prime_in_G2 over all the subgraphs that match G2
        print("All subgraphs of " + str(G1.graph['name']) + " matching " + str(G2.graph['name']) + " :")
        for G in GM.subgraph_isomorphisms_iter():
            if(check_nodes_criteria(G1, G2, G) == 1 ):
                #Save the subgraph 
                if b : 
                    save_sub_graph(G1, G, b)
                else:
                    save_sub_graph(G2, G, b)
                print("Subgraph: \n")
                print(G)
                print("\n")
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
    for key , value in mapping.items():
        if (node_types1[key] != node_types2[value]):
            return 0
        else:
            print(key + ": "+ node_types1[key] + ", " + value + ": " + node_types2[value])
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
Check for the number of graphs in G1 isomorph with malwares from family X (considering the threshold, a subgraph has to contain at least T nodes in order to be considered as a match). NB. The second parameter for the check_subgraph_isomorphism function has to be the smallest graph since the VF2 algorithm checks for any isomorphic subgraph in the first passed graph matching the whole second passed graph
'''            
def check_number_of_matches_with_family_X(G1, family_X_list):            
    sample_counter = 0
    for GS in family_X_list:
        if(G1.number_of_nodes() > GS.number_of_nodes()):
            if((check_subgraph_isomorphism(G1, GS, True) > T)):
                sample_counter+=1
        else:
            if((check_subgraph_isomorphism(GS, G1, False) > T)):
                sample_counter+=1
    compute_signature()
    return sample_counter
          
            
            
            
            
            
            
            
            
