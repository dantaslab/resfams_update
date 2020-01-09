import sys
import os
import argparse
import csv
from Bio import SearchIO


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
        reader2 = csv.reader(m, delimiter='\t')
        for row in reader2:
            if row not in metadata:
                metadata.append(row)

    hmm_data = []
    for qresult in SearchIO.parse(file1, "hmmer3-tab"):
        for hits in qresult:
            accession = hits.accession
            id = hits.id
            query = hits.query_id
            description = hits.description
            score = hits.bitscore

            for hmm in metadata:
                if id == hmm[0]:
                    ont = ont_level.index(hmm[1])

            array = [accession,id,query,description,ont]

            hmm_data.append(array)
            # output.write("\t".join(array)+"\n")

    outHits = {}
    for hit in hmm_data:
        thisFam = hit[2]
        if thisFam not in outHits.keys():
            outHits[thisFam] = hit
        else:
            if hit[4] > outHits[thisFam][4]:
                outHits[thisFam] = hit

    with open(out, 'w+') as output:
        output.write("%s\t%s\t%s\t%s\t%s\n" % ("Accession","family","query_name","Resfams_description","Ontology_Level"))
        for k,v in outHits.items():
            v[4] = ont_level[v[4]]
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
