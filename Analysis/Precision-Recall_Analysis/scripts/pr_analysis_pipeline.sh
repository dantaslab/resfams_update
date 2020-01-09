#!/bin/bash
#===============================================================================
#
# File family  : pr_analysis_pipeline.sh
# Description  : run precision_recall analysis
# Parameters   : set database and date to desired outputs
#
# Author       : Max Bernstein, mabernstein@wustl.edu
# Version      : 1.0
# Created On   : 2019-12-18
#===============================================================================
#
#Submission script for HTCF
#SBATCH --job-name=pr_analysis
#SBATCH --nodes=1
#SBATCH --mem=8000M
#SBATCH -o prout.out # Standard output
#SBATCH -e prout.out # Standard error

root='/scratch/gdlab/mabernstein/project1/180216_prot_analysis/aro_rework/190702-family_analysis/ncbi/ncbi_tests/201006-pr_pipeline'
DB='/scratch/gdlab/mabernstein/project1/180216_prot_analysis/aro_rework/190702-family_analysis/ncbi/MB_hmms/v3-191212/191212-MB_Resfams.hmm'
blastDB='/scratch/gdlab/mabernstein/project1/180216_prot_analysis/aro_rework/190702-family_analysis/ncbi/MB_hmms/v3-191212/191212-MB_Resfams_sequences.fasta'
date='201007'


module load ncbi-blast
module list

cmd1="blastp -db ${blastDB} -query ${root}/d01-datasets/AMRProt.fasta -outfmt '6 qseqid sseqid pident evalue bitscore qcovs' -out ${root}/s02-ncbi/${date}-MBHmms_blast.txt"
echo "Command: $cmd1"
echo time $cmd1 | bash


module purge
module list


cmd2="python3 ${root}/scripts/blast_aro_parse_v01.py -f1 ${root}/s02-ncbi/${date}-MBHmms_blast.txt -o ${root}/s02-ncbi/${date}-MBHmms_blast_parsed.txt"
echo "Command: $cmd2"
echo time $cmd2 | bash


module load hmmer
module load py-biopython
module list


cmd3="hmmscan --cut_ga --tblout ${root}/s02-ncbi/${date}-MBHmms_hmmscan.txt ${DB} ${root}/d01-datasets/AMRProt.fasta"
echo "Command: $cmd3"
echo time $cmd3 | bash


cmd4="python3 ${root}/scripts/hmmscan_parse.py -i ${root}/s02-ncbi/${date}-MBHmms_hmmscan.txt -o ${root}/s02-ncbi/${date}-MBHmms_hmmscan_parsed.txt"
echo "Command: $cmd4"
echo time $cmd4 | bash


module purge
module list


cmd5="python3 ${root}/scripts/precision_recall_v01.py -f1 ${root}/s02-ncbi/${date}-MBHmms_hmmscan_parsed.txt -f2 ${root}/d01-datasets/MB_hmm_families.txt -m ${root}/s02-ncbi/${date}-MBHmms_blast_parsed.txt -d NCBI -o ${root}/s02-ncbi/${date}-MBHmms"
echo "Command: $cmd5"
echo time $cmd5 | bash





if [ $? -eq 0 ]
then
  echo "Job completed successfully"
else
  echo "Error Occured!"
fi
