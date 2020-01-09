import sys
import os
import argparse
import csv


def main(argv):
    args = parse_arguments(argv)

    file1 = args.file1
    out= args.out_path
    dataset = args.dataset
    database = args.database

    ont_level = ["family","gene","variant"]

    #parse input dataset
    data = []
    with open(file1) as f1:
        reader1 = csv.reader(f1, delimiter='\t')
        for row in reader1:
            # print(row)
            data.append(row)

    outHits = []
    counts = [0,0,0,0]
    for hit in data:
        thisFam = hit[2]
        if thisFam not in outHits:
            counts[3] += 1
            outHits.append(thisFam)
            for ont in ont_level:
                if hit[-1] == ont:
                    counts[ont_level.index(ont)] += 1


    with open(out, 'a+') as output:
        # output.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % ("Database","Dataset","Family","Gene","Variant","Total"))
        print(database + "\t" + dataset + "\t" + "\t".join(map(str, counts)))
        output.write(database + "\t" + dataset + "\t" + "\t".join(map(str, counts))+"\n")





def parse_arguments(argv):
    parser = argparse.ArgumentParser(
        prog = 'hmmscan_count.py',
        description = 'A program tthat parses a hmmscan output')
    parser.add_argument(
        '-f1', '--file1',
        help = 'Enter first hmmscan outfile',
        required = True
    )
    parser.add_argument(
        '-ds', '--dataset',
        help = 'Enter dataset name',
        required = True
    )
    parser.add_argument(
        '-db', '--database',
        help = 'Enter database name',
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
