import pandas as pd

##运行4次，每次更改文件
file_names = ['C:/Users/lenovo/Desktop/文章4/数据集筛选/筛选重复基因/GSE36980/ph_cocaine_norm_statistics_0.15.csv']

# 读取CSV文件
df = pd.read_csv(file_names[0])

# 对lap_sum_norm_0.15列进行降序排序，并选取前25行
top_25_nodes = df.sort_values(by='lap_sum_norm_0.15', ascending=False).head(25)

# 选择node列，并重命名为node_0.15
top_25_nodes = top_25_nodes[['node']].rename(columns={'node': 'node_0.15'})

# 保存结果到新的CSV文件
top_25_nodes.to_csv('C:/Users/lenovo/Desktop/文章4/数据集筛选/筛选重复基因/GSE36980/top_25_nodes_0.15.csv', index=False)
