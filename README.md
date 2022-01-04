# corescripts
This repository contains scripts used for performing variuos processing steps and analysis presented in:

Piquer-Esteban, S., Ruiz-Ruiz, S., Arnau, V., Diaz, W., & Moya, A. (2021). Exploring the universal healthy human gut microbiota around the World. Computational and Structural Biotechnology Journal.https://doi.org/10.1016/j.csbj.2021.12.035

# 1.Scripts used in Databases construction: 
filterN_seqs.sh, accession2taxid.R and check_seq2taxid_accession.py; A detailed description can be found in the supplementary material of the publication.

# 2.multiqc_stats.py
Script used to generate some qc stats from multiqc reports.

# 3.process_counts_K2.py
Script used to generate specific taxon counts of interest from Kraken2 reports for databases comparison.

# 4.process_counts_Bracken.py
Script used to generate the corresponding count table from the Bracken reports.

# 5.get_bracken_taxa_table.py
Script to generate taxonomy table from bracken count table using NCBI Taxonomy.

# 6.DB_comparative.Rmd
Script for comparison of genome databases and figures creation.

# 7.Microbiome_analysis_genus.Rmd
Script for analysis at genus level and figures creation.

# 8.Microbiome_analysis_sp.Rmd
Script for analysis at species level and figures creation.
