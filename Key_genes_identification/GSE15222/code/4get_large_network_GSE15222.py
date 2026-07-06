#import LCC
import lcc
import networkx as nx
import pandas as pd

# df2 = pd.read_csv('./data/string_interactions_11.5_short_0.9.tsv',sep='\t')
#df2 = pd.read_csv('./data/deg_ppi_0.9.tsv',sep='\t')
df2 = pd.read_csv('C:/Users/lenovo/Desktop/文章4/数据集筛选/筛选重复基因/GSE15222/GSE15222_string_interactions_short_0.4.tsv',sep='\t')  #opoid
#df2 = pd.read_csv('C:/Users/Administrator/Desktop/cocaine{_复现结果/string_interactions_short_0.9.tsv',sep='\t')
labels = []
# s = pd.read_csv('./data/Data_Sheet_1_Identification_of_key_genes_and_therapeutic_drugs_for_cocaine_addiction_using_integrated_bioinformatics_analysis.CSV')
# s = pd.read_excel(io='./data/DEGs.xlsx',sheet_name='Sheet2')
s = pd.read_csv('C:/Users/lenovo/Desktop/文章4/数据集筛选/筛选重复基因/GSE15222/GSE15222_DEGs_limma.csv')
#s = pd.read_csv('C:/Users/Administrator/Desktop/cocaine{_复现结果/DEGs.csv')
#s = pd.read_csv('./data/DEGs.csv')
s = list(s['geneName'])  #将列geneName转换为列表

for i in range(len(df2)):
    if df2.iloc[i]['#node1'] in s and df2.iloc[i].node2 in s:
        labels.append(1)
    else:
        labels.append(0)
df2.insert(loc=0,column='label',value=labels) #df2的最前面插入一个新列label，其值为之前创建的labels列表。
df = df2[df2['label'] == 1] #创建一个新的df，它只包含df2中label列值为1的行。
df.to_csv('C:/Users/lenovo/Desktop/文章4/数据集筛选/筛选重复基因/GSE15222/deg_ppi_0.4_clean.tsv',sep='\t')
#$df.to_csv('C:/Users/Administrator/Desktop/cocaine{_复现结果/deg_ppi_0.9_clean.tsv',sep='\t')
G = nx.from_pandas_edgelist(df, '#node1', 'node2', 'combined_score') #从df DataFrame创建一个图G，#node1和node2列作为边，combined_score作为边的权重。
G = G.to_undirected() #图G转换为无向图
largest_component = max(nx.connected_components(G), key=len) #找到图中最大的连通组件
LCC = G.subgraph(largest_component)  #创建一个子图LCC，它只包含最大连通组件中的节点和边
G=LCC #。然后将这个子图赋值给G
# degree_centrality = nx.degree_centrality(G)
# print(a)
node1 = []
node2 = []
node3 = []
for edge in list(G.edges): #遍历图G中的所有边，将每个边的起点和终点分别添加到node1和node2列表中
    node1.append(edge[0])
    node2.append(edge[1])

df = pd.DataFrame({
    'node1':node1,
    'node2':node2
})



df.to_csv('C:/Users/lenovo/Desktop/文章4/数据集筛选/筛选重复基因/GSE15222/deg_ppi_large.csv')
#df.to_csv('C:/Users/Administrator/Desktop/cocaine{_复现结果/deg_ppi_large.csv')

for node in list(G): #遍历一图（G）中的所有节点
    node3.append(node)

df = pd.DataFrame({ #
    'Gene':node3
})
df.to_csv('C:/Users/lenovo/Desktop/文章4/数据集筛选/筛选重复基因/GSE15222/deg_ppi_nodes_large.csv')
#df.to_csv('C:/Users/Administrator/Desktop/cocaine{_复现结果/deg_ppi_nodes_large.csv')
print('over')