# ---------------------------
# 1. 加载依赖包
# ---------------------------
library(clusterProfiler)
library(org.Hs.eg.db)
library(dplyr)
library(readr)
library(circlize)
library(ComplexHeatmap)
library(grid)
library(ggplot2)
library(stringr)


# ---------------------------
# 2. 读取差异表达文件
# ---------------------------
input_file <- "C:/Users/lenovo/Desktop/文章4/数据集筛选/筛选重复基因/GSE4757/GSE4757_DEGs_limma_split.csv"
deg <- read_csv(input_file)

logFC_col <- colnames(deg)[1]
gene_col  <- colnames(deg)[ncol(deg)]   # geneName
pval_col  <- colnames(deg)[4]           # P.Value

deg2 <- deg %>%
  dplyr::select(all_of(logFC_col), all_of(gene_col)) %>%
  dplyr::rename(logFC = all_of(logFC_col),
                gene  = all_of(gene_col)) %>%
  dplyr::filter(!is.na(gene)) %>%
  dplyr::filter(gene != "") %>%
  distinct(gene, .keep_all = TRUE)

cat("Input genes:", nrow(deg2), "\n")


# ---------------------------
# 3. 只使用 Key Genes 做富集分析
# ---------------------------
key_genes <- c("TYROBP", "NLRP3", "CASP1", "MYH1", "MYLPF", "VAV1")

deg_key <- deg %>%
  dplyr::select(all_of(logFC_col), all_of(gene_col)) %>%
  dplyr::rename(logFC = all_of(logFC_col),
                gene  = all_of(gene_col)) %>%
  dplyr::filter(gene %in% key_genes) %>%
  distinct(gene, .keep_all = TRUE)

cat("Key genes found in DEG file:", nrow(deg_key), "\n")
print(deg_key$gene)

if(nrow(deg_key) == 0){
  stop("None of the key genes were found in DEG file.")
}

# ---------------------------
# 4. SYMBOL -> ENTREZID 转换
# ---------------------------
gene_df_key <- bitr(deg_key$gene,
                    fromType = "SYMBOL",
                    toType   = "ENTREZID",
                    OrgDb    = org.Hs.eg.db)

deg_key2 <- merge(deg_key, gene_df_key, by.x = "gene", by.y = "SYMBOL")

cat("Mapped key genes (SYMBOL -> ENTREZID):", nrow(deg_key2), "\n")


# ---------------------------
# 5. GO富集分析（BP）
# ---------------------------
ego <- enrichGO(gene          = deg_key2$ENTREZID,
                OrgDb         = org.Hs.eg.db,
                keyType       = "ENTREZID",
                ont           = "BP",
                pAdjustMethod = "BH",
                pvalueCutoff  = 0.05,
                qvalueCutoff  = 0.05)

ego <- setReadable(ego, OrgDb = org.Hs.eg.db, keyType = "ENTREZID")
ego_res <- as.data.frame(ego)

if (nrow(ego_res) == 0) {
  stop("No significant GO terms found for key genes.")
}

cat("Significant GO terms:", nrow(ego_res), "\n")


# ---------------------------
# 6. 选Top10通路（按p.adjust）
# ---------------------------
ego_top <- ego_res %>%
  arrange(p.adjust) %>%
  slice_head(n = 10)

cat("Top pathways used:", nrow(ego_top), "\n")


# ---------------------------
# 7. 构建 Pathway-Gene-logFC 表
# ---------------------------
df_links <- data.frame()

for(i in 1:nrow(ego_top)){
  pathway <- ego_top$Description[i]
  genes <- unique(unlist(strsplit(ego_top$geneID[i], "/")))
  
  tmp <- data.frame(Pathway = pathway, Gene = genes)
  df_links <- rbind(df_links, tmp)
}

# 只保留 key genes
df_links <- df_links %>%
  dplyr::filter(Gene %in% key_genes)

# logFC 从原deg_key中取
gene_fc <- deg_key2[, c("gene", "logFC")]
colnames(gene_fc) <- c("Gene", "logFC")

df_links <- merge(df_links, gene_fc, by = "Gene")
df_links <- unique(df_links)

cat("Total links used:", nrow(df_links), "\n")

if(nrow(df_links) == 0){
  stop("No gene-pathway links remained after filtering key genes.")
}


# ---------------------------
# 8. 构建 chord matrix
# ---------------------------
mat <- table(df_links$Gene, df_links$Pathway)


# ---------------------------
# 9. 设置颜色（logFC连续渐变 + pathway离散颜色）
# ---------------------------
fc_vals <- df_links$logFC

col_fun <- colorRamp2(
  c(min(fc_vals), 0, max(fc_vals)),
  c("#2C7BB6", "white", "#D7191C")
)

gene_colors <- setNames(col_fun(df_links$logFC), df_links$Gene)

pathways <- unique(df_links$Pathway)
path_colors <- setNames(rainbow(length(pathways)), pathways)

grid.col <- c(gene_colors, path_colors)


# ---------------------------
# 统一字体参数
# ---------------------------
gene_cex         <- 0.95
legend_title_fs  <- 15
legend_label_fs  <- 13

bubble_axis_fs  <- 12
bubble_y_fs     <- 12
bubble_title_fs <- 13
bubble_legend_fs <- 11


# ---------------------------
# 10. 绘制弦图（Key Genes版）
# ---------------------------
output_pdf <- "C:/Users/lenovo/Desktop/GOPHOTO/GSE4757GOChord_plot_KEYGENES.pdf"

pdf(output_pdf, width = 12, height = 8)

circos.clear()

circos.par(start.degree = 90,
           gap.degree = 3,
           track.margin = c(0.01, 0.01),
           cell.padding = c(0, 0, 0, 0),
           canvas.xlim = c(-1.35, 1.55),
           canvas.ylim = c(-1.25, 1.25))

chordDiagram(mat,
             grid.col = grid.col,
             transparency = 0.55,
             annotationTrack = "grid",
             preAllocateTracks = list(track.height = 0.14))

# 只显示基因名称，去掉顶部标题，仅调大字体
circos.trackPlotRegion(track.index = 1, panel.fun = function(x, y) {
  
  sector.name <- get.cell.meta.data("sector.index")
  xlim <- get.cell.meta.data("xlim")
  ylim <- get.cell.meta.data("ylim")
  
  if(!(sector.name %in% pathways)){
    circos.text(mean(xlim), ylim[1] + 0.08, sector.name,
                facing = "clockwise",
                niceFacing = TRUE,
                adj = c(0, 0.5),
                cex = gene_cex)
  }
  
}, bg.border = NA)

# legend 1 log2FC
lgd_fc <- Legend(
  title = "log2FC",
  col_fun = col_fun,
  at = round(c(min(fc_vals), 0, max(fc_vals)), 2),
  title_gp = gpar(fontsize = legend_title_fs, fontface = "bold"),
  labels_gp = gpar(fontsize = legend_label_fs)
)

# legend 2 pathway
pathways_wrapped <- stringr::str_wrap(pathways, width = 22)

lgd_path <- Legend(
  title = "Pathway",
  labels = pathways_wrapped,
  legend_gp = gpar(fill = path_colors),
  title_gp = gpar(fontsize = legend_title_fs, fontface = "bold"),
  labels_gp = gpar(fontsize = legend_label_fs)
)

draw(packLegend(lgd_fc, lgd_path),
     x = unit(0.72, "npc"),
     y = unit(0.5, "npc"),
     just = c("left", "center"))

dev.off()

cat("Saved clean chord plot:", output_pdf, "\n")


# ---------------------------
# 11. 保存富集结果表格
# ---------------------------
write.csv(ego_res,
          "C:/Users/lenovo/Desktop/文章4/数据集筛选/筛选重复基因/GSE4757/GO_enrichment_results.csv",
          row.names = FALSE)

cat("GO enrichment table saved as: GO_enrichment_results.csv\n")


# ============================================================
# 12. 气泡图（横轴GeneRatio，颜色p.adjust）
# ============================================================

bubble_data <- ego_top

# GeneRatio 转换为数值
bubble_data <- bubble_data %>%
  mutate(GeneRatio_num = sapply(GeneRatio, function(x){
    as.numeric(strsplit(x, "/")[[1]][1]) / as.numeric(strsplit(x, "/")[[1]][2])
  }))

# 对通路名称换行，避免左侧太宽
bubble_data$Description_wrap <- stringr::str_wrap(bubble_data$Description, width = 26)

# 排序
bubble_data <- bubble_data[order(bubble_data$Count, decreasing = FALSE), ]
bubble_data$Description_wrap <- factor(bubble_data$Description_wrap,
                                       levels = bubble_data$Description_wrap)

p_bubble <- ggplot(
  bubble_data,
  aes(x = GeneRatio_num,
      y = Description_wrap,
      size = Count,
      color = p.adjust)
) +
  geom_point(alpha = 0.9) +
  
  scale_color_gradientn(
    colours = c("red", "purple", "blue"),
    name = "p.adjust"
  ) +
  
  scale_size_continuous(
    name = "Count",
    breaks = c(2, 3),
    range = c(4, 8)
  ) +
  
  # 只保留 0.4、0.5、0.6，并把左右边界稍微卡紧
  scale_x_continuous(
    breaks = c(0.4, 0.5, 0.6),
    limits = c(0.39, 0.61),
    expand = expansion(mult = c(0.025, 0.025))
  ) +
  
  labs(
    title = NULL,
    x = "GeneRatio",
    y = NULL
  ) +
  
  theme_bw() +
  theme(
    axis.text.y = element_text(size = 18, colour = "black"),
    axis.text.x = element_text(size = 16, colour = "black"),
    axis.title.x = element_text(size = 20, face = "bold"),
    axis.title.y = element_text(size = 20, face = "bold"),
    
    plot.title = element_blank(),
    
    legend.text = element_text(size = 15),
    legend.title = element_text(size = 18, face = "bold"),
    
    panel.grid.major = element_line(colour = "#D0D0D0", linewidth = 0.5),
    panel.grid.minor = element_blank(),
    
    # 收紧整体边距，让图不要显得过宽
    plot.margin = margin(t = 8, r = 10, b = 8, l = 8),
    
    # 右侧图例适当缩短
    legend.key.height = unit(0.9, "cm"),
    legend.key.width  = unit(0.6, "cm")
  )

ggsave(
  filename = "C:/Users/lenovo/Desktop/GOPHOTO/GSE4757_GO_bubble_chart.png",
  plot = p_bubble,
  width = 6.8,
  height = 7.6,
  dpi = 600,
  bg = "white"
)

cat("✓ 气泡图已保存\n")
cat("  - 气泡颜色: p.adjust\n")
cat("  - 气泡大小: Count\n")
cat("  - X轴: GeneRatio\n")

