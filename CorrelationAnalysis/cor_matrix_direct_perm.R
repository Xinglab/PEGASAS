args<-commandArgs(TRUE)
#Loading matrix
library('LSD')
library('data.table')
signature=args[1]#'Prostate_multidataset/SMALL_CELL/SMALL_CELL.sorted.txt'
PSImatrix=args[2]#'Prostate_multidataset/SMALL_CELL' #sometime equals to dataset
folder=args[3]#'Prostate_multidataset/SMALL_CELL/refinedBySample.stdNull.na0.99.cov10.splcing.merged_matrix.tissue.SMALL_CELL.sorted.txt'
analysis_prefix=unlist(strsplit(tail(unlist(strsplit(signature,'\\/')),1),'\\.sorted.txt'))[1]

matrix1=as.matrix(fread(signature), header=T,skip = 0)
matrix2=as.matrix(fread(PSImatrix), header=T,skip = 0)
matrix11=as.matrix(as.numeric(matrix1[,-1]))
matrix22=apply(matrix2[,c(0:-8)],2,as.numeric)

#permutation function
cor.perm.test <- function(x, y, N=5000, plot=F){
  obs <- cor(x,y,use='pairwise.complete.obs')
  reps <- replicate(200, cor(sample(x), y,use='pairwise.complete.obs'))
  p <-min(mean(obs>=reps),mean(obs<=reps)) # shortcut for sum(reps > obs)/N
  if (N>200 & p<0.2){
    reps_new<-replicate(800, cor(sample(x), y,use='pairwise.complete.obs'))
    reps<-c(reps,reps_new)
    p <-min(mean(obs>=reps),mean(obs<=reps))
  }
  if (N>1000 & p<0.04){
    reps_new<-replicate(N-1000, cor(sample(x), y,use='pairwise.complete.obs'))
    reps<-c(reps,reps_new)
    p <-min(mean(obs>=reps),mean(obs<=reps))
  }
  if(plot){
    hist(as.numeric(reps),xlim=c(-abs(obs),abs(obs)))
    abline(v=obs, col="red")
  }
  p
}


#making plots
pdf(paste(folder,'/',matrix1[1,1],"_high_cor_scatterplots.pdf",sep=""), onefile = TRUE)

#Calculating
cor <- c()
correlated=c()
cor_p<-c()
p_keep <- c()
cor_keep <- c()

#for (i in 1:10){
for (i in 1:nrow(matrix22)){
  c.i <- cor(matrix11[,1],as.vector(matrix22[i,]),use="pairwise.complete.obs",method = "pearson")
  cor<-c(cor,c.i)
  if (!is.na(c.i) & abs(as.numeric(c.i)) > 0.3){
#    print(i)
    cor_p<-tryCatch({
      cor_p<-cor.perm.test(matrix11[,1],matrix22[i,])},error=function(e){NA})
    if (!is.na(cor_p) ){
      if (cor_p < 0.0002){# get rid of low samples but high cor events.
        s_long=paste(matrix2[i,2],matrix2[i,3],matrix2[i,4],matrix2[i,5],matrix2[i,6],matrix2[i,7],matrix2[i,8],sep="_")
        s_long=paste0(unlist(strsplit(s_long, split=' ', fixed=TRUE)),collapse = "")
        s=paste(matrix2[i,2],matrix2[i,3],matrix2[i,4],matrix2[i,5],matrix2[i,6],sep="_")
        s=paste0(unlist(strsplit(s, split=' ', fixed=TRUE)),collapse = "")
        correlated <- c(correlated,s_long)
        p_keep <- c(p_keep,as.numeric(cor_p))
        cor_keep <- c(cor_keep,as.numeric(cor[i]))
        cor_p_lab=format(cor_p,scientific = T)
        if (cor_p==0){cor_p_lab='<1E-3'}
        heatscatter(matrix11[,1],matrix22[i,],
                    xlab=paste(matrix1[1,1],' GSEA Score (K-S statistic)\nPearson\'s corr coef:',round(cor[i],digit=3),
                               '\tp-value:',cor_p_lab,sep=""),
                    ylab='' ,ylim=c(0,1),main=paste(strwrap(s, width = 40), collapse = "\n"),
                    cex.main=1,cex.lab=0.95, cex.axis=0.8, font.lab=2, font.main=2)
        mtext(expression(italic(psi)), side=2, line=2,cex=1.3, font=2)
        abline(lm(matrix22[i,]~matrix11[,1]))
      }
    }}
}
dev.off()

cor <- cbind(matrix2[,c(2:8)],cor)
#colnames(cor) <- c("ENSG","Corelation")
remain <- cbind(correlated,cor_keep,p_keep)

write.table(remain, file = paste(folder,'/',analysis_prefix,'_high_cor_matrix.txt',sep=""),row.names=F,quote = F,sep='\t')
write.table(cor, file = paste(folder,'/',analysis_prefix,'_global_cor_matrix.txt',sep=""),row.names=F,quote = F,sep='\t')


