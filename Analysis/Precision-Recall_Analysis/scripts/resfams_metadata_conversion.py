import sys
import os
import argparse
import csv


def main(argv):
    args = parse_arguments(argv)

    file1 = args.file1
    meta = args.meta
    out= args.out_path

    data = []
    metadata = []

    with open(file1) as f1:
        reader = csv.reader(f1, delimiter='\t')
        for row in reader:
            data.append(row)

    with open(meta) as m:
        reader2 = csv.reader(m, delimiter='\t')
        for row in reader2:
            if row not in metadata:
                metadata.append(row)

    outData = []
    for seq in data:
        seqID = seq[0]
        ids = seq[1].split("|")
        convID = []

        for fam in metadata:
            mbid = fam[1]
            rfid = fam[2]

            for id in ids:
                if id == mbid and rfid != "" and rfid not in convID:
                    convID.append(rfid)

        array = [seqID,"|".join(convID)]
        outData.append(array)


    with open(out, 'w+') as output:
        for row in outData:
            print("\t".join(row))
            output.write("\t".join(row)+"\n")





def parse_arguments(argv):
    parser = argparse.ArgumentParser(
        prog = 'hmmscan.parse',
        description = 'A program tthat parses a hmmscan output')
    parser.add_argument(
        '-f1', '--file1',
        help = 'Enter first hmmscan outfile',
        required = True
    )
    parser.add_argument(
        '-m', '--meta',
        help = 'Enter meta-family data file',
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
