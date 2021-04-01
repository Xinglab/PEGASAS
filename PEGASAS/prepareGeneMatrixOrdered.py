import sys,os

def loadGeneList(fin): #A file with Both ENSMBL ID and HUGO gene name
	Gene_list={}
	for l in open(fin):
		ls=l.strip().split(',')
		Gene_list[ls[1]]=''
	return Gene_list


def loadfromExpMatrix(fin,Gene_list):
	EXP={}
	n=0 
	header=[]
	for l in open(fin):
		if n==0:
			header=l.strip().split('\t')[1:]
			n+=1
			continue	
		ls=l.strip().split('\t')
		l_dict=dict(zip(header,ls[1:]))
		if ls[0].split('.')[0] in Gene_list:
			if ls[0].split('.')[0] in EXP:
				print '! Error in ', ls[0]
			EXP[ls[0].split('.')[0]]={}
			for sample in l_dict.keys():
				EXP[ls[0].split('.')[0]][sample]=float(l_dict[sample])
		return EXP

def loadOrder(fin):
	order=[]
	for l in open(fin):
		order=l.strip().split(',')
		break
	return order

def loadfromGSEA(fin): #Updated with new pathway format Sep 2018
	ES={}
	for l in open(fin):
		ls=l.strip().split('\t')
		if ls[1] not in ES:
			ES[ls[1]]={}
		ES[ls[1]][ls[0]]=float(ls[2])
	return ES


def main():
	fin_gene_score=sys.argv[1]
	Gene_score_dict=loadfromGSEA(fin_gene_score)
	outdir=sys.argv[2].rstrip('/')
	folder_prefix=fin_gene_score.split('/')[-1].split('.scores.txt')[0]
	os.system('mkdir -p '+outdir+' '+outdir+'/'+folder_prefix)
	fout_name=fin_gene_score.split('/')[-1].split('.scores.txt')[0]+'.sorted.txt'
	fout=open(outdir+'/'+folder_prefix+'/'+fout_name,'w')
	header_line='SampleID'
	value_line=sys.argv[1].split('/')[-1].split('.')[0]
	sample_order_fin=sys.argv[3]
	order=loadOrder(sample_order_fin)
	#print order
	#order=['Benign-GTEx','Benign-TCGA','Primary-TCGA','CRPC-SU2C','CRPC-Robinson','CRPC-Beltran','NE-SU2C','NE-Beltran']
	if len(order)==0:
		exit('needs to input the sample order for matrix')

	for dataset in order:
		for sample in sorted(Gene_score_dict[dataset].keys(), key=lambda x:Gene_score_dict[dataset][x]):
			header_line+='\t'+sample
			value_line+='\t'+str(Gene_score_dict[dataset][sample])

	fout.write(header_line+'\n')
	fout.write(value_line+'\n')

if __name__ == '__main__':
	main()
