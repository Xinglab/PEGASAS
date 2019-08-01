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

#### Step 1: Pathway activity calculation

To perform pathway activity calculation, see the corresponding help message as below:

```bash
>python PathwayActivity/PEGASAS_pathway.py -h
usage: PEGASAS_pathway.py [-h] [-o OUT_DIR] [-n NUM_INTERVAL] [--plotting]
                          geneExpbySample geneSignatureList groupInfo

PEGASAS-Pathway (v1.0)

positional arguments:
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
 You can find the [example](https://github.com/Xinglab/PEGASAS/tree/master/example) file for Group Info and 50 Hallmarks in the [dataset](https://github.com/Xinglab/PEGASAS/tree/master/PathwayActivity/dataset) from the Github repo. 
 
 #### Step 2: Pathway activity-correlated events
 
 To perform pathway activity calculation, see the corresponding help message as below:
 ```bash
 python CorrelationAnalysis/PEGASAS_correlation.py -h
usage: PEGASAS_correlation.py [-h] [-o OUT_DIR] [-g] [--GO-path]
                              signatureScorebySample PSIbySample
                              groupNameOrder

PEGASAS-Correlation (v1.0)

positional arguments:
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
  -g, --GO-background-gene-list
                        Enables downstream GO analysis of pathway activity-
                        correlated events and provides background gene list
                        for GO anlaysis bias correction. This background list
                        should contain genes involved in the splicing
                        analysis.
  --GO-path             directory of GO analysis scripts.
```


### Contact

Yang Pan <panyang@ucla.edu>
Yi Xing <yxing@ucla.edu>

### Citation
Manuscript in submission. 

Authors: John W. Phillips, Yang Pan ... Douglas L. Black, Owen N. Witte, Yi Xing 
