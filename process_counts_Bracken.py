#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
process_counts_Bracken.py
"""

#Import Packages
from argparse import ArgumentParser
import os, sys
import pandas as pd

def ls2_paths(path): 
    return [os.path.join(f) for f in os.scandir(path)]

def main():

    #Setting Arguments
    parser = ArgumentParser()
    ##Parameter fasta file
    parser.add_argument(
            '--input_dir', '-i',
            dest='param1',
            action ='store',
            required =True,
            help='Path to de input directory'
    )
    ##Parameter output file
    parser.add_argument(
            '--out_file', '-o',
            dest='param2',
            action ='store',
            required =True,
            help='Name of the output file.[With out extension]'
    )
    #Process arguments
    args = parser.parse_args()
    input_direc=args.param1
    out_file_name=args.param2
    
    #Get paths list for the directory files
    files_paths=ls2_paths(input_direc)
    report_paths=[k for k in files_paths if '.bracken' in k]
    
    #Set init variables
    names_list=[]
    counts_dicts=[]
    props_dicts=[]
    levels_list=[]    
    
    #Process each file
    for file in report_paths:
        #Get name and save
        temp_name=file.split('/')[-1].replace('.bracken','')
        names_list.append(temp_name)
        #Print update
        sys.stdout.write("Processing File: " + temp_name + '\n')
        #Read file
        temp_file=open(file,'r')
        lines=temp_file.readlines()
        #Check header
        if lines[0] != 'name\ttaxonomy_id\ttaxonomy_lvl\tkraken_assigned_reads\tadded_reads\tnew_est_reads\tfraction_total_reads\n':
            sys.exit("This file header does not match the spected header for a bracken output file")
        else:
            #Set init variables
            tax_levels=[]
            names_with_taxids=[]
            counts=[]
            props=[]
            temp_count_dict={}
            temp_prop_dict={}
            #Process each line
            for line in lines[1:len(lines)]:
                #Get info
                ##Combine name to taxid
                name=line.split('\t')[0]
                tax_id=line.split('\t')[1]
                name_w_tax=name+'('+str(tax_id)+')'
                names_with_taxids.append(name_w_tax)
                ##Get tax level
                level=line.split('\t')[2]
                tax_levels.append(level)
                ##Get count
                count=line.split('\t')[5]
                counts.append(count)
                ##Get prop
                prop=line.split('\t')[6].replace('\n','')
                props.append(prop)
            #Check Taxonomy levels
            uniq_levels=list(dict.fromkeys(tax_levels))
            if len(uniq_levels) != 1:
                sys.exit("Taxonomy level not matching between taxons for sample "+ temp_name)
            else:
                #Add de sample taxon level
                levels_list.append(uniq_levels[0])
                #Create dictionaries and sabe them
                temp_count_dict=dict(zip(names_with_taxids,counts))
                counts_dicts.append(temp_count_dict)
                temp_prop_dict=dict(zip(names_with_taxids,props))
                props_dicts.append(temp_prop_dict)
    
    #Merge info
    #Check that all samples have the same taxonomy level
    uniq_sample_levels=list(dict.fromkeys(levels_list))
    if len(uniq_sample_levels) != 1:
        sys.exit("Taxonomy level not matching between samples")
    else:
        #Get count tables
        conteos=pd.DataFrame(counts_dicts)
        conteos=conteos.fillna(0)
        conteos.insert(0,'run_accession',names_list)
        conteos.to_csv(out_file_name+'_count_bracken.txt',header=True,index=False,sep='\t')
    
if __name__ == '__main__':
    main()  
