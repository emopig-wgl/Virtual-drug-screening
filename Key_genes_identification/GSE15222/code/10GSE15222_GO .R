
# ---------------------------
# 1. 加载依赖包（你已安装）
# ---------------------------
library(clusterProfiler)
library(org.Hs.eg.db)
library(dplyr)
library(readr)
library(circlize)
library(ComplexHeatmap)
library(grid)


# ---------------------------
# 2. 读取差异表达文件
# ---------------------------
input_file <- "C:/Users/lenovo/Desktop/文章4/数据集筛选/筛选重复基因/GSE15222/GSE15222_DEGs_limma.csv"
deg <- read_csv(input_file)

logFC_col <- colnames(deg)[1]
gene_col  <- colnames(deg)[ncol(deg)]

deg2 <- deg %>%
  dplyr::select(all_of(logFC_col), all_of(gene_col)) %>%
  dplyr::rename(logFC = all_of(logFC_col),
                gene  = all_of(gene_col)) %>%
  dplyr::filter(!is.na(gene)) %>%
  dplyr::filter(gene != "") %>%
  distinct(gene, .keep_all = TRUE)

cat("Input genes:", nrow(deg2), "\n")


# ---------------------------
# 3. SYMBOL -> ENTREZID 转换
# ---------------------------
gene_df <- bitr(deg2$gene,
                fromType = "SYMBOL",
                toType   = "ENTREZID",
                OrgDb    = org.Hs.eg.db)

deg3 <- merge(deg2, gene_df, by.x = "gene", by.y = "SYMBOL")

cat("Mapped genes (SYMBOL -> ENTREZID):", nrow(deg3), "\n")


# ---------------------------
# 4. GO富集分析（BP）
# ---------------------------
ego <- enrichGO(gene          = deg3$ENTREZID,
                OrgDb         = org.Hs.eg.db,
                keyType       = "ENTREZID",
                ont           = "BP",
                pAdjustMethod = "BH",
                pvalueCutoff  = 0.05,
                qvalueCutoff  = 0.05)

ego <- setReadable(ego, OrgDb = org.Hs.eg.db, keyType = "ENTREZID")
ego_res <- as.data.frame(ego)

if (nrow(ego_res) == 0) {
  stop("No significant GO terms found.")
}

cat("Significant GO terms:", nrow(ego_res), "\n")


# ---------------------------
# 5. 选Top10通路（按p.adjust）
# ---------------------------
ego_top <- ego_res %>%
  arrange(p.adjust) %>%
  slice_head(n = 10)

cat("Top pathways used:", nrow(ego_top), "\n")


# ---------------------------
# 6. 构建 Pathway-Gene-logFC 表
# ---------------------------
df_links <- data.frame()

for(i in 1:nrow(ego_top)){
  pathway <- ego_top$Description[i]
  genes <- unique(unlist(strsplit(ego_top$geneID[i], "/")))
  
  tmp <- data.frame(Pathway = pathway, Gene = genes)
  df_links <- rbind(df_links, tmp)
}

gene_fc <- deg3[, c("gene", "logFC")]
colnames(gene_fc) <- c("Gene", "logFC")

df_links <- merge(df_links, gene_fc, by = "Gene")
df_links <- unique(df_links)


# ---------------------------
# 7. 让图更干净（每条通路只保留变化最大的前8个基因）
# ---------------------------
df_links <- df_links %>%
  group_by(Pathway) %>%
  arrange(desc(abs(logFC))) %>%
  slice_head(n = 8) %>%   # 可调，越小越干净
  ungroup()

cat("Total links used:", nrow(df_links), "\n")


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
# 10. 绘制弦图并加入双Legend
# ---------------------------
output_pdf <- "C:/Users/lenovo/Desktop/GOPHOTO/GSE15222GOChord_plot_clean.pdf"

pdf(output_pdf, width = 13, height = 8)

circos.clear()
circos.par(start.degree = 90,
           gap.degree = 3,
           track.margin = c(0.01, 0.01))

chordDiagram(mat,
             grid.col = grid.col,
             transparency = 0.55,
             annotationTrack = "grid",
             preAllocateTracks = 1)

# 添加标签（基因小字，通路稍大）
circos.trackPlotRegion(track.index = 1, panel.fun = function(x, y) {
  sector.name <- get.cell.meta.data("sector.index")
  xlim <- get.cell.meta.data("xlim")
  ylim <- get.cell.meta.data("ylim")
  
  if(sector.name %in% pathways){
    circos.text(mean(xlim), ylim[1] + 0.1, sector.name,
                facing = "clockwise",
                niceFacing = TRUE,
                adj = c(0, 0.5),
                cex = 0.75)
  } else {
    circos.text(mean(xlim), ylim[1] + 0.1, sector.name,
                facing = "clockwise",
                niceFacing = TRUE,
                adj = c(0, 0.5),
                cex = 0.45)
  }
}, bg.border = NA)

title("GO Biological Process enrichment (Top 10 pathways)")

# --- legend 1 log2FC
lgd_fc <- Legend(
  title = "log2FC",
  col_fun = col_fun,
  at = round(c(min(fc_vals), 0, max(fc_vals)), 2)
)

# --- legend 2 pathway
lgd_path <- Legend(
  title = "Pathway",
  labels = pathways,
  legend_gp = gpar(fill = path_colors),
  labels_gp = gpar(fontsize = 9)
)

draw(packLegend(lgd_fc, lgd_path),
     x = unit(0.82, "npc"),
     y = unit(0.55, "npc"),
     just = c("left", "center"))

dev.off()

cat("Saved clean chord plot:", output_pdf, "\n")


# ---------------------------
# 11. 保存富集结果表格
# ---------------------------
write.csv(ego_res,
          "C:/Users/lenovo/Desktop/文章4/数据集筛选/筛选重复基因/GSE15222/GO_enrichment_results.csv",
          row.names = FALSE)

cat("GO enrichment table saved as: GO_enrichment_results.csv\n")

# ============================================================
# 12. 绘制标准气泡图（参照 KEGG dotplot 风格）
# 绘制 GO 气泡图（符合三个核心要求）
# 1. 气泡大小标注：2,4,6,8,10,12（整数）
# 2. 颜色渐变有标注（Pvalue）
# 3. 横轴合理，图不宽
# ============================================================

library(ggplot2)

# 使用 Top10 通路结果
bubble_data <- ego_top

# 按 pvalue 排序（最显著在上方）
bubble_data <- bubble_data[order(bubble_data$pvalue, decreasing = FALSE), ]
bubble_data$Description <- factor(bubble_data$Description, 
                                  levels = rev(bubble_data$Description))

# 绘制气泡图
p_bubble <- ggplot(bubble_data, 
                   aes(x = Count, 
                       y = Description, 
                       size = Count, 
                       color = pvalue)) +
  geom_point(alpha = 0.8) +
  
  # 颜色渐变标注（Pvalue）
  scale_color_gradient(
    low = "red", 
    high = "blue",
    name = "Pvalue",
    breaks = c(0.01, 0.02, 0.03, 0.04, 0.05),
    labels = c("0.01", "0.02", "0.03", "0.04", "0.05")
  ) +
  
  # 气泡大小标注（2,4,6,8,10,12）
  scale_size_continuous(
    name = "Gene count",
    breaks = c(2, 4, 6, 8, 10, 12),
    labels = c("2", "4", "6", "8", "10", "12"),
    range = c(3, 10)
  ) +
  
  # 横轴设置
  scale_x_continuous(
    breaks = seq(0, max(bubble_data$Count), by = 2)
  ) +
  
  # 标签
  labs(
    title = "GO Biological Process Enrichment",
    x = "Gene Count",
    y = "Pathway"
  ) +
  
  # 主题
  theme_bw() +
  theme(
    axis.text.y = element_text(size = 12),
    axis.text.x = element_text(size = 10),
    axis.title.x = element_text(size = 12),
    axis.title.y = element_text(size = 12),
    plot.title = element_text(hjust = 0.5, size = 14),
    legend.text = element_text(size = 10),
    legend.title = element_text(size = 12)
  )

# 保存图片
ggsave(
  filename = "C:/Users/lenovo/Desktop/GOPHOTO/GSE15222_GO_bubble_chart.png",
  plot = p_bubble,
  width = 8,
  height = 6,
  dpi = 600
)

# 输出确认信息
cat("✓ 气泡图已保存\n")
cat("  - 气泡大小标注: 2, 4, 6, 8, 10, 12\n")
cat("  - 颜色标注: Pvalue (红→蓝)\n")