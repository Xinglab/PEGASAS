import sys, os, argparse
#INPUT GSEA fold needs to be organized in the defined way(just two hierarcy, type and name)
#INPUT GSEA matrix is a sample vs KS score matrix; INPUT PSI matrix is a sample vs PSI matrix. Sort sample based on the former one.
#This script sort based on groups for the purpose of heatmap.

#INPUTS
parser = argparse.ArgumentParser(description='PEGASAS-Correlation (v1.0)')
parser.add_argument('signatureScorebySample',help='A TSV format list of gene signature score where each column is one sample and the corresponding score.')
parser.add_argument('PSIbySample',help='A TSV format matrix of PSI values where each column is one sample and each row is one splicing event')
parser.add_argument('groupNameOrder',help='A file contains a comma-separated string of group name orders. The group name should match group info list in the pathway score calculation step. This is useful for the heatmap visualization.')
parser.add_argument('-o','--out-dir', default='PEGASAS_PathwayScore', help='Output folder name of the analysis.')
parser.add_argument('-g','--GO-background-gene-list',default=False, action='store_true', help='Enables downstream GO analysis of pathway activity-correlated events and provides background gene list for GO anlaysis bias correction. This background list should contain genes involved in the splicing analysis.')
parser.add_argument('--GO-path',default='/u/nobackup/yxing-BIGDATA/panyang/Analysis.scripts/GO/GO_plot.R', action='store_true', help='directory of GO analysis scripts.')
args = parser.parse_args()




fin_signature=args.signatureScorebySample#UPDATED Sep2018 #
signature_name=fin_signature.split('/')[-1].split('.scores.txt')[0]
fin_PSI_matrix=args.PSIbySample
sample_order_fin=args.groupNameOrder #split by comma
sample_order=''
for l in open(sample_order_fin):
	sample_order=l.strip()
	break
outdir=args.out_dir
GO_path=args.GO_path
GO_analysis=False
if args.GO_background_gene_list:
	GO_analysis=True
	bg_list_dir=args.GO_background_gene_list
	
#STEP1: SORTING (matching sample, ordering sample for heatmap) #TODO, simple version- just matching sample
print '###STEP 1'
cmd1='python prepareGeneMatrixOrdered.py '+fin_signature+' '+outdir+' '+sample_order
print cmd1
os.system(cmd1)

cmd2='python generateMatrixbySample.py '+fin_PSI_matrix+' '+outdir+'/'+signature_name+'/'+signature_name+'.sorted.txt'
print cmd2
os.system(cmd2)

#STEP2: CALCULATE CORRELATION
print '###STEP 2'
cmd3='Rscript cor_matrix_direct_perm.R '+outdir+'/'+signature_name+'/'+signature_name+'.sorted.txt '+outdir+'/'+signature_name+'/refinedBySample.'+fin_PSI_matrix.split('/')[-1].rstrip('.txt')+'.'+signature_name+'.sorted.txt '+outdir+'/'+signature_name
print cmd3
os.system(cmd3)

#STEP3: PARSE FOR GO ANLAYSIS
print '###STEP 3'
fout=open(outdir+'/'+signature_name+'/'+signature_name+'_sig_list.txt','w')
keys={}
n=0
for l in open(outdir+'/'+signature_name+'/'+signature_name+'_high_cor_matrix.txt'):
	if n==0:
		n+=1
		continue
	ls=l.strip().split('\t')
	keys[ls[0].split('_')[0]]=''
for k in keys:
	fout.write(k+'\n')
fout.close()

#STEP4: GO ANALYSIS
print "###STEP 4"
if GO_analysis==False:
	exit('Skipped GO.')
cmd4 = 'Rscript '+GO_path+' '+bg_list_dir+' '+outdir+'/'+signature_name+'/'+signature_name+'_sig_list.txt'+' '+outdir+' '+signature_name
print cmd4
os.system(cmd4)


