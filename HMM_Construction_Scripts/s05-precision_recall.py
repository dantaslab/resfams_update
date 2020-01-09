#!/usr/bin/env python
"""
File Name       : precision_recall.py
Author          : Max Bernstein
Created On      : 2018-02-18
Last Modified   : 2019-12-17
Description     : A program for acessing precision and recall of hmms.
                  Utilizes hmmscan ouptut along with a currated metadata file.

Dependencies    :
Usage           : precision_recall.py --infile testing_set_hmmscan_parsed.txt
                  --family_file blactamA_families.txt --metadata
                  blactamA_mapping.txt --dtype test_dataset_1
                  --output path/to/output/directory
CHANGE LOG      :
TODO            :

"""

import sys
import os
import argparse
import csv
import re
import ast


def main(argv):
    args = parse_arguments(argv)

    infile = args.infile
    family_file = args.family_file
    meta = args.metadata


    #Initialize output files
    out = open("{}/pr_analysis.txt".format(args.output), 'w+')
    fpout=open("{}/fplist.txt".format(args.output),'w+')

    if args.dtype is not None:
        dtype = args.dtype
        out.write("DATASET: {}\n".format(dtype))
        fpout.write(dtype + ":\n")

    out.write("Family\tTrue_Pos\tRes_hits\tRel_Seqs\tPrecision\tRecall\n")
    fpout.write("Seq_Header\tHmmscan_Family\n")




    #parse input dataset
    data = []
    with open(infile) as f1:
        reader1 = csv.reader(f1, delimiter='\t')
        for row in reader1:
            # print(row)
            data.append(row)

    metadata = []
    seq_meta = []
    with open(meta) as m:
        reader2 = csv.reader(m, delimiter='\t')
        for row in reader2:
            if row[0] not in seq_meta:
                # print(row)
                metadata.append(row)
                seq_meta.append(row[0])

    families = []
    with open(family_file) as f2:
        reader3 = csv.reader(f2, delimiter='\t')
        for row in reader3:
            # print(row)
            families.append(row)



    ##Find Hits and count True Positives
    for fam in families:
        hit_count = 0
        tp_count = 0
        seq_count = 0
        family = fam[0]

        dbFamList = []
        for seq in metadata:
            if len(seq) > 1:
                if len(seq) > 2:
                    dbFam = [seq[1],seq[2]]
                else:
                    dbFam = [seq[1]]
                if family in dbFam:
                    seq_count+=1
                    dbFamList.append(seq[0])

        seqlist=[]
        tplist=[]

        for hit in data:
            check = tp_count
            hitseq = hit[2]
            hitfam = hit[1]
            if hitseq not in seqlist:
                if hitfam == family:
                    hit_count += 1
                    # seqlist.append(hit[2])
                    for seq in metadata:
                        metaseq = seq[0]
                        if len(seq) > 1:
                            if len(seq) > 2:
                                dbFam = [seq[1],seq[2]]
                            else:
                                dbFam = [seq[1]]
                            if hitseq == metaseq:
                                if hitfam in dbFam:
                                    tp_count+=1
                                    if hitseq not in tplist:
                                        tplist.append(hitseq)




        ##Calculate Precision and Recall
        if hit_count >0:
            precision = tp_count/hit_count
        else:
            precision = "N/A"

        if seq_count >0:
            recall = tp_count/seq_count
        else:
            recall = "N/A"


        #print outputs
        print(family + " -->")
        print("\tPrecision = " + str(tp_count) + "/" + str(hit_count)+ " = " + str(precision))
        print("\tRecall = " + str(tp_count) + "/" + str(seq_count) + " = " + str(recall))
        out.write(family + "\t" + str(tp_count) + "\t" + str(hit_count) + "\t" + str(seq_count) + "\t" + str(precision) + "\t" + str(recall) + "\n")


        #list sequences where there were false positives against hmms
        for hit in data:
            if hit[1] == family:
                if hit[2] not in tplist:
                    fpout.write("{}\t{}\n".format(hit[2],hit[1]))



    fpout.close()
    out.close()









def parse_arguments(argv):
    parser = argparse.ArgumentParser(
        prog = 'precision_recall.py',
        description = 'A program for acessing precision and recall of hmms. \n Utilizes hmmscan ouptut along with a currated metadata file.')
    parser.add_argument(
        '-i', '--infile',
        help = 'Enter parsed hmmscan output file',
        required = True
        )
    parser.add_argument(
        '-f', '--family_file',
        help = 'Enter file of families to be test',
        required = True
        )
    parser.add_argument(
        '-m', '--metadata',
        help = 'Enter metadata file',
        required = True
        )
    parser.add_argument(
        '-d', '--dtype',
        help = 'dataset name for extra information purposes.',
    )
    parser.add_argument(
        '-o', '--output',
        help = 'Enter path to output directory',
        required = True
        )

    return parser.parse_args()





if __name__=="__main__":
    main(sys.argv[1:])
