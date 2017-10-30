'''
Created on 30 Oct 2017

@author: mlecce
'''

import re

def input_formatter(filein, fileout):
    with open(filein, 'r') as fin:
        data = fin.read().splitlines(True)
    
    data2 = list()
    for s in data:
        #delete the first 11 and last 4 chars 
        s2 = s[11:-4]
        #match ","dest":" replace with space 
        s3 = re.sub(r"\",\"dest\":\"", " ", s2)
        data2.append(s3)
            
    #write on formatted output file without the first and the last row    
    with open(fileout, 'w') as fout:
        for s in data2[1:-1]:
            fout.write(s)
            fout.write("\n")
        
    fin.close()
    fout.close()