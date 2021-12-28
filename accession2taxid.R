#Set parameters
arg=commandArgs(trailingOnly = TRUE)
file_name=arg[1]
out_name=arg[2]

#Load library
library(taxonomizr)

#Read file
accessions_input=read.csv(file_name, header = FALSE)
#Convert to vector
accessions=as.vector(t(accessions_input))
#Get taxids
taxids=accessionToTaxa(accessions,"accessionTaxa.sql")
#Create the results data.frame 
seq2tax=data.frame(accessions,taxids)
#Filter NAs in two objects
##Good to go Seq2taxid relationships 
correct=seq2tax[!is.na(seq2tax$taxids),]
print(paste("There are",as.character(nrow(correct)),"seq2taxid relationships"))
##Only NA(empty relationships)
NAs=seq2tax[is.na(seq2tax$taxids),]
print(paste("There are",as.character(nrow(NAs)),"empty seq2taxid relationships"))
#Save results
write.table(correct,file=paste(out_name,".txt",sep=''), sep ="\t", row.names=FALSE, col.names=FALSE, quote = FALSE)
write.table(NAs[1],file=paste(out_name,"_NA.txt",sep=''), sep ="\t", row.names=FALSE, col.names=FALSE, quote = FALSE)
