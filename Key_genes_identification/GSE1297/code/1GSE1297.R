# Ensure BiocManager is installed
if(!requireNamespace("BiocManager", quietly = TRUE))
  install.packages("BiocManager")  #确保已将安装了BiocManager包

# Uncomment to install necessary packages
# BiocManager::install("limma")
# BiocManager::install("GEOquery")
# install.packages("devtools")
# devtools::install_github("BioSenior/ggVolcano")
getwd()
setwd("C:/Users/lenovo/Desktop/文章4/数据集筛选/GSE1297") #获取工作目录并更改为指定路径

# Load required libraries
library(GEOquery)
library(limma)
#library(ggVolcano)#加载这三个包

# Download data from GEO
eSet <- getGEO("GSE1297", destdir = ".", getGPL = T)
exprSet = exprs(eSet[[1]])
fdata = fData(eSet[[1]])
pdata = pData(eSet[[1]])
dim(exprSet)  
dim(fdata)
dim(pdata) #从GEO数据库下载指定的数据集（GSE1297），并提取表达矩阵、特征矩阵、样本数据，然后输出每个数据集的维度
write.csv(exprSet, file = "GSE1297.csv", row.names = TRUE)

