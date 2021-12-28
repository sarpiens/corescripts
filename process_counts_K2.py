#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
process_counts_K2.py

"""


#Packages
from argparse import ArgumentParser
import os
import pandas as pd 


#Functions
def ls2(path): 
    return [obj.name for obj in os.scandir(path) if obj.is_file()]

def root_count(df):
    try:
        root=int(df[df[3]=='R'][1])
    except:
        root=0
    return root

def unclas_count(df):
    try:
        unclas=int(df[df[3]=='U'][1])
    except:
        unclas=0
    return unclas

def bact_count(df):
    """
    int(df[df[tax_id]==n][total_counts])
    """
    try:
        bact=int(df[df[4]==2][1])
    except:
        bact=0
    return bact

def arch_count(df):
    try:
        arch=int(df[df[4]==2157][1])
    except:
        arch=0
    return arch

def euk_count(df):
    try:
        euk=int(df[df[4]==2759][1])
    except:
        euk=0
    return euk

def virus_count(df):
    try:
        virus=int(df[df[4]==10239][1])
    except:
        virus=0
    return virus

def DOM_count(df):
    try:
        DOM=df[df[3]=='D'][1].sum()
    except:
        DOM=0
    return DOM

def PHY_count(df):
    try:
        PHY=df[df[3]=='P'][1].sum()
    except:
        PHY=0
    return PHY

def CLA_count(df):
    try:
        CLA=df[df[3]=='C'][1].sum()
    except:
        CLA=0
    return CLA

def ORD_count(df):
    try:
        ORD=df[df[3]=='O'][1].sum()
    except:
        ORD=0
    return ORD

def FAM_count(df):
    try:
        FAM=df[df[3]=='F'][1].sum()
    except:
        FAM=0
    return FAM

def GEN_count(df):
    try:
        GEN=df[df[3]=='G'][1].sum()
    except:
        GEN=0
    return GEN

def SP_count(df):
    try:
        SP=df[df[3]=='S'][1].sum()
    except:
        SP=0
    return SP

def main():
    #Setting Arguments
    parser = ArgumentParser()
    ##Parameter fasta file
    parser.add_argument(
            '--input_dir', '-i',
            dest='param1',
            action ='store',
            required =True,
            help='Path to de input directory.'
    )
    ##Parameter output file
    parser.add_argument(
            '--out_file', '-o',
            dest='param2',
            action ='store',
            required =True,
            help='Name of the output file.[With extension]'
    )
    #Process arguments
    args = parser.parse_args()
    input_direc=args.param1
    out_file_name=args.param2
    
    #Create empty data_frame
    out_df=pd.DataFrame(columns=['Sample_Name','R','U','Total','classify_reads_perc','Bact_count','Arch_count','Euk_count','Virus_count','Bacteria','Archaea','Eukaryota','Virus','DOM_count','PHY_count','CLA_count','ORD_count','FAM_count','GEN_count','SP_count','Domain','Phylum','Class','Order','Family','Genus','Species'])
    
    #Get list with report files
    direc_files=ls2(input_direc)
    report_files=[k for k in direc_files if '.report' in k]
    
    #Process each report file
    for report in report_files:
        #Get samples by name
        sample_name=report.split('.')[0]
        #Load file
        tabla=pd.read_csv(input_direc+'/'+report, sep='\t',header=None)
        #Get main stats
        root=root_count(tabla)
        unclas=unclas_count(tabla)
        total=root+unclas
        perc_clas=(root/total)*100
        #Get stats at domain level
        bact=bact_count(tabla)
        bact_perc=(bact/total)*100
        arch=arch_count(tabla)
        arch_perc=(arch/total)*100
        euk=euk_count(tabla)
        euk_perc=(euk/total)*100
        virus=virus_count(tabla)
        virus_perc=(virus/total)*100
        #Get general stats at domain level
        DOM=DOM_count(tabla)
        DOM_perc=(DOM/total)*100
        #Get general stats at Phylum level
        PHY=PHY_count(tabla)
        PHY_perc=(PHY/total)*100
        #Get general stats at Class level
        CLA=CLA_count(tabla)
        CLA_perc=(CLA/total)*100
	#Get general stats at Order level
        ORD=ORD_count(tabla)
        ORD_perc=(ORD/total)*100
        #Get general stats at family level
        FAM=FAM_count(tabla)
        FAM_perc=(FAM/total)*100
        #Get general stats at genus level
        GEN=GEN_count(tabla)
        GEN_perc=(GEN/total)*100
        #Get general stats at Sp level
        SP=SP_count(tabla)
        SP_perc=(SP/total)*100
        #Add line to data.frame
        line={'Sample_Name':sample_name,'R':root,'U':unclas,'Total':total,'classify_reads_perc':perc_clas,'Bact_count':bact,'Arch_count':arch,'Euk_count':euk,'Virus_count':virus,'Bacteria':bact_perc,'Archaea':arch_perc,'Eukaryota':euk_perc,'Virus':virus_perc,'DOM_count':DOM,'PHY_count':PHY,'CLA_count':CLA,'ORD_count':ORD,'FAM_count':FAM,'GEN_count':GEN,'SP_count':SP,'Domain':DOM_perc,'Phylum':PHY_perc,'Class':CLA_perc,'Order':ORD_perc,'Family':FAM_perc,'Genus':GEN_perc,'Species':SP_perc}
        out_df=out_df.append(line,ignore_index=True)
    
    #Save output file
    out_df.to_csv(out_file_name,header=True,index=False,sep='\t')

if __name__ == '__main__':
    main()    
