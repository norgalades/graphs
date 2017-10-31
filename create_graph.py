'''
Created on 23 Oct 2017

@author: mlecce
'''

import networkx as nx
import os
from format_input import parse_input_dir

#Inputs and variables
inputdir1 = "METASPLOIT"
#Format the input file so that it is possible to read the edges and write it to file output
#parse_input_dir(inputdir1)
inputdir1+="_PARSED"

DGs = list()

#Create the database with malware's graphs for a certain family 
sample_number=0
for filename in os.listdir(inputdir1):
    #Create a directed graph 
    DGs.append(nx.read_edgelist(inputdir1+"\\"+filename, create_using=nx.DiGraph()))
    #Read the edge list and populate the graph corresponding to sample_number
    sample_number+=1
    
#Print some information on the just read graph
print("Number of nodes in each graph\n")
i=1
for DG in DGs:
    print("Graph" + str(i))
    print(DG.number_of_nodes())
    i+=1
    edges = [e for e in DG.edges()]
    print(edges)


