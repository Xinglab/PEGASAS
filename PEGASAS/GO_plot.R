args<-commandArgs(TRUE)
bg_list=args[2]#bg_list.txt
sg_list=args[3]
source(args[1])

background_gene_table <- read.table(bg_list)
outdir=args[4]#'Prostate_multidataset/oncogenic_sets'
system(paste0('mkdir -p ',outdir))
out_name=args[5]#'P53_PATHWAY'
observed_gene_table <- read.table(sg_list)
db_versions=unlist(strsplit(args[6],','))#GO_Biological_Process_2017b, GO_Cellular_Component_2015,GO_Molecular_Function_2017b
GO_BP_db=db_versions[1]
GO_CC_db=db_versions[2]
GO_MF_db=db_versions[3]
# Remove duplicates and put it in correct type for enrichR
background_gene_list <- unique(background_gene_table$V1)
observed_gene_list <- unique(observed_gene_table$V1)

GO_table <- get_enrichr_GO(background_gene_list, observed_gene_list, GO_BP_db, GO_CC_db, GO_MF_db)

save_GO_result(GO_table,output_dir=outdir, output_prefix=out_name)
# You can adjust the aspect ratio and bar width according to the size of the result 
pdf(file=paste0(outdir,'/','GO_top_chart_',out_name,'.pdf',sep=''), width=10, height=7)
generate_go_plot_dev(GO_table, cutoff=0.05,num_top = 5,term_size=10, bar_width = 0.6, aspect_ratio = 1.2)
dev.off()

