# PEGASAS
#### Pathway Enrichment-Guided Activity Study of Alternative Splicing (PEGASAS)
__Web server:__ We have a web server now! It supports light-weight analysis and various interactive visualizations (scatter plot, hive plot, etc.), [check it out by clicking here!](http://xingshiny.research.chop.edu:3838/PEGASASServer/) 

### Quick guide
1. [Installation](#installation)
2. [Dependencies](#dependencies)
3. [Usage](#performing-pegasas-analysis)
4. [Example](#example-pegasas-run)
4. [Contact](#contact)
5. [Publication](#citation)

### Installation
The PEGASAS package (including [a toy example](https://github.com/Xinglab/PEGASAS/tree/master/example) and [data](https://github.com/Xinglab/PEGASAS/tree/master/PEGASAS/data)) can be downloaded and installed as shown below:
```
git clone https://github.com/Xinglab/PEGASAS.git
cd PEGASAS
python setup.py install
```
Note that the installation process will only automatically check and install python package dependencies. If the R packages required for PEGASAS are missing, they can only be installed manually. See [next section](#dependencies) for required packages.

### Dependencies 
python version 2.7 (numpy, scipy, matplotlib)

R version 3.4.0 (LSD, data.table, ggplot2)

### Performing PEGASAS analysis
After installing PEGASAS and its dependencies, the user can follow the two steps below to perform the analysis and to generate plots for correlation and Gene Ontology (GO) analysis.  ([A toy example](https://github.com/Xinglab/PEGASAS/tree/master/example) is provided for a test run. Corresponding commands are provided in the [next section](#example-pegasas-run).)

There are two steps to perform PEGASAS analysis, as shown below (typing PEGASAS -h in the command line):
```
usage: PEGASAS [-h] [--version] {pathway,correlation} ...

PEGASAS -- PEGASAS

positional arguments:
  {pathway,correlation}
    pathway             Calculates signaling pathway activity derived from
                        geneset enrichment metric based on RNA-Seq gene
                        expression
    correlation         Computes pathway-correlated alternative splicing
                        events

optional arguments:
  -h, --help            show this help message and exit
  --version             show program's version number and exit

For command line options of each sub-command, type: PEGASAS COMMAND -h
```
##### Step 1: Pathway activity calculation
PEGASAS can calculate the signaling pathway activity based on predefined gene signatures and gene expression. For details of this step, see below:
```
PEGASAS pathway -h
usage: PEGASAS pathway [-h] [-o OUT_DIR] [-n NUM_INTERVAL] [--plotting]
                       geneExpbySample geneSignatureList groupInfo

required arguments:
  geneExpbySample       TSV format matrix of gene expression values (FPKM,
                        TPM, etc.), where each column is one sample and each
                        row is one gene
  geneSignatureList     One or multiple gene signature sets from pathway of
                        interest, in the 'gmt' format (see MSigDB webset)
  groupInfo             TSV format file, providing patient ID and
                        phenotype/disease stage in each row

optional arguments:
  -h, --help            show this help message and exit
  -o OUT_DIR, --out-dir OUT_DIR
                        Name of folder for analysis output
  -n NUM_INTERVAL, --num-interval NUM_INTERVAL
                        Number of parallel processes for KS enrichment calculation
  --plotting            Makes plots to inspect K-S enrichment scores
  ```
  
 ##### Step 2: Pathway activity-correlated events
PEGASAS can perform correlation analysis to identify pathway-associated events from the pathway acitivity measurements generated in Step 1 and alternative splicing(or editing, etc.) events. For details of this step, see below:
 ```
PEGASAS correlation -h
usage: PEGASAS correlation [-h] [-o OUT_DIR] [--GO] [--GO-only]
                           [-b GO_BACKGROUND_GENE_LIST]
                           signatureScorebySample PSIbySample groupNameOrder

required arguments:
  signatureScorebySample
                        TSV format list of gene signature scores, where each
                        column is one sample and the corresponding score
  PSIbySample           TSV format matrix of PSI values where each column is
                        one sample and each row is one splicing event
  groupNameOrder        File containing a comma-separated string of group name
                        orders. The group name should match group info list in
                        the pathway score calculation step. This is useful for
                        the heatmap visualization

optional arguments:
  -h, --help            show this help message and exit
  -o OUT_DIR, --out-dir OUT_DIR
                        Name of folder for analysis output
  --GO                  Performs GO analysis
  --GO-only             Only performs GO analysis. Requires to provide background
                        gene list for p-value calculation (see -b GO_BACKGROUND_GENE_LIST)
  -b GO_BACKGROUND_GENE_LIST, --GO-background-gene-list GO_BACKGROUND_GENE_LIST
                        Provides background gene list for GO analysis bias
                        correction and should contain genes
                        participated in the splicing analysis. Required for GO-
                        only mode

```

### Example PEGASAS run
Here are commands for a test run using [toy example files](https://github.com/Xinglab/PEGASAS/tree/master/example) provided in the example folder in the package.\
Go to PEGASAS folder:
```
cd PEGASAS
```
Use hallmarks50-2.gmt.txt as the signature file. This file only contains two gene signatures:
```
PEGASAS pathway -o test example/geneExpbySample_example.txt PEGASAS/data/hallmarks50-2.gmt.txt example/groupInfo_example.txt
```
Use the HALLMARK_MYC_TARGETS_V2 signature activity generated in the last step to perform the correlation analysis:
```
PEGASAS correlation -o test --GO test/HALLMARK_MYC_TARGETS_V2/HALLMARK_MYC_TARGETS_V2.scores.txt example/PSIbySample_example.txt example/groupNameOrder_example.txt
```
Results can be found under the 'test' folder:
```
 4.0K  GO/ 
  40K  HALLMARK_MYC_TARGETS_V2_background_list.txt
 924K  HALLMARK_MYC_TARGETS_V2_global_cor_matrix.txt
 3.1K  HALLMARK_MYC_TARGETS_V2_high_cor_matrix.txt
  56K  HALLMARK_MYC_TARGETS_V2_high_cor_scatterplots.pdf
 4.0K  HALLMARK_MYC_TARGETS_V2.pathway/
 1.3K  HALLMARK_MYC_TARGETS_V2.scores.txt
  241  HALLMARK_MYC_TARGETS_V2_sig_list.txt
  579  HALLMARK_MYC_TARGETS_V2.sorted.txt
 2.4M  refinedBySample.PSIbySample_example.HALLMARK_MYC_TARGETS_V2.sorted.txt
```
__HALLMARK_MYC_TARGETS_V2_high_cor_matrix.txt__: Pathway-associated events with Pearson's r and permutation p-value.


### Contact

Yang Pan <panyang@ucla.edu>\
Yi Xing <XINGYI@email.chop.edu>

### Citation

Phillips J.W.\*, Pan Y.\*, Tsai B.L., Xie Z., Demirdjian L., Xiao W., Yang H.T., Zhang Y., Lin C.H., Cheng D., Hu Q., Liu S., Black D.L., Witte O.N.+, Xing Y.+ __Pathway-guided analysis reveals Myc-dependent alternative pre-mRNA splicing in aggressive prostate cancers.__ Proc. Natl. Acad. Sci. U.S.A., (2020) In Press (+ joint corresponding authors; \* joint first authors)
