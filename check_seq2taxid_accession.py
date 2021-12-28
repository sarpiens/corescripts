#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
check_seq2taxid_accession.py

"""
from argparse import ArgumentParser
import pandas as pd

def main():
    #Setting Arguments
    parser = ArgumentParser()
    ##Parameter base headers file
    parser.add_argument(
            '--cab_file', '-c',
            dest='param1',
            action ='store',
            required =True ,
            help='Name of the headers accessions file (With txt extension).'
    )
    ##Parameter enrichment file
    parser.add_argument(
            '--raw_file', '-r',
            dest='param2',
            action ='store',
            required =True,
            help='Name of raw seqs2taxids file (With txt extension).'
    )
    ##Parameter output file
    parser.add_argument(
            '--out_name', '-o',
            dest='param3',
            action ='store',
            required =True,
            help='Name of the output file (With out extension).'
    )
    ##Parameter format
    parser.add_argument(
            '--format', '-f',
            dest='param4',
            action ='store',
            required =True,
            choices=['kraken2','centrifuge'],
            help='Format of the raw seqs2taxids file.'
    )
    #Process arguments
    args = parser.parse_args()
    cab_file=args.param1
    raw_file=args.param2
    out_file_name=args.param3
    formato=args.param4
    
    #Show description and message
    print(__doc__)

    #Loading seq2taxid raw file
    print('')
    print('Loading raw file ...')
    raw=pd.read_csv(raw_file,header=None,sep='\t')

    #Loading seq accessions file
    print('Loading cab file ...')
    cabeceras=pd.read_csv(cab_file,header=None)

    #Show info
    print('')
    print('Total accessions in raw file: ',len(raw))
    print('Total accessions in cab file: ',len(cabeceras))
    
    #Indicate format of the raw seq2taxid file
    if formato == 'kraken2':
        left=1
        inner='0_y'
        rt=2
    elif formato == 'centrifuge':
        left=0
        inner=0
        rt=1

    #inner join
    #2 Get common seq2taxid relationships raw&cab
    merged_inner=pd.merge(left=raw,right=cabeceras,left_on=left,right_on=0, how='inner')
    if formato == 'kraken2':
        #2 Remove last column
        result_inner=merged_inner.drop(columns=[inner])
    elif formato == 'centrifuge':
        result_inner=merged_inner
    #2 Show totals
    print('')
    print('Total common relationships in raw&cab files: ',len(result_inner))
    #2 Save result
    result_inner.to_csv(out_file_name+'_raw+cab.txt',sep='\t',header=False,index=False)

    #left join(if null)
    #2 Get accessions of raw seq2taxid file
    merged_left=pd.merge(left=raw,right=cabeceras,left_on=left,right_on=0, how='left')
    #2 Get those that are unique to the raw file
    result_left=merged_left[pd.isna(merged_left[inner])]
    #2 Show totals
    print('Total accessions unique to raw file: ',len(result_left))
    #2 Save result
    result_left.to_csv(out_file_name+'_raw_only.txt',sep='\t',header=False,index=False)

    #right join(if null)
    #2 Get accesions from seq accessions file(cab)
    merged_right=pd.merge(left=raw,right=cabeceras,left_on=left,right_on=0, how='right')
    #2 Get those that are unique to seq accessions file(cab)
    result_right=merged_right[pd.isna(merged_right[rt])][inner]
    #2 Show totals
    print('Total accessions unique to cab file: ',len(result_right))
    #2 Save result
    result_right.to_csv(out_file_name+'_cab_only.txt',sep='\t',header=False,index=False)

if __name__ == '__main__':
    main()



      
