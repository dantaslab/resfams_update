#!/usr/bin/env python
"""
File Name       : precision_recall.py
Author          : Max Bernstein
Created On      : 2018-04-11
Last Modified   : 2019-12-17
Description     : A program to parse an hmmscan output

Dependencies    :py-biopython
Usage           : hmmscan_parse.py --infile testing_set_hmmscan.txt
                  --out_path testing_set_hmmscan_parsed.txt
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

    file1 = args.file1
    file2 = args.file2
    meta = args.metadata

    if args.dtype is not None:
        dtype = args.dtype
        out = open("{}_pr_analysis.txt".format(args.output), 'w+')
        out.write("DATASET: {}\n".format(dtype))
        out.write("Family\tTrue_Pos\tRes_hits\tRel_Seqs\tPrecision\tRecall\n")

        col = "1"
        if dtype == "HMM_Seqs":
            col = 1
        elif dtype == "CARD_Seqs":
            col = 2
        elif dtype == "RES_Seqs":
            col = 3

    else:
        out = open("{}_pr_analysis.txt".format(args.output), 'w+')
        out.write("Family\tTrue_Pos\tRes_hits\tRel_Seqs\tPrecision\tRecall\n")

    fpout=open("{}_fplist.txt".format(args.output),'w+')
    fpout.write(dtype + ":\n")
    fpout.write("Seq_Header\tHmmscan_Family\n")
    nhout=open("{}_nhlist.txt".format(args.output),'w+')
    nhout.write(dtype + ":\n")
    nhout.write("Seq_Header\tHmmscan_Family\n")




    data = []
    with open(file1) as f1:
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
    with open(file2) as f2:
        reader3 = csv.reader(f2, delimiter='\t')
        for row in reader3:
            # print(row)
            families.append(row)


    ##Find Hits
    for fam in families:
        hit_count = 0
        tp_count = 0
        seq_count = 0
        rfid = fam[0]
        family = fam[1]

        dbFamList = []
        for seq in metadata:
            dbFam = seq[1].split("|")
            if rfid in dbFam:
                seq_count+=1
                dbFamList.append(seq[0])

        tplist=[]

        for hit in data:
            check = tp_count
            hitseq = hit[2]
            hitfam = hit[1]
            hitID = hit[0]

            if hitID == rfid:
                hit_count += 1
                for seq in metadata:
                    metaseq = seq[0]
                    dbFam = seq[1].split("|")
                    if hitseq == metaseq:
                        if hitID in dbFam:
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


        print(rfid + ": " + family + " -->")
        print("\tPrecision = " + str(tp_count) + "/" + str(hit_count)+ " = " + str(precision))
        print("\tRecall = " + str(tp_count) + "/" + str(seq_count) + " = " + str(recall))

        out.write(family + "\t" + str(tp_count) + "\t" + str(hit_count) + "\t" + str(seq_count) + "\t" + str(precision) + "\t" + str(recall) + "\n")



        for seq in dbFamList:
            if seq not in tplist:
                nhout.write("{}\t{}\t{}\n".format(seq,family,rfid))

        for hit in data:
            if hit[0] == rfid:
                if hit[2] not in tplist:
                    fpout.write("{}\t{}\t{}\n".format(hit[2],hit[1],hit[0]))



    fpout.close()
    nhout.close()
    out.close()









def parse_arguments(argv):
    parser = argparse.ArgumentParser(
        prog = 'precision_recall.py',
        description = 'A program for acessing precision and recall of hmms. \n Utilizes hmmscan ouptut along with a currated metadata file.')
    parser.add_argument(
        '-f1', '--file1',
        help = 'Enter parsed hmmscan output file',
        required = True
        )
    parser.add_argument(
        '-f2', '--file2',
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
        help = 'dataset type for Extra information purposes.',
    )
    parser.add_argument(
        '-o', '--output',
        help = 'Enter path to output file',
        required = True
        )

    return parser.parse_args()





if __name__=="__main__":
    main(sys.argv[1:])
