import sys
import os
import pandas as pd
import csv
import argparse
from collections import OrderedDict


def main(argv):
    args = parse_arguments(argv)
    out = args.out_path
    file1 = args.file1


    map_files(file1,out)



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
        '-o', '-outpath',
        dest = 'out_path',
        help = 'Enter path to dropped seqs file'
    )

    return parser.parse_args()


def map_files(file1, out):
    df1 = pd.read_table(file1, sep="\t", usecols=[0,1,2,3,5], names=['query_name','blast_id','pident','evalue','qcoverage'])
    print("input: " + str(df1['query_name'].nunique()))

    df1 = df1.loc[df1['evalue'] <= 1e-10]
    df1 = df1.loc[df1['pident'] >= 80]
    # df1 = df1.loc[df1['qcoverage'] >= 80]
    # print(df1.dtypes)
    print("blast restrict: " + str(df1['query_name'].nunique()))

    df1 = df1.drop_duplicates(subset=['query_name','blast_id'], keep='first')
    df1['RFID'] = df1['blast_id'].str.split("~~~",n=1).str[0]


    ddf = df1[['query_name','RFID']]
    ddf = ddf.drop_duplicates(subset=['query_name'], keep='first')
    print("final out: " + str(ddf['query_name'].nunique()))
    ddf.to_csv(out, sep="\t", index=False, header=False)






if __name__=="__main__":
    main(sys.argv[1:])
