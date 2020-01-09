# **Resfams Update 2019**
2019 Update to Resfams database

---

## Workflow

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



### 3) Precision-Recall Analysis to Fine-Tune Profiles
  #### Precision-Recall Calculations
  _Precision_ (Positive Predictive Value) is defined as the number of relevant instances among retrieved instances.
  _Recall_ (Sensitivity) is defined as the fraction of relevant instances that were actually retrieved.
  Both of these Equations can be written as:

  <p align="center">
    <img src="https://github.com/dantaslab/resfams_update/blob/master/src/precision_recall_eq.png" alt="Precision-Recall Equations"/>
  </p>

  In the context of the analysis that we performed, we are interested in the hits we retrieved when running sequences against our Hmms and if they were accurate. As such we calculated precision and recall in this analysis with the following equations:

  <p align="center">
    <img src="https://github.com/dantaslab/resfams_update/blob/master/src/resfam_precision_recall_eq.png" alt="Resfams Precision-Recall Equations" width="400"/>
  </p>

  * Here, _Positive Hits_ are the sequences that we got hmmscan hits for that were are confirmed to be from the hit family. _Total Hits_ are the total number of hmmscan hits for a given family. _Relevent Sequences_ are the number of sequences in the dataset that are known to belong to a family.

  #### Workflow:
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
  * outputs 2 files: pr_analysis.txt, which shows the results of precision-recall analysis, and pr_fplist.txt, which shows the sequences which were falsely hit against profiles.


  python3 precision_recall.py -f1 testSet_hmmscan_parsed.txt -f2 testSet_families.txt -m testSet_metadata.txt -o path/to/output/directory/

V. Using results of precision and recall analysis, gathering thresholds, and if needed hmm sequence sets, were adjusted. If any changes were made, analysis was repeated. Continued until a precision and recall greater than 90% was achieved for all profiles.



### 4) Compile HMMs and Rename HMM sequences
Final profile HMMs for families, genes, and variants were compiled into a final HMM file. Sequences used to construct each profile had their fasta headers reformatted.

I. HMMs were compiled using _cat_ function

    cat family.hmm >> 191212-MB_Resfams.hmm

II. Custom Script: reformat_headers.py was used to reformat fasta headers using compiled metadata sequence data from HMM construction

    python3 reformat_headers.py -f1 conmpiled_hmms_seqs_metadata.txt -f2 GA_metadata.txt -f3 family_sequences.faa -d 191212 -o path/to/output/directory/

  #### Header Format:
  A format for fasta headers was developed to give the most information possible while also making easy to parse and avoid unwanted errors and interactions with existing informatics programs.
  These headers were constructed from existing information, primarily from the old headers, and supplemented by Resfams information we collected in the Hmm profile building process.

    Resfams IDs~~~Database Name=ID~~~Sequence Name

    MB-RF002|MB-RF003|MB-RF011~~~gb=AAR21614.1|card=ARO:3002529~~~AAC(3)-Id


---

## Analysis
  To assess the update to Resfams, we performed analysis on the _Precision and Recall_ as well as the _Resolution_ of the updated database. That is, we wanted to see the accuracy of the new database and at what level--family, gene, variant-- we were able to classify sequences.

### 1) Resolution Comparative Analysis:
  Resolution analysis was performed against 5 different databases and across 3 datasets.
  ###### Databases:
  * MBhmms
  * ncbi amrfinder module
  * ncbi hmms
  * Resfams-full
  * Resfams-core


  ###### Datasets:
  * CARD dataset (3.05) -- 2602 Unique Sequences
  * fxl metgenomic dataset provided by Dantas Lab-- 23095 Unique Sequences
  * Megares dataset (2.0) -- 6742 Unique Sequences


  ##### Workflow:
  I. cd-hit with a cutoff value of 1.0 was used to remove redundant sequences

    cd-hit -i dataset_seqs.faa -o dataset_seqs_cdhit.faa -c 1.0

  II. hmmscan dataset against database

    hmmscan --cut_ga --tblout analysis_hmmscan.txt database.hmm dataset_seqs_cdhit.faa


  III. Custom Script: hmmscan_parse_v02.py parses hmmscan table output, retrieving relevant information for precision-recall analysis
  * database_families.txt is a family of database families with labels as to what level--family, gene, variant-- each is.


  python3 hmmscan_parse.py -f1 analysis_hmmscan.txt -m database_families.txt -o analysis_hmmscan_parsed.txt

  Note: amrfinder module used its own program and parsing script to run against its database.

    amrfinder --protein dataset_seqs_cdhit.faa --output analysis_output.txt

    python3 amrfinder_parse.py -f1 analysis_output.txt -m ncbi_families.txt -o analysis_output_parsed.txt

  IV. Custom Script: hmmscan_count.py counts the number of hits at the deepest ontology level found for each sequence.

    python3 hmmscan_count.py -f1 analysis_hmmscan_parsed.txt -ds "dataset" -db "database" -o analysis-hitCounts.txt

  V. Hit counts are compiled and, using _Seaborn_, graphs were constructed for analysis

  #### A) Total Hits Comparison

  <p align="center">
    <img src="https://github.com/dantaslab/resfams_update/blob/master/Analysis/Resolution_Analysis/plots/191218-comparative_analysis.png" alt="Total Hits Comparative Analysis"/>
  </p>


  #### B) Resolution Comparison

  <p align="center">
    <img src="https://github.com/dantaslab/resfams_update/blob/master/Analysis/Resolution_Analysis/plots/191218-resolution_analysis.png" alt="Resolution Comparative Analysis"/>
  </p>



### 2) Precision and Recall Comparative Analysis:
  Precision and Recall Analysis compared the performance of the new Resfams against the old version. We conducted the analysis using 2 different datasets.

  ###### Databases:
  * MBhmms
  * Resfams-full

  ###### Datasets:
  * CARD dataset (3.05) -- 2602 Unique Sequences
  * NCBI Amrfinder Proteins -- 5823 Unique Sequences


  ##### Workflow:
  We will run the anlysis against the New Resfams first because its information is easier to parse and can easily be mapped to Old Resfams profiles.

  I. blastp against new Resfams was used to get initial classification of dataset sequences by profile family.

    blastp -db MB_Resfams.hmm -query AMRProt.fasta -outfmt '6 qseqid sseqid pident evalue bitscore qcovs' -out MBHmms_blast.txt


  II. Custom Script: blast_aro_parse.py parses blast output, restricting hits by predetermined evalue, percent identity, and query coverage (we used 1e-10, 80%, 80% for each respectively) and outputs a metadata file to be used for precision-recall analysis.

    python3 blast_aro_parse_v01.py -f1 MBHmms_blast.txt -o MBHmms_blast_parsed.txt


  III. hmmscan dataset against New Resfams.

    hmmscan --cut_ga --tblout MBHmms_hmmscan.txt MB_Resfams.hmm AMRProt.fasta


  III. Custom Script: hmmscan_parse.py parses hmmscan table output, retrieving relevant information for precision-recall analysis

    python3 hmmscan_parse.py -i MBHmms_hmmscan.txt  -o MBHmms_hmmscan_parsed.txt


  IV. Custom Script: precision_recall_v02.py performs precision recall by comparing hmmscan output to known classification of input sequences.
    * outputs 3 files: pr_analysis.txt, which shows the results of precision-recall analysis, pr_fplist.txt, which shows the sequences which were falsely hit against profiles, and pr_nhlist.txt, which shows the known sequences from the dataset for a family that did not get a hit.


    python3 precision_recall_v02.py -f1 MBHmms_hmmscan_parsed.txt -f2 database_families.txt -m MBHmms_blast_parsed.txt -o path/to/output/directory/


  V. Manual curation of MBHmms_fplist.txt and MBHmms_nhlist.txt to confirm that the results are accurate.
    * for MBHmms_fplist.txt, sequences that are not actually false positives (known to not belong to indicated family are removed).
    * for MBHmms_nhlist.txt sequences that do belong to indicated family are removed.
  Curated files are inputed into custom script that outputs a new metadata file to be used for another run of precision-recall analysis.

    python3 add_tp_seqs.py -f1 MBHmms_blast_parsed.txt -f2 MBHmms_fplist.txt  -f3 MBHmms_nhlist.txt -o MBHmms_metadata.txt


  VI. precision-recall_v02.py is run again using the new metadata file.


  VII. Custom Script: resfams_metadata_conversion.py is used to map the metadata file for Old Resfams. a mapping file between the databases is needed for this.

    python3 resfams_metadata_conversion.py -f1 MBHmms_metadata.txt -m MBhmms-Resfams_conversion.txt -o OldRes_metadata.txt

  VIII. hmmscan, hmmscan parsing, and precision-recall are now run in the same manner for Old Resfams using the new metadata file. Output OldRes_fplist.txt and OldRes_nhlist.txt are checked for validity.


  IX. Precision and Recall results are compiled and, using _Seaborn_, graphs were constructed for analysis.


  #### A) Precision Comparison


  #### B) Recall Comparison
