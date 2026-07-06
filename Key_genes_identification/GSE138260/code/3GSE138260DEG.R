############################
## 1. 环境与库
############################

setwd("C:/Users/lenovo/Desktop/文章4/数据集筛选/GSE138260")

library(GEOquery)
library(data.table)
library(dplyr)
library(ggplot2)
library(limma)

############################
## 2. 从 series_matrix.txt 读取样本分组信息
############################

gse <- getGEO(
  filename = "GSE138260_series_matrix.txt/GSE138260_series_matrix.txt",
  getGPL = FALSE
)

pdata <- pData(gse)

group <- ifelse(
  grepl("AD|Alzheimer", pdata$title, ignore.case = TRUE),
  "AD",
  "control"
)

group <- factor(group, levels = c("control", "AD"))
names(group) <- pdata$geo_accession

table(group)

############################
## 3. 读取你已有的 HUGO + log2 表达矩阵
############################

expr <- fread(
  "GSE138260_HUGO_expression.csv",
  data.table = FALSE
)

rownames(expr) <- expr[, 1]
expr <- expr[, -1]
expr <- as.matrix(expr)

############################
## 4. 对齐表达矩阵与分组信息
############################

expr <- expr[, colnames(expr) %in% names(group)]
expr <- expr[, names(group)]

############################
## 5. limma 差异表达分析
############################

design <- model.matrix(~ group)
fit <- lmFit(expr, design)
fit <- eBayes(fit)

DEG <- topTable(
  fit,
  coef = "groupAD",
  number = Inf,
  adjust.method = "BH"
)

############################
## 6. DEG 筛选
############################

logFC_cutoff <- 0.8
P.Value <- 0.05

DEG_result <- DEG

k1 <- (DEG_result$P.Value < P.Value) &
  (DEG_result$logFC < -logFC_cutoff)

k2 <- (DEG_result$P.Value < P.Value) &
  (DEG_result$logFC >  logFC_cutoff)

DEG_result <- DEG_result %>%
  mutate(
    change = ifelse(
      k1, "down",
      ifelse(k2, "up", "stable")
    )
  )

filtered_DEG_result <- DEG_result %>%
  filter(change != "stable")

filtered_DEG_result$geneName <- rownames(filtered_DEG_result)

############################
## 7. 保存 DEG 结果
############################

write.csv(
  filtered_DEG_result,
  file = "GSE138260_DEGs_limma.csv",
  row.names = FALSE,
  fileEncoding = "UTF-8"
)

############################
## 8. 火山图
############################

p <- ggplot(
  DEG_result,
  aes(x = logFC, y = -log10(P.Value), color = change)
) +
  geom_point(alpha = 0.6, size = 2) +
  scale_color_manual(values = c("blue4", "grey", "red3")) +
  geom_vline(xintercept = c(-logFC_cutoff, logFC_cutoff),
             lty = 4, col = "black") +
  geom_hline(yintercept = -log10(P.Value),
             lty = 4, col = "black") +
  theme_bw() +
  labs(
    title = "GSE138260 Differential Expression (limma)",
    x = "log2 Fold Change",
    y = "-log10(P value)"
  )

ggsave(
  filename = "GSE138260_volcano_limma.png",
  plot = p,
  width = 6,
  height = 5
)

ggsave(
  filename = "GSE138260_volcano_limma.pdf",
  plot = p,
  width = 6,
  height = 5
)
