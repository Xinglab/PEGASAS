save_GO_result <- function(GO_result_table, output_dir, output_prefix){
  output_file = paste0(output_dir, "/", "GO_result_table_", output_prefix, ".txt")
  write.table(GO_result_table, output_file, sep = '\t')
  print(paste("The file is saved at:", output_file))
}

generate_go_plot_dev <- function(GO_result, cutoff = 0.05, aspect_ratio = 1.8, bar_width = 0.6, x_axis.tilt = 0, num_top = 10, term_size=10){
  total_sig_events <- data.frame(matrix(ncol = 7, nrow = 0)) # generate sig hits data frame for top events.
  colnames(total_sig_events) <- colnames(GO_result)
  
  for (process in c("BP", "CC", "MF")){
    library(ggplot2)
    significant_hits <- subset(GO_result, GO_process == process ) # subset events for each process
    # TODO - possibly this is the point where we can add the sort 
    significant_hits <- significant_hits[order(significant_hits$corrected_score),]
    significant_hits_cutoff <- subset(significant_hits, corrected_score < cutoff ) # select events below the cutoff p-value
    significant_hits_cutoff_bg_filter<- subset(significant_hits_cutoff, background_hit>=term_size)
    significant_hits_cutoff_bg_filter_top<- significant_hits_cutoff_bg_filter[1:min(num_top,dim(significant_hits_cutoff_bg_filter)[1]),]
    total_sig_events <- rbind(total_sig_events, significant_hits_cutoff_bg_filter_top)
  }
  
  significant_events_ordered <- total_sig_events[order(total_sig_events$GO_process),]
  significant_events_ordered$order = c(1:length(significant_events_ordered$Term)) # put order so that it will be in the order of processes
  # TODO - better plot implementation
  ggplot(significant_events_ordered, aes(x = reorder(Term, -order), y = -log10(corrected_score), fill = GO_process)) + 
    # geom_col(aes(alpha = log10(interest_hit)), width = bar_width)+  
    geom_col( width = bar_width)+
    # facet_grid(.~GO_process) +
    theme(axis.text.x = element_text(hjust=0, size=13,face = "bold"), axis.text = element_text(size=13,face = "bold")) +
    xlab("GO Terms") +
    ylab("-log10(adj p-value)") + 
    theme(aspect.ratio = aspect_ratio)+
    geom_hline(yintercept = -log10(0.05), linetype = "dashed") + 
    theme(panel.background = element_blank())+
    theme(axis.text.x=element_text(angle = x_axis.tilt, hjust=0)) +
    theme(axis.title.x = element_text(size=14,face="bold"),axis.title.y = element_text(face="bold",size=14))+
    theme(legend.position = "bottom",legend.title = element_text(size=14,face="bold"),legend.text= element_text(size=14,face="bold")) + 
    scale_x_discrete(labels = function(x) lapply(strwrap(x, width = 70, simplify = FALSE), paste, collapse="\n"), position = "top") +
    coord_flip() 
  
}

get_enrichr_GO <- function(all_gene_list, significant_genes){
  GO_processes = c("BP", "CC", "MF")
  merged_GO_result <- list()
  for (process in GO_processes){
    recalculated_GO_result = recalculate_GO(all_gene_list, significant_genes, process)
    merged_GO_result <- rbind(recalculated_GO_result, merged_GO_result)
  }
  merged_GO_result
}

recalculate_GO <- function(all_gene_list, significant_genes, GO_process = "BP") {
  library(enrichR)
  if (GO_process == "BP") {
    go_db = "GO_Biological_Process_2017b"
  }  else if (GO_process == "CC"){
    go_db = "GO_Cellular_Component_2015"
  }  else if (GO_process == "MF"){
    go_db = "GO_Molecular_Function_2017b"
  }
  all_gene_GO <- enrichr(as.vector(all_gene_list), databases = go_db)
  sig_gene_GO <- enrichr(as.vector(significant_genes), databases = go_db)
  
  bg_numbers <- as.data.frame(cbind(all_gene_GO[[go_db]]$Term, sapply(strsplit(as.character(all_gene_GO[[go_db]]$Overlap), '/'), '[', 1)), stringsAsFactors = FALSE)
  colnames(bg_numbers) = c("Term", "Overlap_number")
  rownames(bg_numbers) <- bg_numbers$Term
  
  sig_numbers <- as.data.frame(cbind(sig_gene_GO[[go_db]]$Term, sapply(strsplit(as.character(sig_gene_GO[[go_db]]$Overlap), '/'), '[', 1)), stringsAsFactors = FALSE)
  colnames(sig_numbers) <- c("Term", "Overlap_number")
  rownames(sig_numbers) <- sig_numbers$Term
  
  corrected_score <- sapply(sig_numbers$Term, function(x) get_hypergeometric_values(x, sig_numbers, bg_numbers, all_gene_list, significant_genes))
  names(corrected_score) <- sig_numbers$Term
  
  # remove NA 
  corrected_score <- corrected_score[!is.na(corrected_score)]
  
  # FDR Correction
  corrected_score_after_fdr <- p.adjust(corrected_score, method = "fdr") 
  
  # formatting 
  corrected_numbers <- cbind(as.numeric(as.character(sig_numbers[names(corrected_score_after_fdr),]$Overlap_number)), as.numeric(as.character(bg_numbers[names(corrected_score_after_fdr),]$Overlap_number)))
  colnames(corrected_numbers) <- c("Sig_event_num", "Background_event_num")
  rownames(corrected_numbers) <- sig_numbers[names(corrected_score_after_fdr),]$Term
  
  corrected_genes <- sig_gene_GO[[go_db]][sig_gene_GO[[go_db]]$Term %in% rownames(corrected_numbers),]$Genes
  
  info_table <- cbind(rownames(corrected_numbers), corrected_numbers, data.frame(corrected_score), data.frame(corrected_score_after_fdr), corrected_genes)  
  head(info_table)
  colnames(info_table) <- c("Term", "interest_hit", "background_hit", "corrected_score", "adjusted_corrected_score", "Genes")
  info_table$GO_process = GO_process
  info_table
}

get_hypergeometric_values <- function (term, sig_num, bg_num, all_gene_list, sig_gene_list)  {
  term_bg <- as.numeric(as.character(bg_num[term,]$Overlap_number))
  if (term_bg >= 5){
    term_obs <- as.numeric(as.character(sig_num[term,]$Overlap_number))
    term_bg <- as.numeric(as.character(bg_num[term,]$Overlap_number))
    total_bg <- length(all_gene_list)
    total_obs <- length(sig_gene_list)
    # pval=hypergeom.sf(term_obs,tot_bg,term_bg,tot_obs)
    # sf(x, M, n, N, loc=0)
    updated_p_value = 1 - phyper(term_obs, term_bg, total_bg - term_bg, total_obs, lower.tail = TRUE)
    updated_p_value  
  }
  else{
    # print("WRONG ")
    NA
  }
}
