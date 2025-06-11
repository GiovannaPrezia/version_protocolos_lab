# ──────────────────────────────────────────────────────────────
# R Script Completo DESeq2 + PCA + Volcano + Heatmap
# Projeto: Câncer de Mama – MCF10A (normais) vs MCF7 (luminal A)
# Observações:
# - Altere os caminhos conforme seu projeto
# - Use apenas amostras com replicatas para DESeq2
# ──────────────────────────────────────────────────────────────

# 1) Pacotes
if (!requireNamespace("BiocManager", quietly=TRUE)) install.packages("BiocManager")
if (!requireNamespace("DESeq2", quietly=TRUE)) BiocManager::install("DESeq2")
if (!requireNamespace("pheatmap", quietly=TRUE)) install.packages("pheatmap")
if (!requireNamespace("ggplot2", quietly=TRUE)) install.packages("ggplot2")
if (!requireNamespace("biomaRt", quietly=TRUE)) BiocManager::install("biomaRt")

library(DESeq2)
library(pheatmap)
library(ggplot2)
library(biomaRt)

# 2) Leitura da matriz de contagem (ajuste se necessário)
counts <- read.table("~/disk1/data/Bernardo_2/counts/counts_matrix.txt", header=TRUE, row.names=1, sep="\t", comment.char="#")
counts <- counts[, sapply(counts, is.numeric)]

# 3) Metadados das amostras
sample_info <- data.frame(
  row.names = colnames(counts),
  condition = c(
    "control", "control", "control", "control", "control", "control",  # MCF10A_1,2,3,4,6,7
    "cancer", "cancer", "cancer"                                       # MCF7_BCC1,2,3
  )
)

# 4) Criar objeto DESeq2
dds <- DESeqDataSetFromMatrix(countData = counts, colData = sample_info, design = ~ condition)
dds <- dds[rowSums(counts(dds)) > 10, ]
dds <- DESeq(dds)

# 5) PCA
vsd <- vst(dds, blind=TRUE)
pcaData <- plotPCA(vsd, intgroup="condition", returnData=TRUE)
ggpca <- ggplot(pcaData, aes(PC1, PC2, color=condition)) +
  geom_point(size=3) + theme_minimal() + ggtitle("PCA - Câncer de Mama")
ggsave("PCA_CancerMama.png", ggpca, width=6, height=5)

# 6) Anotação de genes com biomaRt
annotate_genes <- function(df) {
  df$GeneID <- rownames(df)
  mart <- useMart("ensembl", dataset="hsapiens_gene_ensembl")
  map <- getBM(attributes=c("ensembl_gene_id", "hgnc_symbol"),
               filters="ensembl_gene_id", values=df$GeneID, mart=mart)
  colnames(map) <- c("GeneID", "GeneName")
  merged <- merge(df, map, by="GeneID", all.x=TRUE)
  merged$GeneName[is.na(merged$GeneName) | merged$GeneName==""] <- merged$GeneID[is.na(merged$GeneName) | merged$GeneName==""]
  return(merged)
}

# 7) Exportar tabela de contagens com nomes de genes
write.csv(annotate_genes(as.data.frame(counts(dds))),
          "Counts_CancerMama_AllSamples_GeneNames.csv", row.names=FALSE)

# 8) Resultados do DESeq2
res <- results(dds)
res_df <- as.data.frame(res)
res_df <- annotate_genes(res_df)
write.csv(res_df[, c("GeneName", "baseMean", "log2FoldChange", "lfcSE", "stat", "pvalue", "padj")],
          "DESeq2_CancerMama_FullResults.csv", row.names=FALSE)

# 9) Genes significativos (padj < 0.05)
sig <- res_df[!is.na(res_df$padj) & res_df$padj < 0.05, ]
write.csv(sig, "DESeq2_CancerMama_SignificantGenes.csv", row.names=FALSE)

# 10) Heatmap dos top 30 genes mais variáveis
rld <- rlog(dds, blind=TRUE)
top_var_genes <- head(order(rowVars(assay(rld)), decreasing=TRUE), 30)
pheatmap(assay(rld)[top_var_genes, ],
         scale="row",
         annotation_col=sample_info,
         main="Top 30 Variable Genes")

# 11) Volcano plot
res_df$significance <- "ns"
res_df$significance[res_df$padj < 0.05 & abs(res_df$log2FoldChange) >= 1] <- "Significant"

volcano <- ggplot(res_df, aes(log2FoldChange, -log10(pvalue), color=significance)) +
  geom_point(size=2, alpha=0.8) +
  scale_color_manual(values=c("ns"="gray", "Significant"="red")) +
  labs(title="Volcano Plot – Câncer de Mama", x="log2FC", y="-log10(p-value)") +
  theme_minimal()
ggsave("Volcano_CancerMama.png", volcano, width=7, height=5)
