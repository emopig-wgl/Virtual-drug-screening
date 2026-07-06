import gudhi
import pandas as pd
import numpy as np
import math
from sklearn import preprocessing
from functools import reduce
dt = np.dtype([('dim', int), ('birth', float), ('death', float)])

#计算矩阵A的特征值并返回其实部
def call_eig(A):
    eigens = np.linalg.eigvalsh(A)
    return np.real(eigens)

#类初始化，两个参数 path 和 path_deg，分别是网络数据文件和包含节点信息的文件路径。
class network_complex:
    def __init__(self,path,path_deg) -> None:
        '''
        path: string network 的文件路径
        '''
        # path = './data/opioid/string_deg4_0.4.tsv'
        # path = './data/string_interactions_short_11.5_0.9.tsv'
        self.path = path

        #功能: 读取文件中的网络数据和基因名称。 self.nodes保存所有节点名称列表。
        df = pd.read_csv(self.path,sep='\t')
        count = 0

        degs = pd.read_csv(path_deg)
        self.nodes = list(degs['geneName']) #从degs数据框中提取geneName列，将其转换成列表，并保存到实例变量self.nodes

        self.node_id = {}
        for i in range(len(self.nodes)): #self.node_id，将每个基因名称映射到一个唯一的整数ID
            self.node_id[self.nodes[i]] = i
        
        self.edges = {}
        for i in range(len(df)): #，读取df数据框中的每一行，提取节点1（#node1）、节点2（node2）和它们之间的组合分数（combined_score）。然后将每个边（由节点1和节点2组成的字符串，格式为'{node1}_{node2}'）及其对应的分数保存到实例变量self.edges字典中。
            node1 = df['#node1'].iloc[i]
            node2 = df['node2'].iloc[i]
            score = float(df['combined_score'].iloc[i])
            self.edges[f'{node1}_{node2}'] = score
        pass

    #这个函数计算了不同尺度（由 intervals 定义）下的网络结构的持久性同调，并存储了这些特征
    def rips(self,start = 0,end = 0.3, stride = 0.03):
        matrixA = np.ones((len(self.nodes),len(self.nodes))) * 1000 #创建一数组,其大小为网络中节点数乘以节点数.1000进行初始化
        
        intervals = np.arange(start,end+stride,stride) #创建一个数组，包含从 start 到 end（包含）的等间距值，步长为 stride。这些值将用于定义Rips复形的参数。

        features = np.zeros((len(intervals)-1,3)) #存储持久性同调的特征

        def get_inter_id(num):
            for i in range(len(intervals)-1) :
                if intervals[i] <= num < intervals[i+1]:
                    return i
            return len(intervals) -1 -1
        
        for i in range(len(self.nodes)):
            for j in range(i,len(self.nodes)):
                node1 = self.nodes[i]
                node2 = self.nodes[j]

                score = -1000  #通过嵌套循环遍历所有节点对 (i, j)，并尝试从 self.edges 字典中获取它们之间的边权重（score）
                try:
                    score = self.edges[f'{node1}_{node2}']
                except:
                    pass
                try:
                    score = self.edges[f'{node2}_{node1}']
                except:
                    pass
                if score != -1000:
                    matrixA[i,j] = 1-score
                    matrixA[j,i] = 1-score
        
        rips_complex = gudhi.RipsComplex(distance_matrix=matrixA, max_edge_length=1) #用 gudhi.RipsComplex 创建一个Rips复形对象，传入 matrixA 作为距离矩阵，并将最大边长设置为1。
        Ph = rips_complex.create_simplex_tree(max_dimension = 2).persistence() #rips_complex.create_simplex_tree 方法创建一个单纯复形树，并设置最大维度为2（这意味着它将计算0维、1维和2维的持久性同调）。然后，调用 .persistence() 方法计算持久性同调。
        temp_bar = np.zeros(len(Ph),dtype=dt) #创建一个数组存储持久性条形码（persistence barcode），应该是数字类型

        ct = 0
        for simplex in Ph:
            dim, b, d = int(simplex[0]), float(simplex[1][0]), float(simplex[1][1])
            if d-b > 0.00002 and d != math.inf: #如果如果单纯形的死亡时间减去出生时间大于一个很小的阈值（0.00002），并且死亡时间不是无穷大（math.inf），则认为这个单纯形具有显著的持久性。
                temp_bar[ct]['dim'] = dim #满足上述条件，则将其维度、出生和死亡时间存储到 temp_bar 数组中
                temp_bar[ct]['birth'] = b
                temp_bar[ct]['death'] = d
                ct+=1
        bars = temp_bar[:ct] #bars 变量被设置为 temp_bar 数组的前 ct 个元素，即所有具有显著持久性的单纯形。

        for bar in bars: #更新特征矩阵
            if bar['dim'] == 0:
                features[get_inter_id(bar['death']),0] += 1
            if bar['dim'] == 1:
                features[get_inter_id(bar['birth']),1] += 1
                features[get_inter_id(bar['death']),2] += 1
        
        return features.flatten()  #features 矩阵被展平（转换为一维数组），并作为函数的返回值
    #用于计算一个图在不同半径下的最小非零特征值
    def lap(self,start = 0,end = 0.3, stride = 0.03,remove_id=None):
        matrixA = np.zeros((len(self.nodes),len(self.nodes)))
        intervals = np.arange(start,end+stride,stride)
        num_inter = (end-start)/stride

        eigen_values = []
        for radius in intervals: #
            for i in range(len(self.nodes)-1):
                for j in range(i+1,len(self.nodes)):
                    if i != remove_id and j != remove_id:
                        node1 = self.nodes[i]
                        node2 = self.nodes[j]

                        score = -1000
                        try:
                            score = self.edges[f'{node1}_{node2}']
                        except:
                            pass
                        try:
                            score = self.edges[f'{node2}_{node1}']
                        except:
                            pass

                        if score != -1000 and (1-score)<=radius:
                            matrixA[i,j] = -1
                            matrixA[j,i] = -1
            
            for i in range(len(self.nodes)):
                matrixA[i,i] = - np.sum(matrixA, axis = 1)[i]

            eigens = call_eig(matrixA) #计算拉普拉斯矩阵的特征值
            nonzero_eigens = eigens[eigens>1e-6] #筛选出大于 1e-6 的非零特征值

            if nonzero_eigens.shape[0] > 0:
                mini = nonzero_eigens.min()
            else:
                mini = 0.0

            eigen_values.append(mini) #找到这些非零特征值中的最小值，并将其添加到 eigen_values
        return np.array(eigen_values) #返回一个包含所有计算出的最小非零特征值的 NumPy
        # ##计算拉普拉斯矩阵的5个统计量（和、均值、最大、最小值、标准差）
    def lap_statistics(self,start = 0,end = 0.3, stride = 0.03,remove_id=None):
        matrixA = np.zeros((len(self.nodes),len(self.nodes)))
        intervals = np.arange(start,end+stride,stride)
        num_inter = (end-start)/stride

        eigen_values = []
        for radius in intervals:
            for i in range(len(self.nodes)-1):
                for j in range(i+1,len(self.nodes)):
                    if i != remove_id and j != remove_id:
                        node1 = self.nodes[i]
                        node2 = self.nodes[j]

                        score = -1000
                        try:
                            score = self.edges[f'{node1}_{node2}']
                        except:
                            pass
                        try:
                            score = self.edges[f'{node2}_{node1}']
                        except:
                            pass

                        if score != -1000 and (1-score)<=radius:
                            matrixA[i,j] = -1
                            matrixA[j,i] = -1
            
            for i in range(len(self.nodes)):
                matrixA[i,i] = - np.sum(matrixA, axis = 1)[i]

            eigens = call_eig(matrixA)
            nonzero_eigens = eigens[eigens>1e-6]

            if nonzero_eigens.shape[0] > 0:
                features_ele1 = [
                    np.sum(nonzero_eigens),
                    np.mean(nonzero_eigens),
                    np.max(nonzero_eigens),
                    np.std(nonzero_eigens),
                    np.min(nonzero_eigens),
                    ]
            else:
                features_ele1 = [
                    0.0, 0.0, 0.0, 0.0, 0.0
                ]


            # if nonzero_eigens.shape[0] > 0:
            #     mini = nonzero_eigens.min()
            # else:
            #     mini = 0.0

            eigen_values.append(features_ele1)##储存拉普拉斯矩阵的5个统计量（和、均值、最大、最小值、标准差）

        return np.array(eigen_values).flatten()

    #它用于在移除特定节点后，计算图在不同半径下的拓扑特征
    def remove_node(self,remove_id,start = 0,end = 0.3, stride = 0.03):
        matrixA = np.ones((len(self.nodes),len(self.nodes))) * 1000
        
        intervals = np.arange(start,end+stride,stride)

        features = np.zeros((len(intervals)-1,3))


        def get_inter_id(num):
            for i in range(len(intervals)-1) :
                if intervals[i] <= num < intervals[i+1]:
                    return i
            return len(intervals) -1 -1
        
        for i in range(len(self.nodes)):
            for j in range(i,len(self.nodes)):
                if i != remove_id and j != remove_id:
                    node1 = self.nodes[i]
                    node2 = self.nodes[j]

                    score = -1000
                    try:
                        score = self.edges[f'{node1}_{node2}']
                    except:
                        pass
                    try:
                        score = self.edges[f'{node2}_{node1}']
                    except:
                        pass
                    if score != -1000:
                        matrixA[i,j] = 1-score
                        matrixA[j,i] = 1-score
                else:
                    if self.nodes[remove_id] == 'EGR1':
                        x = 1
                        pass
        rips_complex = gudhi.RipsComplex(distance_matrix=matrixA, max_edge_length=1)
        Ph = rips_complex.create_simplex_tree(max_dimension = 2).persistence()
        temp_bar = np.zeros(len(Ph),dtype=dt)

        ct = 0
        for simplex in Ph:
            dim, b, d = int(simplex[0]), float(simplex[1][0]), float(simplex[1][1])
            if d-b > 0.00002 and d != math.inf:
                temp_bar[ct]['dim'] = dim
                temp_bar[ct]['birth'] = b
                temp_bar[ct]['death'] = d
                ct+=1
        bars = temp_bar[:ct]

        for bar in bars:
            if bar['dim'] == 0:
                features[get_inter_id(bar['death']),0] += 1
            if bar['dim'] == 1:
                features[get_inter_id(bar['birth']),1] += 1
                features[get_inter_id(bar['death']),2] += 1

        return features.flatten()

    #用于计算一个图在给定维度下的持久性贝蒂数
    def static(self,dim=1):
        matrixA = np.ones((len(self.nodes),len(self.nodes))) * 1000
        for i in range(len(self.nodes)):
            for j in range(i,len(self.nodes)):
                node1 = self.nodes[i]
                node2 = self.nodes[j]

                score = -1000
                try:
                    score = self.edges[f'{node1}_{node2}']
                except:
                    pass
                try:
                    score = self.edges[f'{node2}_{node1}']
                except:
                    pass
                if score != -1000:
                    matrixA[i,j] = 1-score
                    matrixA[j,i] = 1-score
        
        rips_complex = gudhi.RipsComplex(distance_matrix=matrixA, max_edge_length=2)
        complex_ = rips_complex.create_simplex_tree(max_dimension = dim)
        
        complex_.compute_persistence() 
        re = complex_.persistent_betti_numbers(2,100) #来获取维度为 2 的持久性贝蒂数
        return np.array(re)

    #在移除一个特定的节点后，计算剩余图的持久性贝蒂数（persistent Betti numbers）
    def static_remove_node(self,remove_id,dim = 1):
        matrixA = np.ones((len(self.nodes),len(self.nodes))) * 1000
        for i in range(len(self.nodes)):
            for j in range(i,len(self.nodes)):
                if i != remove_id and j != remove_id:
                    node1 = self.nodes[i]
                    node2 = self.nodes[j]

                    score = -1000
                    try:
                        score = self.edges[f'{node1}_{node2}']
                    except:
                        pass
                    try:
                        score = self.edges[f'{node2}_{node1}']
                    except:
                        pass
                    if score != -1000:
                        matrixA[i,j] = 1-score
                        matrixA[j,i] = 1-score
        
        rips_complex = gudhi.RipsComplex(distance_matrix=matrixA, max_edge_length=2)
        complex_ = rips_complex.create_simplex_tree(max_dimension = dim)
        
        complex_.compute_persistence() 
        re = complex_.persistent_betti_numbers(2,100)
        return np.array(re)

    # get_result 的方法，它用于计算移除图中每个节点后，图的结构变化程度，并返回一个包含这些变化得分的字典
    def get_result(self,start = 0,end = 0.3, stride = 0.03):
        
        original = self.rips(start = start,end = end, stride = stride)
        result_dic = {}
        for i,node in enumerate(self.nodes):
            # score = self.remove_node(i)
            score = np.linalg.norm(self.remove_node(i,start = start,end = end, stride = stride)-original) #使用 np.linalg.norm 函数计算移除节点后得到的持久性贝蒂数与原始持久性贝蒂数之间的欧几里得距离（即两个向量之间的差异程度），这个距离作为节点移除的得分。
            result_dic[node] = score
            if node == 'EGR1': #如果当前节点是 ‘EGR1’，则执行 x = 1（这行代码没有实际作用，可能是一个占位符或调试代码），然后使用 pass 语句跳过。
#返回结果字典：最后，返回包含所有节点移除得分的 result_dic 字典。
                x = 1
                pass
        return result_dic

    def get_result_static(self,dim=1):
        
        original = self.static(dim=dim)
        result_dic = {}
        for i,node in enumerate(self.nodes):
            # score = self.remove_node(i)
            score = np.linalg.norm(self.static_remove_node(i,dim=dim)-original) #np.linalg.norm 函数计算移除节点后得到的持久性贝蒂数与原始持久性贝蒂数之间的欧几里得距离（即两个向量之间的差异程度），这个距离作为节点移除的得分
            result_dic[node] = score
            if node == 'EGR1':
                x = 1
                pass
        return result_dic
        
    def get_result_lap(self,start = 0,end = 0.3, stride = 0.03):
        
        original1 = self.rips(start = start,end = end, stride = stride)
        original2 = self.lap(start = start,end = end, stride = stride,remove_id=None)

        original = np.concatenate((original1,original2),axis=0)

        result_dic = {}
        ls = []
        ls1 = []
        ls2 = []
        for i,node in enumerate(self.nodes):
            # score = self.remove_node(i)

            fea1 = self.remove_node(i,start = start,end = end, stride = stride)
            fea2 = self.lap(start = start,end = end, stride = stride,remove_id=i)

            score1 = np.linalg.norm(fea1-original1)
            score2 = np.linalg.norm(fea2-original2)
            score = np.linalg.norm(np.concatenate((fea1,fea2),axis=0)-original)
            result_dic[node] = score
            ls1.append(score1)
            ls2.append(score2)
            ls.append(score)
            if node == 'EGR1':
                x = 1
                pass
        return result_dic,ls1,ls2,ls,list(preprocessing.minmax_scale(np.array(ls1))+preprocessing.minmax_scale(np.array(ls2)))

    def get_result_lap_statistics(self,start = 0,end = 0.3, stride = 0.03):

        original1 = self.rips(start = start,end = end, stride = stride)
        original2 = self.lap_statistics(start = start,end = end, stride = stride,remove_id=None)

        original = np.concatenate((original1,original2),axis=0)

        result_dic = {}
        ls = []
        ls1 = []
        ls2 = []
        for i,node in enumerate(self.nodes):
            # score = self.remove_node(i)

            fea1 = self.remove_node(i,start = start,end = end, stride = stride)
            fea2 = self.lap_statistics(start = start,end = end, stride = stride,remove_id=i)

            score1 = np.linalg.norm(fea1-original1) #PH特征
            score2 = np.linalg.norm(fea2-original2) #拉普拉斯矩阵特征
            score = np.linalg.norm(np.concatenate((fea1,fea2),axis=0)-original) #分别归一化并相加
            result_dic[node] = score
            ls1.append(score1)
            ls2.append(score2)
            ls.append(score)
        return result_dic,ls1,ls2,ls,list(preprocessing.minmax_scale(np.array(ls1))+preprocessing.minmax_scale(np.array(ls2)))


    def get_result_lap_only_lamda(self,start = 0,end = 0.3, stride = 0.03):
        
        # original1 = self.rips(start = start,end = end, stride = stride)
        original2 = self.lap(start = start,end = end, stride = stride,remove_id=None)

        # original = np.concatenate((original1,original2),axis=0)

        result_dic = {}
        for i,node in enumerate(self.nodes):
            # score = self.remove_node(i)

            # fea1 = self.remove_node(i,start = start,end = end, stride = stride)
            fea2 = self.lap(start = start,end = end, stride = stride,remove_id=i)
            score = np.linalg.norm(fea2-original2)
            result_dic[node] = score
            if node == 'EGR1':
                x = 1
                pass
        return result_dic

        
# a = network_complex('')
# b = a.static()
# b = a.get_result_static()
# c = dict(sorted(b.items(), key=lambda item: item[1],reverse=True))
# d = c

df_new = {}
dfs = []
#patp = 'C:/Users/Administrator/Desktop/cocaine{_复现结果'
patp = 'C:/Users/lenovo/Desktop/文章4/数据集筛选/筛选重复基因/GSE36980/'
compl = network_complex(patp + f'/GSE36980_string_interactions_short_0.9.tsv', patp + '/GSE36980_DEGs_limma_split.csv')
df = pd.DataFrame()
df['node'] = compl.nodes
lap = compl.get_result_lap_statistics(start=0,end=1-0.9,stride=(1-0.9)/10)
    # df[f're_ph_{cutoff}'] = list(re_ph.values())
    # df[f're_dim1_{cutoff}'] = list(compl.get_result_static(dim=1).values())
    # df[f're_dim2_{cutoff}'] = list(compl.get_result_static(dim=2).values())
    # df[f're_dim3_{cutoff}'] = list(compl.get_result_static(dim=3).values())
    # df[f'lap_lamda_{cutoff}'] = list(compl.get_result_lap_only_lamda(start=0,end=1-cutoff,stride=(1-cutoff)/10).values())
df[f'lap_barcode_0.9'] = lap[1]
df[f'lap_lamda_0.9'] = lap[2]
df[f'lap_sum_0.9'] = lap[3]
df[f'lap_sum_norm_0.9'] = lap[4]
dfs.append(df)
merged_df = reduce(lambda left, right: pd.merge(left, right, on='node'), dfs)
merged_df.to_csv('C:/Users/lenovo/Desktop/文章4/数据集筛选/筛选重复基因/GSE36980/ph_cocaine_norm_statistics_0.9.csv')


