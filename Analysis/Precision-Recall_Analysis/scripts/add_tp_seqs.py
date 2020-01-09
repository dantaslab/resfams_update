import sys
import os
import pandas as pd
import csv
import argparse
from collections import OrderedDict
from io import StringIO


def main(argv):
    args = parse_arguments(argv)
    out = args.out_path
    file1 = args.file1
    file2 = args.file2
    file3 = args.file3


    ddf1 = addSeqs(file1,file2)
    ddf2 = removeSeqs(ddf1,file3)


    with open(out, 'w+') as output:
        for row in ddf2:
            print("\t".join(row))
            output.write("\t".join(row)+"\n")


def parse_arguments(argv):
    parser = argparse.ArgumentParser(
        prog = 'mapping.py',
        description = 'A program to map two files (csv of txt) to each other')
    parser.add_argument(
        '-f1', '--file1',
        help = 'Enter first file.',
        required = True
    )
    parser.add_argument(
        '-f2', '--file2',
        help = 'Enter fplist file.',
        required = True
    )
    parser.add_argument(
        '-f3', '--file3',
        help = 'Enter nhlist file.',
        required = True
    )
    parser.add_argument(
        '-o', '-outpath',
        dest = 'out_path',
        help = 'Enter path to dropped seqs file'
    )

    return parser.parse_args()


def addSeqs(file1, file2):
    df1 = pd.read_table(file1, sep="\t", names=['seq_name','dbID'])

    df2 = pd.read_table(file2, sep="\t", skiprows=2, usecols=[0,2], names=['seq_name','dbID'])


    ddf = pd.concat([df1,df2])
    ddf = ddf.groupby('seq_name')['dbID'].apply(list).map(set).str.join('|')
    ddf = ddf.reset_index()
    print(ddf.head())

    return ddf


def removeSeqs(ddf1, file3):

    data = ddf1.values.tolist()

    nhlist = []
    with open(file3) as f3:
        reader = csv.reader(f3, delimiter='\t')
        next(reader, None)
        next(reader, None)
        for row in reader:
            # print(row)
            nhlist.append(row)


    ddf2 = []
    for row in data:
        if row[1] != None:
            rfids = str(row[1]).split("|")
        else:
            rfids = []


        for seq in nhlist:
            id = seq[2]

            if row[0] == seq[0]:
                for rfid in rfids:
                    if id == rfid:
                        rfids.remove(id)

        array = [row[0],"|".join(rfids)]
        ddf2.append(array)

    return ddf2





if __name__=="__main__":
    main(sys.argv[1:])
