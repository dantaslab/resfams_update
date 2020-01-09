import sys
import os
import argparse
import csv

def main(argv):
    args = parse_arguments(argv)

    file1 = args.file1
    meta = args.meta
    out= args.out_path
    outputs = []
    query_sequences = []

    ont_level = ["family","gene","variant"]
    metadata = []
    with open(meta) as m:
        reader = csv.reader(m, delimiter='\t')
        for row in reader:
            if row not in metadata:
                metadata.append(row)

    hmm_data = []
    with open(file1) as f:
        reader2 = csv.reader(f, delimiter='\t')
        next(reader2, None)
        for row in reader2:
            accession = row[16]
            query = row[0]
            description = row[17]

            for hmm in metadata:
                if accession == hmm[0]:
                    ont = ont_level.index(hmm[2])

            array = [accession,query,description,ont]

            hmm_data.append(array)

    outHits = {}
    for hit in hmm_data:
        thisFam = hit[2]
        if thisFam not in outHits.keys():
            outHits[thisFam] = hit
        else:
            if hit[3] > outHits[thisFam][3]:
                outHits[thisFam] = hit

    with open(out, 'w+') as output:
        output.write("%s\t%s\t%s\t%s\t%s\n" % ("Accession","family","query_name","Resfams_description","Ontology_Level"))
        for k,v in outHits.items():
            v[3] = ont_level[v[3]]
            print("\t".join(v))
            output.write("\t".join(v)+"\n")





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
