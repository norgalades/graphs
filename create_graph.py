'''
Created on 23 Oct 2017

@author: mlecce
'''

###############################################################################################################################################
#                                                  Import section
#
###############################################################################################################################################

import networkx as nx
from networkx.algorithms import isomorphism
#import matplotlib.pyplot as plt
import os
from format_input import parse_input_dir
from max_sub_graph import *

###############################################################################################################################################
#                                                  Variable assignment
#
###############################################################################################################################################

#Inputs and variables
inputdir1 = "METASPLOIT"
#Format the input file so that it is possible to read the edges and write it to file output
parse_input_dir(inputdir1)
inputdir1+="_PARSED"

#List of all the malware directed graphs 
DGs = list()

###############################################################################################################################################
#                                                  Functions' section
#
###############################################################################################################################################

'''
This function searches for the node category on the AndroidManifesdt.xml file and assigns to each node one of the following categories:
# 1) activity
# 2) service
# 3) provider
# 4) receiver
# if no reference about the node it's found, it is probably because the node is an inner class of the translation to the Smali code. So: 
# 5) innerClass
'''
def check_node_component(G, file):
    #Open the corresponding AndroidManidest 
    with open(file, 'r') as fin:
        rows = fin.read().splitlines(True)
            
    #Take all the nodes contained on the graph G
    nodes = [n for n in G.nodes()]
    for n in nodes: 
        #For each node, search the component type and add it as attribute
        for row in rows:
            if n in row: 
                if "activity" in row:
                    d = {n : 'activity'}
                    nx.set_node_attributes(G, d, "compType")
                    break #step to next node
                elif "service" in row:
                    d = {n : 'service'}
                    nx.set_node_attributes(G, d, "compType")
                    break #step to next node
                elif "provider" in row:
                    d = {n : 'provider'}
                    nx.set_node_attributes(G, d, "compType")
                    break #step to next node
                elif "receiver" in row:
                    d = {n : 'receiver'}
                    nx.set_node_attributes(G, d, "compType")
                    break #step to next node
        else:
            d = {n : 'innerClass'}
            nx.set_node_attributes(G, d, "compType")
 
'''
This function creates the database with malware's graphs for a certain family 
'''            
def populate_list():
    sample_number=0
    for filename in os.listdir(inputdir1):
        #Create a directed graph 
        DGs.append(nx.read_edgelist(inputdir1+"\\"+filename, create_using=nx.DiGraph()))
        #Read the edge list and populate the graph corresponding to sample_number
        sample_number+=1
    
    check_node_component(DGs[2], "AndroidManifest_da5b.xml")
    check_node_component(DGs[1], "AndroidManifest_d109.xml")          
    check_node_component(DGs[0], "AndroidManifest_d109.xml")    
    
    #Print some information on the just read graph
    print("Number of nodes in each graph")
    i=1
    for DG in DGs:
        print("Graph" + str(i))
        print(DG.number_of_nodes())
        i+=1
        print_graph(DG)
        print("\n")

'''
This function prints how many matching criteria subgraphs were found between graph G and family X. 
Matching criteria subgraphs are isomorphism subgraphs with same node type for each corresponding couple of nodes
with a sufficient number of nodes (defined as a fixed threshold internal to the function)
'''            
def compare_with_family_X(G):
    n = check_number_of_matches_with_family_X(G, DGs)
    print("There are " + str(n) + " malwares in this family that matches your application!")
    
'''
To be completed
'''     
def search_the_exact_match(G):  
    #Print the max common subgraph of family X and the given graph G, if there is one
    CSG = find_max_common_subgraph(DGs) 
    if(check_common_subgraph_with_family_X(G, CSG) == 0):
        print("Empty graph")      
    #TODO
    
###############################################################################################################################################
#                                                  Main section
#
###############################################################################################################################################
   
#Read malware files and populate the list with their graphs       
populate_list()

#Read the graph of an application X 
G = nx.read_edgelist("adiacency_list.txt", create_using=nx.DiGraph())
print("Application graph:")
print_graph(G)

compare_with_family_X(G)
#check_subgraph_isomorphism(DGs[0], DGs[1])
#print_isomorphic_subgraphs(DGs[0], DGs[1])

