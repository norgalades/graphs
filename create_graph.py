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
#parse_input_dir(inputdir1)
inputdir1+="_PARSED"

DGs = list()

###############################################################################################################################################
#                                                  functions' section
#
###############################################################################################################################################

#This function searches for the node category on the AndroidManifesdt.xml file and assigns to each node one of the following categories:
# 1) activity
# 2) service
# 3) provider
# 4) receiver
# if no reference about the node it's found, it is probably because the node is an inner class of the translation to the Smili code. So: 
# 5) innerClass
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

#This function searches for the edge category on the AndroidManifesdt.xml file and assigns to each of them one of the following categories:     
#TODO       
def check_edge_component(G, file):
    #Open the corresponding AndroidManidest 
    with open(file, 'r') as fin:
        rows = fin.read().splitlines(True)
          
###############################################################################################################################################
#                                                  Main section
#
###############################################################################################################################################
            
#Create the database with malware's graphs for a certain family 
sample_number=0
for filename in os.listdir(inputdir1):
    #Create a directed graph 
    DGs.append(nx.read_edgelist(inputdir1+"\\"+filename, create_using=nx.DiGraph()))
    #Read the edge list and populate the graph corresponding to sample_number
    sample_number+=1

check_node_component(DGs[1], "AndroidManifest_d109.xml")          
check_node_component(DGs[0], "AndroidManifest_d109.xml")    

#Print some information on the just read graph
print("Number of nodes in each graph")
i=1
for DG in DGs:
    print("Graph" + str(i))
    print(DG.number_of_nodes())
    i+=1
    nodes = [n for n in DG.nodes()]
    compTypes = nx.get_node_attributes(DG, "compType")
    for node in nodes: 
        if(compTypes[node] != "innerClass"):
            print(node + ": " + compTypes[node])
            for nb in nx.all_neighbors(DG, node): 
                print(nb)
            print("\n")
    #edges = [e for e in DG.edges()]
    #print(edges)
    
    print("\n")

check_subgraph_isomorphism(DGs[0], DGs[1])
print_isomorphic_subgraphs(DGs[0], DGs[1])

