# ===============================
# 1. 环境准备
# ===============================
library(dplyr)
library(tidyr)
library(readr)

# ===============================
# 2. 读取 limma 差异分析结果
# ===============================
input_file  <- "C:/Users/lenovo/Desktop/文章4/数据集筛选/筛选重复基因/GSE1297/GSE1297_DEGs_limma.csv"
output_file <- "C:/Users/lenovo/Desktop/文章4/数据集筛选/筛选重复基因/GSE1297/GSE1297_DEGs_limma_split.csv"

deg <- read.csv(input_file, stringsAsFactors = FALSE)

# ===============================
# 3. 按 /// 拆分 geneName，并展开成多行
# ===============================
deg_split <- deg %>%
  separate_rows(geneName, sep = "///")

# ===============================
# 4. 导出新文件
# ===============================
write.csv(deg_split,
          file = output_file,
          row.names = FALSE)

cat("拆分完成，输出文件为：", output_file, "\n")
