import sys, csv

def loadSampleOrder(fin):
	sample_order=[]
	for l in open(fin):
		sample_order=l.strip().split('\t')[1:]
		break
	return sample_order, fin.split('/')[-1].split('.txt')[0]

def readMatrix(fin, sample_order, name, outdir): 
	fout=open(outdir+'/refinedBySample.'+fin.split('/')[-1].split('.txt')[0]+'.'+name+'.txt','w')
	header=''
	for r in open(fin):
		header=r.strip().split('\t')[0:8]
		break
	fout.write('\t'.join(header+sample_order)+'\n')
	for l in csv.DictReader(open(fin),dialect='excel-tab'):
		key='\t'.join([l['AC'],l['GeneName'],l['chr'],l['strand'],l['exonStart'],l['exonEnd'],l['upstreamEE'],l['downstreamES']])
		line=key
		for s in sample_order:
			line+='\t'+l[s]
		fout.write(line+'\n')
		
def main():
	sample_order, name=loadSampleOrder(sys.argv[2])
	outdir='/'.join(sys.argv[2].split('/')[:-1])
	readMatrix(sys.argv[1],sample_order, name, outdir)

if __name__ == '__main__':
	main()
