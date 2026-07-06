# from sklearn.svm import SVR 
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
import numpy as np
import csv
import sys, time, os

t_start = time.time()

# 对输入数据进行标准化
def normalize(X):
    scaler = StandardScaler().fit(X)
    return scaler.transform(X)

# 将 CSV 文件转换为 NumPy 数组
def csv_to_npy(filename):
    import pandas as pd
    df = pd.read_csv(filename)

    # ✅ 只取 cddd 特征列
    feature_cols = [col for col in df.columns if col.startswith('cddd_')]

    X = df[feature_cols].values

    # 防止变成一维（极端情况）
    if X.ndim == 1:
        X = X.reshape(-1, 1)

    return X

# 接收参数：训练集 CHEMBL 数据集 & 测试集 CHEMBL 数据集
model = sys.argv[1]  # 训练集，如 CHEMBL216
name = sys.argv[2]   # 测试集，CHEMBL1

# 设置各路径
base_dir = '/share/home/u2415173011/Aldisease/TOP25_CHEMBL'
path_smi = f'{base_dir}/{model}/'
path_label = f'{base_dir}/{model}/'
path_BET_npy = f'{base_dir}/BET/'
path_AE_csv = f'{base_dir}/AE/'
path_ECFP_npy = f'{base_dir}/ECFP/'

# 读取 SMILES 文件
with open(path_smi + f'{model}.smi', 'r') as f:
    data = np.array([line.strip() for line in f.readlines()])

print('size of data:', np.shape(data), flush=True)

# 读取标签
y_val_list = []
with open(path_label + f'label_{model}.csv', 'r') as f:
    for line in f:
        y_val_list.append(eval(line.strip()))
y_val = np.array(y_val_list)

train_size = int(data.shape[0] * 0.8)
print('size of train size:', train_size, flush=True)

# 设置 SVM 参数
C = 10 if train_size < 1000 else 5 if train_size < 5000 else 1

# 读取特征
# X_train_BET = np.load(path_BET_npy + f'{model}/{model}_BET.npy', allow_pickle=True)
# X_train_AE = csv_to_npy(path_AE_csv + f'{model}_AE.csv')
# X_train_ECFP = np.load(path_ECFP_npy + f'{model}/{model}_ECFP.npy', allow_pickle=True)
# X_train = np.hstack((X_train_BET, X_train_AE, X_train_ECFP))
X_train_AE = csv_to_npy(path_AE_csv + f'{model}_AE.csv')
X_train_ECFP = np.load(path_ECFP_npy + f'{model}/{model}_ECFP.npy', allow_pickle=True)

X_train = np.hstack((X_train_AE, X_train_ECFP))
X_train = normalize(X_train)

y_train = np.array([float(i.strip()) for i in open(path_label + f'label_{model}.csv').readlines()])

# X_test_BET = np.load(path_BET_npy + f'{name}/{name}_BET.npy', allow_pickle=True)
# X_test_AE = csv_to_npy(path_AE_csv + f'{name}/{name}_AE.csv')
# X_test_ECFP = np.load(path_ECFP_npy + f'{name}/{name}_ECFP.npy', allow_pickle=True)
X_test_AE = csv_to_npy(path_AE_csv + f'{name}/{name}_AE.csv')
X_test_ECFP = np.load(path_ECFP_npy + f'{name}/{name}_ECFP.npy', allow_pickle=True)

# ✅ 加载有效索引
valid_idx = np.load(f'{path_AE_csv}/{name}/{name}_valid_idx.npy')

# ✅ 对齐所有特征
# ✅ 加载 valid_idx
valid_idx = np.load(f'{path_AE_csv}/{name}/{name}_valid_idx.npy')

# ✅ 对齐
# X_test_BET = X_test_BET[valid_idx]
# X_test_ECFP = X_test_ECFP[valid_idx]
X_test_ECFP = X_test_ECFP[valid_idx]

# X_test = np.hstack((X_test_BET, X_test_AE, X_test_ECFP))
# X_test = normalize(X_test)

# # SVM 模型训练与预测
# SVR_model = SVR(kernel='rbf', C=C, gamma='scale')
# SVR_model.fit(X_train, y_train)
# y_pred = SVR_model.predict(X_test)
X_test = np.hstack((X_test_AE, X_test_ECFP))
X_test = normalize(X_test)

GBDT_model = GradientBoostingRegressor(
    n_estimators=300,
    learning_rate=0.05,
    max_depth=4,
    random_state=42
)

GBDT_model.fit(X_train, y_train)

y_pred = GBDT_model.predict(X_test)

# 保存预测结果
path_all_BA = f'{base_dir}/prediction_result/'
os.makedirs(path_all_BA, exist_ok=True)
np.savetxt(path_all_BA + f'{model}_{name}_all_BA.txt', y_pred)


import pandas as pd

# ✅ 读取原始测试集 CSV
df = pd.read_csv(f'{base_dir}/AE/{name}/{name}.csv')

# ✅ 加载 valid_idx
valid_idx = np.load(f'{path_AE_csv}/{name}/{name}_valid_idx.npy')

# ✅ 创建完整 BA（用 NaN 填充）
BA_full = np.full(len(df), np.nan)

# ✅ 回填预测值
BA_full[valid_idx] = y_pred

# ✅ 加入 DataFrame
df['BA_pred'] = BA_full

# ✅ 保存完整结果（推荐）
df.to_csv(path_all_BA + f'{model}_{name}_with_BA.csv', index=False)

t_end = time.time()
print('total time:', (t_end - t_start)/3600, 'h', flush=True)