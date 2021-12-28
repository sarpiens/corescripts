#!/bin/bash

#Read input parameters
while getopts p:i:o: flag
do
    case "${flag}" in
        p) reformat=${OPTARG};;
        i) IN_FILE=${OPTARG};;
        o) OUT_FILE=${OPTARG};;
    esac
done

#Set temp file in current directory
TEMP_FILE="./temp_file.fa"

#Step1/NFilter
##Filter 100%N sequences in the input file
cat $IN_FILE | awk '/^>/ {printf("\n%s\n",$0);next; } { printf("%s",$0);}  END {printf("\n");}' | sed '/^ *$/d' | paste - - | awk -F '\t' '{S=$2;L=gsub(/N/,"",S);L2=length($2); if (L/L2 < 1.0) print $0}' | tr "\t" "\n" >> $TEMP_FILE
##Show Message
echo '100%N Sequences filtered. Done.'

#Step2/ Reformat
##Reformat fasta file to W60 using the reformat.sh script from BBTools Suite
$reformat in=$TEMP_FILE out=$OUT_FILE fastawrap=60
##Show Message
echo 'Reformat to W60. Done.'

#Step3/ Remove temp file
##Remove temp file
rm $TEMP_FILE
##Final Message
echo 'Final script.Done.'
