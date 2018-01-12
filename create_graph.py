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
import sys
from format_input import parse_input_dir
from max_sub_graph import *

###############################################################################################################################################
#                                                  Variable assignment
#
###############################################################################################################################################

#Inputs and variables
inputdir1 = "SYRINGE"
inputdir2 = "SYRINGE_MANIFESTS"

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
    for filename in os.listdir(inputdir1):
        #Create a directed graph 
        DGs.append(nx.read_edgelist(inputdir1+"/"+filename, create_using=nx.DiGraph()))
        DGs[-1].graph['name'] = filename[:-7]
        check_node_component(DGs[-1], inputdir2+"/"+os.path.splitext(filename)[0])
    
    '''    
    #Print some information on the just read graph

    for DG in DGs:
        print("Graph name: " + str(DG.graph['name']))
        print(DG.number_of_nodes())
        print_graph(DG)
        print("\n")
    '''

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

#Redirects the prints to a file
sys.stdout = open('output.txt','wt')

#Format the input file so that it is possible to read the edges and write it to file output
#parse_input_dir(inputdir1)
inputdir1+="_PARSED"
   
#Read malware files and populate the list with their graphs       
populate_list()

#Read the graph of an application X 
G = nx.read_edgelist("f29fcd749f5e1b4e701e2359fe12a0ac2a5927a37b1eb5b4e308de39e4dc95f4.txt", create_using=nx.DiGraph())
G.graph['name'] = "app_under_analysis"
check_node_component(G, "f29fcd749f5e1b4e701e2359fe12a0ac2a5927a37b1eb5b4e308de39e4dc95f4")
print("Application graph:")
#print_graph(G)
print("Number of nodes:")
print(G.number_of_nodes())

compare_with_family_X(G)
#check_subgraph_isomorphism(G, DGs[11])
#print_isomorphic_subgraphs(DGs[0], DGs[1])

