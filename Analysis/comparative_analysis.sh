#!/bin/bash
#===============================================================================
#
# File family  : comparative_analysis.sh
# Description  : run comparative analysis between different dbs
# Parameters   : set database and date to desired outputs
#
# Author       : Max Bernstein, mabernstein@wustl.edu
# Version      : 1.0
# Created On   : 2019-12-18
#===============================================================================
#
#Submission script for HTCF
#SBATCH --job-name=compAnalysis
#SBATCH --nodes=1
#SBATCH --array=1-5%5
#SBATCH --mem=8000M
#SBATCH -o logfiles/compA_%a.out # Standard output
#SBATCH -e logfiles/compA_%a.out # Standard error

root='/scratch/gdlab/mabernstein/project1/180216_prot_analysis/aro_rework/190702-family_analysis/ncbi/ncbi_tests/191218-pr_comp_analysis_2'
date='191218'
method=`sed -n ${SLURM_ARRAY_TASK_ID}p ${root}/d01-datasets/analysis_methods.txt`
declare -a datasets=("card" "megares" "fxnl_complete")
meta="${root}/d01-datasets/${method}_families.txt"

if [ $method == "MBhmms" ]; then
  DB='/scratch/gdlab/mabernstein/project1/180216_prot_analysis/aro_rework/190702-family_analysis/ncbi/MB_hmms/v3-191212/191212-MB_Resfams.hmm'
  meta="${root}/d01-datasets/MBhmms_families.txt"
  rm ${root}/${date}-hitCounts.txt
elif [ $method == "resfams_core" ]; then
  DB='/scratch/ref/gdlab/hmm/Resfams/latest/ResFams-only.hmm'
  meta="${root}/d01-datasets/resfams_families.txt"
elif [ $method == "resfams_full" ]; then
  DB='/scratch/ref/gdlab/hmm/Resfams/latest/ResFams.hmm'
  meta="${root}/d01-datasets/resfams_families.txt"
elif [ $method == "ncbi" ]; then
  DB='/scratch/gdlab/mabernstein/project1/180216_prot_analysis/aro_rework/190702-family_analysis/ncbi/ncbi_hmm/NCBI_amrfinder.hmm'
  meta="${root}/d01-datasets/ncbi_families.txt"
fi
echo ${DB}



module purge
module load cdhit
module load hmmer
module load py-biopython
module load amrfinder
module list

echo e0${SLURM_ARRAY_TASK_ID}-${method}

rm ${root}/e0${SLURM_ARRAY_TASK_ID}-${method}/${date}-${method}-hitCounts.txt

for i in "${datasets[@]}"
do
   echo "$i"

   cmd1="cd-hit -i ${root}/d01-datasets/full_datasets/${i}_protseqs.faa -o ${root}/d01-datasets/${date}-${i}_cdhit.faa -c 1"
   echo "Command: $cmd1"
   echo time $cmd1 | bash

   if [ $method == 'amrfinder' ]; then
      cmd2="amrfinder --protein ${root}/d01-datasets/${date}-${i}_cdhit.faa --output ${root}/e0${SLURM_ARRAY_TASK_ID}-${method}/${date}-${method}-${i}_hmmscan.txt"
      echo "Command: $cmd2"
      echo time $cmd2 | bash

      cmd3="python3 ${root}/scripts/amrfinder_parse.py -f1 ${root}/e0${SLURM_ARRAY_TASK_ID}-${method}/${date}-${method}-${i}_hmmscan.txt -m ${root}/d01-datasets/ncbi_families2.txt -o ${root}/e0${SLURM_ARRAY_TASK_ID}-${method}/${date}-${method}-${i}_hmmscan_parsed.txt"
      echo "Command: $cmd3"
      echo time $cmd3 | bash

   else

     # if [ $method == "resfams_core" ] || [ $method == "resfams_full" ]; then
     #   meta="${root}/d01-datasets/resfams_families.txt"
     # fi

     cmd2="hmmscan --cut_ga --tblout ${root}/e0${SLURM_ARRAY_TASK_ID}-${method}/${date}-${method}-${i}_hmmscan.txt ${DB} ${root}/d01-datasets/${date}-${i}_cdhit.faa"
     echo "Command: $cmd2"
     echo time $cmd2 | bash

     cmd3="python3 ${root}/scripts/hmmscan_parse.py -f1 ${root}/e0${SLURM_ARRAY_TASK_ID}-${method}/${date}-${method}-${i}_hmmscan.txt -m ${meta} -o ${root}/e0${SLURM_ARRAY_TASK_ID}-${method}/${date}-${method}-${i}_hmmscan_parsed.txt"
     echo "Command: $cmd3"
     echo time $cmd3 | bash
   fi

   cmd4="python3 ${root}/scripts/hmmscan_count.py -f1 ${root}/e0${SLURM_ARRAY_TASK_ID}-${method}/${date}-${method}-${i}_hmmscan_parsed.txt -ds ${i} -db ${method} -o ${root}/e0${SLURM_ARRAY_TASK_ID}-${method}/${date}-${method}-hitCounts.txt"
   echo "Command: $cmd4"
   echo time $cmd4 | bash
done


cmd5="cat ${root}/e0${SLURM_ARRAY_TASK_ID}-${method}/${date}-${method}-hitCounts.txt >> ${root}/${date}-hitCounts.txt"
echo "Command: $cmd5"
echo time $cmd5 | bash



if [ $? -eq 0 ]
then
  echo "Job completed successfully"
else
  echo "Error Occured!"
fi
