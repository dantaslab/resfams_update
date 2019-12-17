# **Resfams Update 2019**
2019 Update to resfams database

---

# Workflow

### 1) Construct Phylogenetic Trees
  Start with a set of sequences believed to be related in fasta format (for example Class A beta-lactamases)<br> * We used existing Resfams families and supplemented with CARD data, separated into broad family groups.

  I. cd-hit with a "c" value of 1.0 was used to remove redundant sequences

    cd-hit -i family_seqs.faa -o family_cdhit.faa -c 1.0

  II. blastp of family sequences against CARD with an evalue cutoff of 1E-10, percent identity cutoff of 90%, and q-coverage cutoff of 80% was used to retrieve sequence information.

    blastp -db "CARD_db" -query family_cdhit.faa -evalue 1e-10 -pident 90 -qcov 80 -outfmt 6 -out family_card_blast.txt

  III. Custom script: make_tree_dataset.py preps and renames input sequences in order to make tree analysis easier.
  * outputs 2 files: family_tree_dataset.faa and family_tree_mappingFile.txt


    make_tree_dataset.py --infile family_cdhit.fasta --blast family_card_blast.txt --family "famliy" --out_path path/to/output/directory/

  IV. muscle used to create multiple sequence alignment of parsed tree family sequences

    muscle -seqtype protein -in family_tree_dataset.faa -out family_tree_aligned.afa

  V. fasttree/2.1.9 used to create a tree file for phylogenetic analysis

    FastTree family_tree_aligned.afa > family_tree.txt

  VI. tree file was analyzed and family_tree_mappingFile.txt was manually curated to list corresponding resistance families for each sequence

| Tree Seq Header | Original Header | Family1 | Family2 | Family3 | Family4
| :-------------: |:-------------:|:-----:|:-----:|:-----:|:-----:|
| RF-1\|CblA-1\|CblA-1 | gb\|ACT97415.1\|ARO:3002999\|CblA-1 | CblA | blactamA |
| RF-2\|SHV-52\|SHV-52 | gb\|AEJ08681.1\|ARO:3001109\|SHV-52 |  SHV | SHV-LEN | SHV-LEN-OKP | blactamA |
| RF-3\|CTX-M-130\|CTX-M-130 | gb\|AFJ59957.1\|ARO:3001989\|CTX-M-130 | CTX-M | blactamA |

  * Note: the sequences used in the example above came from CARD, so there is redundant information in the header.


### 2) HMM Construction
