import pandas as pd
import glob
# 定义文件名列表
file_names = [
    'C:/Users/lenovo/Desktop/文章4/数据集筛选/筛选重复基因/GSE138260/top_25_nodes_0.15.csv',
    'C:/Users/lenovo/Desktop/文章4/数据集筛选/筛选重复基因/GSE138260/top_25_nodes_0.4.csv',
    'C:/Users/lenovo/Desktop/文章4/数据集筛选/筛选重复基因/GSE138260/top_25_nodes_0.7.csv',
    'C:/Users/lenovo/Desktop/文章4/数据集筛选/筛选重复基因/GSE138260/top_25_nodes_0.9.csv'
]

# 读取所有 CSV 文件并将它们添加到一个列表中
dataframes = [pd.read_csv(file) for file in file_names]

#dataframes = [pd.read_csv(file) for file in file_names]
# 使用 pd.concat 合并所有 DataFrame
#merged_dataframe = pd.concat(dataframes, ignore_index=True,axis=1)
merged_dataframe = pd.concat(dataframes,axis=1)
# 保存合并后的 DataFrame 到一个新的 CSV 文件

# df = pd.read_csv(file_names[0])
# # 获取原始CSV文件的第1列内容，包括列名
# first_column_name = df.columns[0]
# first_column_data = df[first_column_name]
# merged_dataframe.insert(0, first_column_name, first_column_data)
merged_dataframe.to_csv('C:/Users/lenovo/Desktop/文章4/数据集筛选/筛选重复基因/GSE138260/top25genes_python.csv', index=False)



