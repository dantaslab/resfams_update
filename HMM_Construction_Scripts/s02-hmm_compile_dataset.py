#!/usr/bin/env python


"""
File Name       : hmm_compile_dataset.py
Author          : Max Bernstein
Created On      : 2019-07-13
Last Modified   : 2019-12-17
Description     : A program to compile family hmm seqs from tree manually
                  curated mapping file

Dependencies    : py-biopython
Usage           : hmm_compile_dataset.py --infile blactamA_tree_dataset.fasta
                  --map blactamA_tree_mappingFile.txt --species CblA
                  --out_path path/to/output/directory/
CHANGE LOG      :
TODO            :

"""

import sys
import os
import argparse
import csv
import re

from Bio import SeqIO


def main(argv):
    args = parse_arguments(argv)

    infile = args.infile
    map = args.map
    species = args.species

    seq_file = open("{}/{}_hmm_seqs.faa".format(args.out_path,species), 'w+')

    outSeqs=[]
    for record in SeqIO.parse(infile,'fasta'):
        header = record.id
        with open(map) as m:
            reader = csv.reader(m,delimiter='\t')
            for row in reader:
                seqHead = row[1]
                if len(row) > 2:
                    for family in row[2:]
                        if header == row[0] and species == family and seqHead not in outSeqs:
                            print(seqHead)
                            seq_file.write(">" + seqHead + "\n")
                            seq_file.write(str(record.seq) + "\n")
                            outSeqs.add(seqHead)





def parse_arguments(argv):
    parser = argparse.ArgumentParser(
        prog = 'hmm_compile_dataset.py',
        description = 'A program to compile family hmm seqs from tree manually curated mapping file')

    parser.add_argument(
        '-i', '--infile',
        help = 'tree dataset fasta file with modified headers',
        required = True
    )
    parser.add_argument(
        '-m', '--map',
        help = 'path to inpute tree mapping file. Format: \n column1 = tree header \n column2 = original sequence header \n column3 and greater = tree families',
        required = True
    )
    parser.add_argument(
        '-s', '--species',
        help = 'species',
        required = True
    )
    parser.add_argument(
        '-o', '-outpath',
        dest = 'out_path',
        help = 'Enter path to output directory'
    )
    return parser.parse_args()





if __name__=="__main__":
    main(sys.argv[1:])
