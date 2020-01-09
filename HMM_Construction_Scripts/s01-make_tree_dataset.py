#!/usr/bin/env python

"""
File Name       : s01-make_tree_dataset.py
Author          : Max Bernstein
Created On      : 2019-07-12
Last Modified   : 2019-12-17
Description     : A program to prep and rename sequences in order to make tree
                  anlaysis easier

Dependencies    : py-biopython
Usage           : s01-make_tree_dataset.py --infile blactamA.fasta
                  --blast blactamA_card_blast.txt --family blactamA
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
    blast_file = args.blast


    #retrieve blast data
    seqInfo = {}
    for record in SeqIO.parse(infile,'fasta'):
        array=[]
        for hit in blast_file:
            if record.id == hit[0] and hit[1] not in array:
                array.append(hit[1])
        seqInfo[record.id] = array



    #renmane sequences
    seq_file = open("{}/{}_tree_dataset.faa".format(args.out_path,args.family), 'w+')
    mapping_file = open("{}/{}_tree_mappingFile.txt".format(args.out_path,args.family), 'w+')

    counter = 1
    for seq,data in seqInfo.items():
        outHeaders = []
        seqHeader = seq.split("|")
        outSeq = "RF-" + str(counter) + "|" + record.id
        bHitCount = 1
        for bData in data:
            outSeq = "RF-" + str(counter) + "-" + str(bHitCount) + "|" + seqHeader[-1] + "|" + bdata.split("|")[-1]
            outHeaders.append(outSeq)
            bHitCount+=1
        if len(outHeaders) < 1:
            outHeaders.append(outSeq)

        for header in outHeaders:
            print(header + "\t" + record.id)
            mapping_file.write(header + "\t" + record.id + "\n")
            seq_file.write(">" + header + "\n")
            seq_file.write(str(record.seq) + "\n")
        counter+=1





def parse_arguments(argv):
    parser = argparse.ArgumentParser(
        prog = 'make_tree_dataset.py',
        description = 'A program to prep and rename sequences in order to make tree anlaysis easier')

    parser.add_argument(
        '-i', '--infile',
        help = 'path to input sequences to make trees',
        required = True
    )
    parser.add_argument(
        '-b', '--blast',
        help = 'path to input blast file',
        required = True
    )
    parser.add_argument(
        '-f', '--family',
        help = 'assumed resistance family of input sequences',
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
