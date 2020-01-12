import multiprocessing as mp
import sys, csv, os, numpy, argparse
from scipy import stats
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from . import config

def loadGeneSet(fin): #GMT file
	geneSet={}
	for l in open(fin):
		ls=l.strip().split('>')
		gene_set_name=ls[0].strip('\t').strip()
		if gene_set_name  not in geneSet:
			geneSet[gene_set_name]={}
		else:
			exit('gene set name conflicts!')
		gene_list_des=ls[1].strip('\t').strip()
		if gene_list_des.find('.')!=0:
			gene_list_des=gene_list_des.rsplit('.',1)[-1].strip('\t').strip() #just split the right most '.'
		gene_list=gene_list_des.split()
		for g in gene_list:
			geneSet[gene_set_name][g.strip()]=''
	return geneSet


def loadExpSet(fin): #gene exp matrix
	geneExp={}
	header=[]
	for i,l in enumerate(open(fin)):
		if i==0:
			header=l.strip().split()[1:]
			continue
		ls=l.strip().split()
		geneExp[ls[0]]=ls[1:]
	return geneExp, header
	
def loadGroupInfo(fin):
	groupMap={}
	for l in open(fin):
		ls=l.strip().split('\t')
		groupMap[ls[0]]=ls[1]
	return groupMap

def KS_test(l_hits, l_null, l_w, plotting, sample_name): #lists are ranks based on sorted list
	med_hits=numpy.median(l_hits)
	n_hits=len(l_hits)
	n_null=len(l_null)
	# KS two sample two sided test
	ks_result=stats.ks_2samp(l_hits,l_null)
	enrichment_score = ks_result[0]
	enrichment_pvalue = ks_result[1]
	if plotting:
		max_hits=max(l_hits)
		enrichment=0
		es_list=[]
		for i in range(0,max_hits+1):
			if l_w[i]=='Hit':
				enrichment+=1.0/n_hits
			else:
				enrichment+=-1.0/n_null
			es_list.append(enrichment)
		plt.plot(es_list)
		plt.ylabel('enrichment')
		plt.xlim(0,len(l_w))
		plt.savefig(sample_name+'.png')
	return enrichment_score, enrichment_pvalue, med_hits


def SampleEnrichment(gene_exp,gene_set,sample_name, group, outdir): 
	make_plot=False
	fout=open(outdir+'/'+sample_name+'.txt','w')
	if make_plot:
		os.system('mkdir -p '+outdir+'/fig/')
	l_hits=[]
	l_null=[]
	l_w=[]
	for rank,k in enumerate(sorted(gene_exp.keys(), key=lambda x: float(gene_exp[x]), reverse=True)): #keep value float is important for the python's numeric sorting!! 
		if gene_set.has_key(k):
			l_w.append('Hit')
			l_hits.append(rank)
		else:
			l_w.append('Non-Hit')
			l_null.append(rank)
	enrichment_score, enrichment_pvalue, med_hits=KS_test(l_hits,l_null,l_w, make_plot , outdir+'/fig/'+sample_name)
	fout.write('{}\t{}\t{}\t{}\t{}\n'.format(sample_name, group, enrichment_score, enrichment_pvalue, med_hits))


def main(args):
	fin_exp_matrix=args.geneExpbySample
	geneExp, header=loadExpSet(fin_exp_matrix)
	outdir=args.out_dir.rstrip('/')
	numInterval=args.num_interval
	group_info=args.groupInfo
	groupMap=loadGroupInfo(group_info)

	fin_gene_set=args.geneSignatureList
	geneSet=loadGeneSet(fin_gene_set)
	for gs in geneSet:
		print gs
		score_outdir=outdir+'/'+gs+'/'+gs+'.pathway'
		os.system('mkdir -p '+outdir+' '+score_outdir)
		batch_list=[]
		batch_list_s=[]
		tot=len(geneExp.keys())
		for i,sample_name in enumerate(geneExp.keys()):
			config.update_progress(i/(0.0+tot))
			exp_v=geneExp[sample_name]
			exp_dict=dict(zip(header,exp_v))
		 	batch_list.append(exp_dict)
		 	batch_list_s.append(sample_name)
		 	if len(batch_list)==numInterval:
				KS_ES_list=[]
				for n in xrange(0,numInterval):
					KS_ES_list.append(mp.Process(target=SampleEnrichment,args=(batch_list[n], geneSet[gs],batch_list_s[n], groupMap[batch_list_s[n]], score_outdir)))
					KS_ES_list[n].start()
				for n in xrange(0,numInterval):
					KS_ES_list[n].join()
				batch_list=[]
				batch_list_s=[]
		#handle last batch
		if batch_list!=[]:
			print 'exist last batch',len(batch_list)
			KS_ES_list=[]
			for n in xrange(0,len(batch_list)):
				KS_ES_list.append(mp.Process(target=SampleEnrichment,args=(batch_list[n], geneSet[gs],batch_list_s[n],groupMap[batch_list_s[n]], score_outdir)))
				KS_ES_list[n].start()
			for n in xrange(0,len(batch_list)):
				KS_ES_list[n].join()
			batch_list=[]
			batch_list_s=[]
		print score_outdir, 'done'

		os.system('cat '+score_outdir.rstrip('/')+'/*.txt >'+score_outdir.rstrip('/').split('.pathway')[0]+'.scores.txt')
		#os.system('rm -r '++score_outdir.rstrip('/'))
		print 'merged'

if __name__ == '__main__':
	main()