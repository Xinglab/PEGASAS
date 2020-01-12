# PEGASAS
#### Pathway Enrichment-Guided Activity Study of Alternative Splicing (PEGASAS)

### Quick guide
1. [Download](#downdload-the-pegasas-and-example-datasets)
2. [Dependencies](#Dependencies)
3. [Usage](#performing-pegasas-analysis)
4. [Contact](#contact)
5. [Publication](#citation)

### Downloading the PEGASAS and example datasets
Go to the directory you want to download the pipeline, then clone as below:
```bash
git clone git@github.com:Xinglab/PEGASAS.git
```
### Dependencies 
python version 2.7

R version 3.4.0

### Performing PEGASAS analysis
After cloned the scripts to your local direcotory, go into the directory of PEGASAS and following the below 2 steps to perform the analysis and generate correlation and Gene Ontology analysis plots.

There are two steps to perform PEGASAS analysis, as shown below (typing PEGASAS -h in the command line):
```
usage: PEGASAS [-h] [--version] {pathway,correlation} ...

PEGASAS -- PEGASAS

positional arguments:
  {pathway,correlation}
    pathway             Calculates signaling pathway activaty derived from
                        geneset enrichment metric based on RNA-Seq gene
                        expression
    correlation         Computes pathway correlated alternative splicing
                        events

optional arguments:
  -h, --help            show this help message and exit
  --version             show program's version number and exit

For command line options of each sub-command, type: PEGASAS COMMAND -h
```

#### Step 1: Pathway activity calculation

To perform pathway activity calculation, see the corresponding help message as below:

```
PEGASAS pathway -h
usage: PEGASAS pathway [-h] [-o OUT_DIR] [-n NUM_INTERVAL] [--plotting]
                       geneExpbySample geneSignatureList groupInfo

required arguments:
  geneExpbySample       A TSV format matrix of gene expression values (FPKM,
                        TPM, etc.) where each column is one sample and each
                        row is one gene.
  geneSignatureList     One or multiple gene signature sets of pathway of
                        interest in the format of 'gmt' (see MSigDB webset).
  groupInfo             A TSV format file provides patient ID and
                        phenotype/disease stage in each row.

optional arguments:
  -h, --help            show this help message and exit
  -o OUT_DIR, --out-dir OUT_DIR
                        Output folder name of the analysis.
  -n NUM_INTERVAL, --num-interval NUM_INTERVAL
                        Number of KS enrichment calculation processes one
                        time.
  --plotting            Making plots to inspect K-S enrichment scores.
  ```
 You can find the [example](https://github.com/Xinglab/PEGASAS/tree/master/example) file for groupInfo and 50 Hallmarks in the [dataset](https://github.com/Xinglab/PEGASAS/tree/master/PathwayActivity/dataset) from the Github repo. 
 
 #### Step 2: Pathway activity-correlated events
 
 To perform pathway activity calculation, see the corresponding help message as below:
 ```
 PEGASAS correlation -h
usage: PEGASAS correlation [-h] [-o OUT_DIR] [--GO] [--GO-only]
                           [-b GO_BACKGROUND_GENE_LIST]
                           signatureScorebySample PSIbySample groupNameOrder

required arguments:
  signatureScorebySample
                        A TSV format list of gene signature score where each
                        column is one sample and the corresponding score.
  PSIbySample           A TSV format matrix of PSI values where each column is
                        one sample and each row is one splicing event
  groupNameOrder        A file contains a comma-separated string of group name
                        orders. The group name should match group info list in
                        the pathway score calculation step. This is useful for
                        the heatmap visualization.

optional arguments:
  -h, --help            show this help message and exit
  -o OUT_DIR, --out-dir OUT_DIR
                        Output folder name of the analysis.
  --GO                  Perform GO analysis.
  --GO-only             Only perform GO analysis. Needs to provide background
                        gene list for p-value calculation.
  -b GO_BACKGROUND_GENE_LIST, --GO-background-gene-list GO_BACKGROUND_GENE_LIST
                        Provides background gene list for GO analysis bias
                        correction. This background list should contain genes
                        involved in the splicing analysis. Required under GO-
                        only mode.

```

### Example

```
PEGASAS pathway -o test example/geneExpbySample_example.txt PEGASAS/data/hallmarks50-2.gmt.txt example/groupInfo_example.txt

PEGASAS correlation -o test --GO test/HALLMARK_MYC_TARGETS_V2/HALLMARK_MYC_TARGETS_V2.scores.txt example/PSIbySample_example.txt example/groupNameOrder_example.txt
```

### Contact

Yang Pan <panyang@ucla.edu>
Yi Xing <XINGYI@email.chop.edu>

### Citation
Manuscript in press. 

Phillips J.W.*, Pan Y.*, Tsai B.L., Xie Z., Demirdjian L., Xiao W., Yang H.T., Zhang Y., Lin C.H., Cheng D., Hu Q., Liu S., Black D.L., Witte O.N.+, Xing Y.+ (2020) Pathway-guided analysis reveals Myc-dependent alternative pre-mRNA splicing in aggressive prostate cancers. Proc. Natl. Acad. Sci. U.S.A., In Press (+ joint corresponding authors; * joint first authors)
