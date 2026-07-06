# 1 设置当前数据集文件夹
setwd("C:/Users/lenovo/Desktop/文章4/数据集筛选/GSE4226")

# 2 读取已经转换好的探针表达矩阵
expr <- read.csv("GSE4226.csv", row.names = 1, check.names = FALSE)

# 3 下载对应平台
gpl <- getGEO("GPL1211", AnnotGPL = TRUE)
gpl_table <- Table(gpl)

# 4 提取探针→基因（HUGO）映射
mapping <- gpl_table[, c("ID", "Gene symbol")]
mapping <- mapping[mapping$`Gene symbol` != "" & !is.na(mapping$`Gene symbol`), ]

# 5 合并表达矩阵与注释
mapping <- mapping[!duplicated(mapping$ID), ]
expr$ID <- rownames(expr)
expr_annot <- merge(mapping, expr, by = "ID")

# 6 去除不能映射的 probe
expr_annot <- expr_annot[expr_annot$`Gene symbol` != "", ]

# 7 合并同一基因 name 的多个探针（按平均值）
expr_HUGO <- aggregate(. ~ `Gene symbol`, 
                       data = expr_annot[, -1], 
                       FUN = mean)

# 8 保存结果
write.csv(expr_HUGO, "GSE4226_HUGO_expression.csv", row.names = FALSE)
