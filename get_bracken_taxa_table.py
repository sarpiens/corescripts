#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
get_taxa_names.py
"""
#Import Packages
import pandas as pd
from progress.bar import IncrementalBar
from argparse import ArgumentParser
import re


def main():
    #Setting Arguments
    parser = ArgumentParser()
    ##Parameter base headers file
    parser.add_argument(
            '--table_file', '-t',
            dest='param1',
            action ='store',
            required =True ,
            help='Name of the table counts file [With extension]'
    )
    ##Parameter enrichment file
    parser.add_argument(
            '--out_taxa_file', '-o',
            dest='param2',
            action ='store',
            required =True,
            help='Name of the output taxa file [With extension]'
    )
    ##Parameter output file
    parser.add_argument(
            '--level', '-l',
            dest='param3',
            action ='store',
            choices=['species','genus','family','order','class','phylum','superkingdom'],
            required =True,
            help='Taxonomy level of the table counts file'
    )
    #Process arguments
    args = parser.parse_args()
    name_file=args.param1
    out_file=args.param2
    start_level=args.param3
    
    #Load count table file and get tax names
    tabla=pd.read_csv(name_file,sep='\t',header=None,low_memory=False)
    t=tabla.T[0]
    
    #Load NCBI Taxonomy names.dmp
    names_file='names.dmp'
    names_table=pd.read_csv(names_file, header=None,sep="\t")
    print('Reading file...',names_file)
    #Get only scientific names
    names_table=names_table[names_table[6]=='scientific name']

    #Load NCBI Taxonomy nodes.dmp
    nodes_file='nodes.dmp'
    nodes_table=pd.read_csv(nodes_file, header=None,sep="\t")
    print('Reading file...',nodes_file)

    #Set tax levels of interest
    lista_levels=['species','genus','family','order','class','phylum','kingdom','superkingdom']
    
    #Open outfile
    outfile=open(out_file,'w')

    #Set header from start_level
    wanted_levels=lista_levels[lista_levels.index(start_level):len(lista_levels)]
    cabecera='\t'.join(wanted_levels)+'\n'
    outfile.write(cabecera)

    #Process lines
    bar=IncrementalBar('Processing', max=len(t)-1, suffix = '%(percent).1f%% - %(elapsed)ds')
    for n in range(1,len(t)):
        #Set lista_salida
        lista_salida=['NA']*len(wanted_levels)    
        #Get taxid /last parenthesis content
        tax_id=int(re.sub('^.*\((.*?)\)[^\(]*$', '\g<1>', t[n]))
        #Get full taxonomy
        while tax_id != 1:        
            tax_parent=nodes_table[nodes_table[0]==tax_id][2].values[0]
            tax_level=nodes_table[nodes_table[0]==tax_id][4].values[0]
            if tax_level in wanted_levels:
                #Get name
                name_t=names_table[names_table[0]==tax_id][2].values[0]
                tax_name=name_t+'('+str(tax_id)+')'
                #get index and save
                ind=wanted_levels.index(tax_level)
                lista_salida[ind]=tax_name
            #Fix new taxid
            tax_id=tax_parent
        #Save line in file
        line='\t'.join(lista_salida)+'\n'
        outfile.write(line)
        #next bar
        bar.next()
    #Close outfile
    outfile.close()
    #bar finish
    bar.finish()
    #Message
    print('Saving in file...',out_file)

if __name__ == '__main__':
    main()





