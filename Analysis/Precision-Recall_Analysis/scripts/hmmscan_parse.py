#!/usr/bin/env python

"""
File Name       : hmmscan_parse.py
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
from Bio import SearchIO


def main(argv):
    args = parse_arguments(argv)

    infile = args.infile
    out= args.out_path
    outputs = []
    query_sequences = []
    count = 0

    with open(out, 'w+') as output:
        output.write("%s\t%s\t%s\t%s\n" % ("Accession","family","query_name","Resfams_description"))
        for qresult in SearchIO.parse(infile, "hmmer3-tab"):
            for hits in qresult:
                accession = hits.accession
                id = hits.id
                query = hits.query_id
                description = hits.description
                score = hits.bitscore

                array = [accession,id,query,description,str(score)]

                print("\t".join(array))
                output.write("\t".join(array)+"\n")

                if hits.query_id not in query_sequences:
                    query_sequences.append(hits.query_id)
                    count += 1
        print("Unique Seqs: " + str(count))



def parse_arguments(argv):
    parser = argparse.ArgumentParser(
        prog = 'hmmscan.parse',
        description = 'A program to parse an hmmscan output')
    parser.add_argument(
        '-i', '--infile',
        help = 'Enter first hmmscan outfile',
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
