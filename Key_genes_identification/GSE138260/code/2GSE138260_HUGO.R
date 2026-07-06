# 1 设置当前数据集文件夹
setwd("C:/Users/lenovo/Desktop/文章4/数据集筛选/GSE138260")

# 2 读取已经转换好的探针表达矩阵
expr <- read.csv("GSE138260.csv", row.names = 1, check.names = FALSE)

# 3 从本地文件读取平台信息
gpl <- getGEO(filename = "GPL27556_family.soft.gz")
gpl_table <- Table(gpl)

# 4 提取探针→基因（HUGO）映射
mapping <- gpl_table[, c("ID", "GENE_SYMBOL")]
mapping <- mapping[mapping$GENE_SYMBOL != "" & !is.na(mapping$GENE_SYMBOL), ]

# 5 合并表达矩阵与注释
mapping <- mapping[!duplicated(mapping$ID), ]
expr$ID <- rownames(expr)
expr_annot <- merge(mapping, expr, by = "ID")

# 6 去除不能映射的 probe（修改这里：使用GENE_SYMBOL）
expr_annot <- expr_annot[expr_annot$GENE_SYMBOL != "", ]

# 7 合并同一基因 name 的多个探针（按平均值）（修改这里：使用GENE_SYMBOL）
expr_HUGO <- aggregate(. ~ GENE_SYMBOL, 
                       data = expr_annot[, -1],  # 排除ID列
                       FUN = mean)

# 8 保存结果
write.csv(expr_HUGO, "GSE138260_HUGO_expression.csv", row.names = FALSE)
