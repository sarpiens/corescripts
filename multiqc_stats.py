#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
multiqc_stats.py

"""

#Import moduls
import pandas as pd
from argparse import ArgumentParser

#Functions
def isNumeric(x):
    try:
        float(x)
        return True
    except ValueError:
        return False

#Main Program
def main():
    #Setting Arguments
    parser = ArgumentParser()
    ##Parameter Reference file
    parser.add_argument(
            '--input_file', '-i',
            dest='param1',
            action ='store',
            required =True,
            default='NULL',
            help='Input Data Path. Indicate rute to multiqc_data directory.'
    )
    ##Parameter out_file(TXT)
    parser.add_argument(
            '--output_name', '-o',
            dest='param2',
            action ='store',
            required =False ,
            default='./multiqc_total_stats',
            help='Output File Name.Indicate output file name[Without extension].'
    )
    #Process arguments
    args = parser.parse_args()
    input_path=args.param1
    output_name=args.param2
    
    #Prepare variables for Load files
    ##Process path
    if input_path.endswith('/'):
       input_path=input_path[:-1]
    ##Set path for taxonomy files
    stats_path=input_path+'/multiqc_fastqc.txt'
    
    #Try to load input file
    try:
        #Load multiqc_fastqc.txt file
        print('\nLoading Input Files...\n')
        stats=pd.read_csv(stats_path, sep='\t')
        
    except Exception as ex:
        print('The system returned the following exception: ', ex)
    else:
        
        #Get Max and Min lenghts per sample
        ##Set min and max list
        min_list=[]
        max_list=[]
        ##Iter rows for Sequence length column
        for i,r in stats.iterrows():
            ##Get temp info
            temp_seq_len=r['Sequence length']
            ##If/else
            if '-' in str(temp_seq_len):
                temp_min=temp_seq_len.split('-')[0]
                min_list.append(temp_min)
                temp_max=temp_seq_len.split('-')[1]
                max_list.append(temp_max)
            else:
                temp_min=temp_seq_len
                min_list.append(temp_min)
                temp_max=temp_seq_len
                max_list.append(temp_max)
        
        ##Convert list to integers
        min_list=[int(i) for i in min_list]
        max_list=[int(i) for i in max_list]
        
        #Iniciate output list
        output=[]
        #Get total stats
        min_length_total=min(min_list)
        max_length_total=max(max_list)
        seqs_total=stats['Total Sequences'].sum()
        seqs_total_mean=stats['Total Sequences'].mean()
        
        #Show total stats
        f11='Min length: '+str(min_length_total)
        f12='Max length: '+str(max_length_total)
        f2='Total seqs:'+str(seqs_total)
        f22='Total mean_seqs:'+str(seqs_total_mean)
        print(f11)
        print(f12)
        print(f2)
        print(f22)
        print('')
        #Append frases
        output.append(f11)
        output.append(f12)
        output.append(f2)
        output.append(f22)

        #Save all output stats
        with open (output_name+'.txt', 'w') as f: f.writelines('%s\n' %i for i in output)

if __name__ == '__main__':
    main()
