# import numpy as np
# from sklearn.ensemble import GradientBoostingRegressor
# from sklearn.linear_model import LinearRegression
# from sklearn.metrics import mean_squared_error
# from sklearn.model_selection import KFold
# from sklearn.preprocessing import StandardScaler
# import scipy, argparse, sys, os
# from random import randrange, seed
# from sklearn.metrics import matthews_corrcoef
# from sklearn.metrics import roc_auc_score
# from sklearn.metrics import r2_score
# import time
# os.environ['MKL_THREADING_LAYER'] = 'GNU'
# os.environ['MKL_SERVICE_FORCE_INTEL'] = '1'

# t_start = time.time()

# def normalize(X):
#     scaler = StandardScaler().fit(X)
#     return scaler.transform(X)

# # 输入文件的类别名称
# model = sys.argv[1] # 数据集名称，如CHEMBL205
# path_smi = '/public/home/chenlong666/Chunhuanzhang/top300_chembl/{}/'.format(model)
# path_label = '/public/home/chenlong666/Chunhuanzhang/top300_chembl/{}/'.format(model)
# file = open(path_smi + '{}.smi'.format(model,model),'r')
# data = [line for line in file.readlines()]
# data = np.array(data)
# print('size of data:', np.shape(data), flush=True)
# # y_val = np.load(path_label + 'label_%s_%s_reg.npy' % (target_ID, cator), allow_pickle=True)

# # 获取标签文件的矩阵形式
# y_val_ori = open(path_label + 'label_{}.csv'.format(model,model),'r')
# y_val_list = []
# for i in y_val_ori.readlines():
#     i = eval(i.strip())
#     y_val_list.append(i)
# y_val = np.array(y_val_list)
# print('size of y_val:', np.shape(y_val), flush=True)

# train_size = int(float(np.shape(data)[0]) * 0.8) # 训练集大小
# print('size of train size:', train_size,flush=True)
# # 设置机器学习参数
# if train_size < 1000:
#     max_depth, min_samples_split, min_samples_leaf = 7, 3, 1
#     subsample = 0.7
#     C = 10
# elif train_size >= 1000 and train_size < 5000:
#     max_depth, min_samples_split, min_samples_leaf = 8, 4, 2
#     subsample = 0.5
#     C = 5
# elif train_size >= 5000:
#     max_depth, min_samples_split, min_samples_leaf = 9, 7, 3
#     subsample = 0.3
#     C = 1

# # path_feature = '/mnt/home/jiangj33/opium/feature_matrix_opium/'
# parser = argparse.ArgumentParser(description='GBDT inputs')
# parser.add_argument('--n_estimators', default=10000, type=int,
#                     help='Maximum tree depth')
# parser.add_argument('--dataset', default=model, type=str,
#                     help='Dataset selected')
# parser.add_argument('--max_depth', default=max_depth, type=int,
#                     help='Maximum tree depth')
# parser.add_argument('--learning_rate', default=0.01, type=float,
#                     help='Learning rate for gbrt')
# parser.add_argument('--criterion', default='friedman_mse', type=str,
#                     help='Loss function for gbrt')
# parser.add_argument('--subsample', default=subsample, type=float,
#                     help='Subsample for fitting individual learners')
# parser.add_argument('--max_features', default='sqrt', type=str,
#                     help='Number of features to be considered')
# parser.add_argument('--min_samples_split', default=min_samples_split, type=int,
#                     help='Minimum sample num of each leaf node.')
# parser.add_argument('--loss', default='ls', type=str,
#                     help='Loss function to be optimized.')
# parser.add_argument('--n_iter_no_change', default=None, type=int,
#                     help='Early stopping will be used to terminate training')
# parser.add_argument('--random_seed', default=0, type=int,
#                     help='random seed')
# # args = parser.parse_args() # 报错
# args = parser.parse_known_args()[0]
# print('GBDT parameter', flush=True)
# print(args, flush=True)

# for ii in range(1):
#     results = np.zeros(y_val.shape)

#     kf = KFold(n_splits=10, shuffle=True, random_state=ii)
#     fold = 0
#     for train_idx, test_idx in kf.split(data):
#         fold += 1
#         print('fold=', fold, flush=True)
       
#         # 生成ECFP特征
#         cmd = 'python "/public/home/chenlong666/desktop/PretrainModels/bt_pro/generate_bt_fps.py" \
#             --model_name_or_path "/public/home/chenlong666/desktop/PretrainModels/examples/models/" \
#             --checkpoint_file "/public/home/chenlong666/desktop/PretrainModels/checkpoint_best.pt" \
#             --data_name_or_path  "/public/home/chenlong666/desktop/PretrainModels/examples/models/" \
#             --dict_file "/public/home/chenlong666/desktop/PretrainModels/examples/models/dict.txt" \
#             --target_file "/public/home/chenlong666/Chunhuanzhang/chansheng10ci/AE/{}/{}_regression_train_{}.smi" \
#             --save_feature_path "/public/home/chenlong666/Chunhuanzhang/chansheng10ci/ECFP/{}_train_ECFP_{}.npy"'.format(model, model, fold, model, fold)
#         os.system(cmd)

#         cmd = 'python "/public/home/chenlong666/desktop/PretrainModels/bt_pro/generate_bt_fps.py" \
#                     --model_name_or_path "/public/home/chenlong666/desktop/PretrainModels/examples/models/" \
#                     --checkpoint_file "/public/home/chenlong666/desktop/PretrainModels/checkpoint_best.pt" \
#                     --data_name_or_path  "/public/home/chenlong666/desktop/PretrainModels/examples/models/" \
#                     --dict_file "/public/home/chenlong666/desktop/PretrainModels/examples/models/dict.txt" \
#                     --target_file "/public/home/chenlong666/Chunhuanzhang/chansheng10ci/AE/{}/{}_regression_valid_{}.smi" \
#                     --save_feature_path "/public/home/chenlong666/Chunhuanzhang/chansheng10ci/ECFP/{}_valid_ECFP_{}.npy"'.format(model,
#              model, fold, model, fold)
#         os.system(cmd)

#         cmd = 'python "/public/home/chenlong666/desktop/PretrainModels/bt_pro/generate_bt_fps.py" \
#                     --model_name_or_path "/public/home/chenlong666/desktop/PretrainModels/examples/models/" \
#                     --checkpoint_file "/public/home/chenlong666/desktop/PretrainModels/checkpoint_best.pt" \
#                     --data_name_or_path  "/public/home/chenlong666/desktop/PretrainModels/examples/models/" \
#                     --dict_file "/public/home/chenlong666/desktop/PretrainModels/examples/models/dict.txt" \
#                     --target_file "/public/home/chenlong666/Chunhuanzhang/chansheng10ci/AE/{}/{}_regression_test_{}.smi" \
#                     --save_feature_path "/public/home/chenlong666/Chunhuanzhang/chansheng10ci/ECFP/{}_test_ECFP_{}.npy"'.format(model,
#              model, fold, model, fold)
#         os.system(cmd)

# t_end = time.time()
# print('total time:', (t_end - t_start) / 3600, 'h', flush=True)
import numpy as np
from sklearn.model_selection import KFold
import sys, os, time

from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit import DataStructs

os.environ['MKL_THREADING_LAYER'] = 'GNU'
os.environ['MKL_SERVICE_FORCE_INTEL'] = '1'

t_start = time.time()

# ===============================
# 输入参数
# ===============================
model = sys.argv[1]

# ===============================
# 路径（你的服务器）
# ===============================
base_path = f"/share/home/u2415173011/Aldisease/TOP25_CHEMBL/AE/{model}/"

path_smi = base_path
path_out = f"/share/home/u2415173011/Aldisease/TOP25_CHEMBL/ECFP/{model}/"

print("Using path:", base_path)

# ===============================
# ECFP函数（核心替换）
# ===============================
def smiles_to_ecfp(smiles, radius=2, nBits=2048):
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return np.zeros(nBits)
    fp = AllChem.GetMorganFingerprintAsBitVect(mol, radius, nBits=nBits)
    arr = np.zeros((nBits,), dtype=int)
    DataStructs.ConvertToNumpyArray(fp, arr)
    return arr

def generate_ecfp_file(input_smi, output_npy):
    features = []
    with open(input_smi, 'r') as f:
        for line in f:
            smi = line.strip()
            if smi == "":
                continue
            features.append(smiles_to_ecfp(smi))

    features = np.array(features)
    np.save(output_npy, features)
    print(f"Saved: {output_npy}, shape={features.shape}", flush=True)

# ===============================
# 10-fold（只控制fold编号）
# ===============================
kf = KFold(n_splits=10, shuffle=True, random_state=0)
dummy = np.arange(10)

fold = 0
for _, _ in kf.split(dummy):
    fold += 1
    print('fold =', fold, flush=True)

    # ===============================
    # 输入文件（不变）
    # ===============================
    train_smi = f"{path_smi}{model}_regression_train_{fold}.smi"
    valid_smi = f"{path_smi}{model}_regression_valid_{fold}.smi"
    test_smi  = f"{path_smi}{model}_regression_test_{fold}.smi"

    # ===============================
    # 输出文件（完全保持不变）
    # ===============================
    train_out = f"{path_out}{model}_train_ECFP_{fold}.npy"
    valid_out = f"{path_out}{model}_valid_ECFP_{fold}.npy"
    test_out  = f"{path_out}{model}_test_ECFP_{fold}.npy"

    print("Generating REAL ECFP...", flush=True)

    # ===== train =====
    generate_ecfp_file(train_smi, train_out)

    # ===== valid =====
    generate_ecfp_file(valid_smi, valid_out)

    # ===== test =====
    generate_ecfp_file(test_smi, test_out)

    print("Fold done!", flush=True)

t_end = time.time()
print('total time:', (t_end - t_start) / 3600, 'h', flush=True)