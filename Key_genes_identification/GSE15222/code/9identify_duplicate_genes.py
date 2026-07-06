import pandas as pd

# 读取CSV文件
input_file = "C:/Users/lenovo/Desktop/文章4/数据集筛选/筛选重复基因/GSE15222/top25genes_python.csv"  # 替换为你的CSV文件路径
output_file = "C:/Users/lenovo/Desktop/文章4/数据集筛选/筛选重复基因/GSE15222/duplicate_gene_top25version.csv"  # 输出文件名

data = pd.read_csv(input_file)

# 确保列名为指定的列名，避免错误
required_columns = ["node_0.15", "node_0.4", "node_0.7", "node_0.9"]
if not all(column in data.columns for column in required_columns):
    raise ValueError("输入文件缺少指定的列")

# 找到4列中均出现的基因
common_genes = set(data[required_columns[0]])
for column in required_columns[1:]:
    common_genes &= set(data[column])

# 将结果转换为DataFrame并保存为CSV文件
common_genes_df = pd.DataFrame(list(common_genes), columns=["Gene"])
common_genes_df.to_csv(output_file, index=False)

print(f"筛选完成，结果已保存到 {output_file}")