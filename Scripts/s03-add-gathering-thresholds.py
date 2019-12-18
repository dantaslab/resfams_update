#!/usr/bin/env python

"""
File Name       : add-gathering_thresholds.py
Author          : Max Bernstein
Created On      : 2019-07-20
Last Modified   : 2019-12-17
Description     : A program to add gathering thresholds and HMM data to a
                  profile hmm

Dependencies    :
Usage           : add-gathering_thresholds.py --infile CblA.hmm
                  --ga_thresh GA_metadata.txt --family CblA
                  --out_path CblA_GA.hmm
CHANGE LOG      :
TODO            :

"""

import os
import os.path
import sys
import csv
import re
import argparse



def main(argv):
    args = parse_arguments(argv)

    infile = args.infile
    outpath = args.out_path
    hmm_name = args.family
    GA_file = args.gathering_threshold

    if infile.endswith('.hmm'):

        GA = ""
        TC = ""
        NC = ""
        ACC = ""
        DESC = ""

        IN = open(infile)
        OUT = open(outpath, 'w+')

        # Find gathering threshold
        print(hmm_name)
        with open(GA_file) as GAF:
            reader = csv.reader(GAF, delimiter="\t")
            for line in reader:
                print(line[0])
                if hmm_name == line[0]:
                    print("MATCH")
                    ACC = line[1]
                    DESC = line[2]
                    GA = line[3]
                    TC = line[4]
                    NC = line[5]
                    print(ACC + " " + DESC + " " + GA + " " + TC + " " + NC)


            for line in IN:
                OUT.write(line.rstrip() + "\n")
                if line.startswith('NAME'):
                    OUT.write("ACC " + ACC + "\n")
                    OUT.write("DESC " + DESC + "\n")
                elif line.startswith('CKSUM'):
                    OUT.write("GA " + str(GA) + " " + str(GA) + ";\n")
                    if TC != "":
                        OUT.write("TC " + str(TC) + " " + str(TC) + ";\n")
                        OUT.write("NC " + str(NC) + " " + str(NC) + ";\n")




def parse_arguments(argv):
    parser = argparse.ArgumentParser(
        prog = 'add-gathering_thresholds.py',
        description = 'A program to add gathering thresholds and HMM data to a profile hmm')
    parser.add_argument(
        '-i', '--infile',
        help = 'path to in hmm file',
        required = True
    )
    parser.add_argument(
        '-o', '--outpath',
        dest = 'out_path',
        help = 'Enter path to output directory'
    )
    parser.add_argument(
        '-ga', '--ga_thresh',
        dest = 'gathering_threshold',
        help = 'Enter path to gathering threshold metadata file'
    )
    parser.add_argument(
        '-f', '--family',
        help = 'hmm family name',
        required = True
    )
    return parser.parse_args()





if __name__=="__main__":
    main(sys.argv[1:])
