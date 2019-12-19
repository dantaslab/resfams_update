# **Resfams Update 2019**
2019 Update to resfams database

---

# Workflow

### 1) Construct Phylogenetic Trees
  Start with a set of sequences believed to be related in fasta format (for example Class A beta-lactamases)<br> * We used existing Resfams sequences and supplemented with CARD data, separated into broad family groups. HMM profiles were made at the family, gene, and variant levels as to make a complete ontology.

  I. cd-hit with a cutoff value of 1.0 was used to remove redundant sequences

    cd-hit -i family_seqs.faa -o family_cdhit.faa -c 1.0

  II. blastp of family sequences against CARD with an evalue cutoff of 1E-10, percent identity cutoff of 90%, and q-coverage cutoff of 80% was used to retrieve sequence information.

    blastp -db "CARD_db" -query family_cdhit.faa -evalue 1e-10 -pident 90 -qcov 80 -outfmt 6 -out family_card_blast.txt

  III. Custom Script: make_tree_dataset.py preps and renames input sequences in order to make tree analysis easier.
  * outputs 2 files: family_tree_dataset.faa and family_tree_mappingFile.txt


    make_tree_dataset.py --infile family_cdhit.fasta --blast family_card_blast.txt --family "famliy" --out_path path/to/output/directory/

  IV. muscle used to create multiple sequence alignment of parsed tree family sequences

    muscle -seqtype protein -in family_tree_dataset.faa -out family_tree_aligned.afa

  V. fasttree/2.1.9 used to create a tree file for phylogenetic analysis

    FastTree family_tree_aligned.afa > family_tree.txt

  VI. tree file was analyzed and family_tree_mappingFile.txt was manually curated to list corresponding resistance families for each sequence

| Tree Seq Header | Original Header | Family1 | Family2 | Family3 | Family4
| :-------------: |:-------------:|:-----:|:-----:|:-----:|:-----:|
| RF-1\|CblA-1\|CblA-1 | gb\|ACT97415.1\|ARO:3002999\|CblA-1 | CblA | ClassA |
| RF-2\|SHV-52\|SHV-52 | gb\|AEJ08681.1\|ARO:3001109\|SHV-52 |  SHV | SHV-LEN | SHV-LEN-OKP | ClassA |
| RF-3\|CTX-M-130\|CTX-M-130 | gb\|AFJ59957.1\|ARO:3001989\|CTX-M-130 | CTX-M | ClassA |

  * Note: the sequences used in the example above came from CARD, so there is redundant information in the header.


### 2) HMM Construction
  Profiles HMMs for each family, gene, and variant were constructed from family tree sequences and using the manually curated mapping file.

  I. Custom Script: compile_hmms.py
    * outputs 1 file1: family_hmm_seqs.faa. This is a fasta file of the sequences that are to be used to construct the profile hmm for a given gamily

    python3 hmm_compile_dataset.py -i family_tree_dataset.faa -m family_tree_mappingFile.txt -s family -o path/to/output/directory/

  II. muscle used to create multiple sequence alignment of profile hmm sequences

    muscle -seqtype protein -in family_hmm_seqs.faa -out family_hmm_aligned.afa

  III. hmmbuild used to create an hmm from the aligned sequences

    hmmbuild -n family --amino family.hmm family_hmm_aligned.afa


  IV. A Gathering Thresholds metadata file constructed for each profile. This metadata file was then used to modify the build profiles hmms using a custom script, add-gathering-thresholds.py.

    python3 add-gathering-thresholds.py -i family.hmm -o family_GA.hmm -ga GA_metadata.txt -f family

  | Name | RFID | Description | GA | TC | NC |
  |:-------------:|:-----:|:-----:|:-----:|:-----:|:-----:|
  | CfxA | MB-RF033 | CfxA cephalosporin (class a) [ARO:3001211] | 500 | 500 | 500 |
  |  ClassA |  MB-RF034 | Class A beta-lactamase [ARO:3000078] | 75 | 75 | 75 |
  | ClassB | MB-RF035 | Class B beta-lactamase [ARO:3000004] | 79 | 79 | 79 |

  * Example format of the gathering thresholds metadata file



### 3) Precision-Recall Analysis
  A test set of sequences with known ontologies was used to test HMM precision and recall. Start with fasta file of sequences to test as well as a metadata file with associated family, gene, and variant classifications.

  | Sequence Header | Family1 | Family2 | Family3 | Family4 |
  |:-------------:|:-----:|:-----:|:-----:|:-----:|
  | AF395881.gene.p01 | KPC | ClassA |
  |  AM087453.1.gene1.p01 |  SHV-LEN | SHV-LEN-OKP | ClassA |
  | gb\|CAJ19616.1\|ARO:3002441\|OKP-B-8 | OKP-B | OKP | SHV-LEN-OKP| ClassA


I. cd-hit with a cutoff value of 1.0 was used to remove redundant sequences

    cd-hit -i testSet_seqs.faa -o testSet_cdhit.faa -c 1.0

II. hmmscan test set sequences against new HMMs

    hmmscan --cut_ga --tblout testSet_hmmscan.txt new_family_db.hmm testSet_cdhit.faa

III. Custom Script: hmmscan_parse.py parses hmmscan table output, retrieving relevant information for precision-recall analysis

    python3 hmmscan_parse.py -i testSet_hmmscan.txt -o testSet_hmmscan_parsed.txt

IV. Custom Script: precision_recall.py performs precision recall by comparing hmmscan output to known classification of input sequences.
  * outputs 2 files: pr_analysis.txt and pr_fplist.txt


    python3 precision_recall.py -f1 testSet_hmmscan_parsed.txt -f2 testSet_families.txt -m testSet_metadata.txt -o path/to/output/directory/

V. Using results of precision and recall analysis, gathering thresholds and if needed hmm sequence sets were adjusted. If any changes made, analysis was repeated. Continued until a precision and recall greater than 90% was achieved for all profiles.



### 4) Compile HMMs and Rename HMM sequences


---

# Analysis

### 1) Comparative Analysis
