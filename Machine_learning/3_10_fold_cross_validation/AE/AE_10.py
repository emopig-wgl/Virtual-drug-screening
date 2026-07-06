# import numpy as np
# import pandas as pd
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
# path_smi = '/share/home/u2415173011/Aldisease/TOP25_CHEMBL/AE/{}/'.format(model)
# path_label = '/share/home/u2415173011/Aldisease/TOP25_CHEMBL/AE/{}/'.format(model)
# file = open(path_smi + f'{model}.smi','r')
# data = [line for line in file.readlines()]
# data = np.array(data)
# print('size of data:', np.shape(data), flush=True)
# # y_val = np.load(path_label + 'label_%s_%s_reg.npy' % (target_ID, cator), allow_pickle=True)

# # 获取标签文件的矩阵形式
# y_val_ori = open(path_label + f'label_{model}.csv','r')
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
#         X_trainset, X_testset = data[train_idx], data[test_idx]
#         y_train, y_test = y_val[train_idx], y_val[test_idx]
#         f_train_smi = open(path_smi + '%s_regression_train_%d.smi' % (model, fold), 'w')
#         f_valid_smi = open(path_smi + '%s_regression_valid_%d.smi' % (model, fold), 'w')
#         f_test_smi  = open(path_smi + '%s_regression_test_%d.smi'  % (model, fold), 'w')
#         f_train_label = open(path_smi + '%s_regression_train_%d.label' % (model, fold), 'w')
#         f_valid_label = open(path_smi + '%s_regression_valid_%d.label' % (model, fold), 'w')
#         f_test_label  = open(path_smi + '%s_regression_test_%d.label'  % (model, fold), 'w')

#         test_num = np.shape(X_testset)[0]
#         train_num = train_size
#         valid_num = np.shape(X_trainset)[0] - train_num
#         print('train_num:', train_num)
#         print('valid_num:',valid_num)
#         print('test_num:',test_num)

#         for i in range(train_num):
#             f_train_smi.write(X_trainset[i].strip() + '\n')
#         for j in range(train_num, train_num + valid_num):
#             f_valid_smi.write(X_trainset[j].strip() + '\n')
#         for i in range(test_num):
#             f_test_smi.write(X_testset[i].strip() + '\n')
#         for k in range(train_num):
#             f_train_label.write(str(y_train[k]) + '\n')
#         for k in range(train_num, train_num + valid_num):
#             f_valid_label.write(str(y_train[k]) + '\n')
#         for p in range(test_num):
#             f_test_label.write(str(y_test[p]) + '\n')
#         f_train_smi.close()
#         f_valid_smi.close()
#         f_test_smi.close()
#         f_train_label.close()
#         f_valid_label.close()
#         f_test_label.close()
#         print('step1 finished!')

#         # 生成BET特征
#         # cmd = 'python "/public/home/chenlong666/desktop/PretrainModels/bt_pro/generate_bt_fps.py" \
#         #     --model_name_or_path "/public/home/chenlong666/desktop/PretrainModels/examples/models/" \
#         #     --checkpoint_file "checkpoint_best.pt" \
#         #     --data_name_or_path  "/public/home/chenlong666/desktop/PretrainModels/examples/models/" \
#         #     --dict_file "/public/home/chenlong666/desktop/PretrainModels/examples/models/dict.txt" \
#         #     --target_file "/public/home/chenlong666/desktop/original_data/{}/{}_regression_train_{}.smi" \
#         #     --save_feature_path "/public/home/chenlong666/desktop/result/BET_npy/{}_train_BET_{}.npy"'.format(model, model, fold, model, fold)
#         # os.system(cmd)
#         #
#         # cmd = 'python "/public/home/chenlong666/desktop/PretrainModels/bt_pro/generate_bt_fps.py" \
#         #             --model_name_or_path "/public/home/chenlong666/desktop/PretrainModels/examples/models/" \
#         #             --checkpoint_file "checkpoint_best.pt" \
#         #             --data_name_or_path  "/public/home/chenlong666/desktop/PretrainModels/examples/models/" \
#         #             --dict_file "/public/home/chenlong666/desktop/PretrainModels/examples/models/dict.txt" \
#         #             --target_file "/public/home/chenlong666/desktop/original_data/{}/{}_regression_valid_{}.smi" \
#         #             --save_feature_path "/public/home/chenlong666/desktop/result/BET_npy/{}_valid_BET_{}.npy"'.format(
#         #     model, model, fold, model, fold)
#         # os.system(cmd)
#         #
#         # cmd = 'python "/public/home/chenlong666/desktop/PretrainModels/bt_pro/generate_bt_fps.py" \
#         #             --model_name_or_path "/public/home/chenlong666/desktop/PretrainModels/examples/models/" \
#         #             --checkpoint_file "checkpoint_best.pt" \
#         #             --data_name_or_path  "/public/home/chenlong666/desktop/PretrainModels/examples/models/" \
#         #             --dict_file "/public/home/chenlong666/desktop/PretrainModels/examples/models/dict.txt" \
#         #             --target_file "/public/home/chenlong666/desktop/original_data/{}/{}_regression_test_{}.smi" \
#         #             --save_feature_path "/public/home/chenlong666/desktop/result/BET_npy/{}_test_BET_{}.npy"'.format(
#         #     model, model, fold, model, fold)
#         # os.system(cmd)

#         # 生成AE特征
#         cmd = f'cddd --input {path_smi}{model}_regression_train_{fold}.smi \
# --out {path_smi}{model}_train_AE_{fold}.csv \
# --no-preprocess'

#         cmd = f'cddd --input {path_smi}{model}_regression_valid_{fold}.smi \
# --out {path_smi}{model}_valid_AE_{fold}.csv \
# --no-preprocess'

#         cmd = f'cddd --input {path_smi}{model}_regression_test_{fold}.smi \
# --out {path_smi}{model}_test_AE_{fold}.csv \
# --no-preprocess'

#         # step2,对输入数据进行预训练，将其二进制化
#         # 下列代码第一次运行则取消注释
#         # os.system('mkdir "./examples/data/regression_example/input0"')
#         # cmd = 'python "/public/home/chenlong666/desktop/PretrainModels/bt_pro/preprocess.py" --only-source \
#         #     --trainpref "/public/home/chenlong666/desktop/original_data/{}/{}_regression_train_{}.smi" \
#         #     --validpref "/public/home/chenlong666/desktop/original_data/{}/{}_regression_valid_{}.smi" \
#         #     --destdir "/public/home/chenlong666/desktop/PretrainModels/examples/data/regression_example/input0" --trainoutf "train" \
#         #     --validoutf "valid" --workers 20 --file-format smiles \
#         #     --srcdict "/public/home/chenlong666/desktop/PretrainModels/examples/models/dict.txt"'.format(model, model,fold,
#         #                                                                                                 model, model,fold)
#         # os.system(cmd)
#         #
#         # # # os.system('mkdir "./examples/data/regression_example/label"') # 生成标签文件，若已经生成目标文件则取消该命令
#         # cmd = 'cp "/public/home/chenlong666/desktop/original_data/{}/{}_regression_train_{}.label" \
#         #           "/public/home/chenlong666/desktop/PretrainModels/examples/data/regression_example/label/train.label"'.format(
#         #     model, model,fold)
#         # os.system(cmd)
#         # cmd = 'cp "/public/home/chenlong666/desktop/original_data/{}/{}_regression_valid_{}.label" \
#         #           "/public/home/chenlong666/desktop/PretrainModels/examples/data/regression_example/label/valid.label"'.format(
#         #     model, model,fold)
#         # os.system(cmd)
#         # print('step2 finished!')
#         #
#         # # Step3, 微调预训练模型
#         # # os.system('mkdir "./examples/models/finetuned_model_regression"')
#         # # CUDA_VISIBLE_DEVICES=0
#         # train_smiles = r'/public/home/chenlong666/desktop/original_data/{}/{}_regression_train_{}.smi'.format(model, model,fold)
#         # with open(train_smiles, 'r') as f:
#         #     smi_text = f.readlines()
#         # cmd = 'num_epoch=50 ; num_sent_pergpu=16 ; updata_freq=1 ; train_data_len=%d ;  \
#         #       num_warmup=`expr $num_epoch \* $train_data_len / ${num_sent_pergpu} / $updata_freq / 10 ` ; max_num_update=100000 ;\
#         #       CUDA_VISIBLE_DEVICES=0 python "/public/home/chenlong666/desktop/PretrainModels/bt_pro/train.py" \
#         #       "/public/home/chenlong666/desktop/PretrainModels/examples/data/regression_example/" \
#         #       --save-dir "/public/home/chenlong666/desktop/PretrainModels/examples/models/finetuned_model_regression" \
#         #       --train-subset train --valid-subset valid --restore-file \
#         #       "/public/home/chenlong666/desktop/PretrainModels/examples/models/checkpoint_best.pt" \
#         #       --task sentence_prediction --num-classes 1 --regression-target \
#         #       --init-token 0 --best-checkpoint-metric loss --arch roberta_base \
#         #       --bpe smi --encoder-attention-heads 8 --encoder-embed-dim 512 \
#         #       --encoder-ffn-embed-dim 1024 --encoder-layers 8 --dropout 0.1 \
#         #       --attention-dropout 0.1 --criterion sentence_prediction \
#         #       --max-positions 256 --truncate-sequence --skip-invalid-size-inputs-valid-test \
#         #       --optimizer adam --adam-betas "(0.9,0.999)" --adam-eps 1e-6 --clip-norm 0.0 \
#         #       --lr-scheduler polynomial_decay --lr 0.0001 --warmup-updates ${num_warmup} \
#         #       --total-num-update  ${max_num_update} --max-update ${max_num_update} \
#         #       --max-epoch ${num_epoch} --weight-decay 0.1 --log-format simple --reset-optimizer \
#         #       --reset-dataloader --reset-meters --no-epoch-checkpoints \
#         #       --no-last-checkpoints --no-save-optimizer-state --find-unused-parameters \
#         #       --log-interval 5 --max-sentences ${num_sent_pergpu} --update-freq ${updata_freq} \
#         #       --required-batch-size-multiple 1 --ddp-backend no_c10d'%(len(smi_text))
#         #
#         # os.system(cmd)
#         # print('step3 finished!')
#         #
#         # # Step4, 从微调模型中生成微调特征
#         # os.system('cp "/public/home/chenlong666/desktop/PretrainModels/examples/models/dict.txt" \
#         #               "/public/home/chenlong666/desktop/PretrainModels/examples/data/regression_example/"')
#         # cmd = 'python "/public/home/chenlong666/desktop/PretrainModels/bt_pro/generate_bt_fps.py" \
#         #     --model_name_or_path "/public/home/chenlong666/desktop/PretrainModels/examples/models/finetuned_model_regression/" \
#         #     --checkpoint_file "checkpoint_best.pt" --data_name_or_path  \
#         #     "/public/home/chenlong666/desktop/PretrainModels/examples/data/regression_example/" \
#         #     --dict_file "/public/home/chenlong666/desktop/PretrainModels/examples/data/regression_example/dict.txt" \
#         #     --target_file "/public/home/chenlong666/desktop/original_data/{}/{}_regression_train_{}.smi" \
#         #     --save_feature_path "/public/home/chenlong666/desktop/result/BET_f_npy/{}_train_BET_f_{}.npy"' \
#         #     .format(model, model, fold, model, fold)
#         # os.system(cmd)
#         #
#         # cmd = 'python "/public/home/chenlong666/desktop/PretrainModels/bt_pro/generate_bt_fps.py" \
#         #             --model_name_or_path "/public/home/chenlong666/desktop/PretrainModels/examples/models/finetuned_model_regression/" \
#         #             --checkpoint_file "checkpoint_best.pt" --data_name_or_path  \
#         #             "/public/home/chenlong666/desktop/PretrainModels/examples/data/regression_example/" \
#         #             --dict_file "/public/home/chenlong666/desktop/PretrainModels/examples/data/regression_example/dict.txt" \
#         #             --target_file "/public/home/chenlong666/desktop/original_data/{}/{}_regression_test_{}.smi" \
#         #             --save_feature_path "/public/home/chenlong666/desktop/result/BET_f_npy/{}_test_BET_f_{}.npy"' \
#         #     .format(model, model, fold, model, fold)
#         # os.system(cmd)
#         #
#         # cmd = 'python "/public/home/chenlong666/desktop/PretrainModels/bt_pro/generate_bt_fps.py" \
#         #     --model_name_or_path "/public/home/chenlong666/desktop/PretrainModels/examples/models/finetuned_model_regression/" \
#         #     --checkpoint_file "checkpoint_best.pt" --data_name_or_path  \
#         #     "/public/home/chenlong666/desktop/PretrainModels/examples/data/regression_example/" \
#         #     --dict_file "/public/home/chenlong666/desktop/PretrainModels/examples/data/regression_example/dict.txt" \
#         #     --target_file "/public/home/chenlong666/desktop/original_data/{}/{}_regression_valid_{}.smi" \
#         #     --save_feature_path "/public/home/chenlong666/desktop/result/BET_f_npy/{}_valid_BET_f_{}.npy"' \
#         #     .format(model, model, fold, model, fold)
#         # os.system(cmd)
#         # print('step4 finished!')

#     #     path_BET_npy = '/public/home/chenlong666/desktop/result/BET_npy/'
#     #     path_BET_f_npy = '/public/home/chenlong666/desktop/result/BET_f_npy/'
#     #     path_AE_npy = '/public/home/chenlong666/desktop/result/AE_csv/'
#     #     X_train_1 = np.loadtxt(path_AE_npy + '{}_train_AE_{}.csv'.format(model,fold),
#     #                         allow_pickle=True)
#     #     X_train_2 = np.loadtxt(path_AE_npy + '{}_valid_AE_{}.csv'.format(model,fold),
#     #                         allow_pickle=True)
#     #     X_train = np.concatenate((X_train_1, X_train_2))
#     #     print('shape of X_train_1:', np.shape(X_train_1))
#     #     print('shape of X_train_2:', np.shape(X_train_2))
#     #     print('shape of X_train:', np.shape(X_train))
#     #     X_test = np.loadtxt(path_AE_npy + '{}_test_AE_{}.csv'.format(model,fold),
#     #                      allow_pickle=True)
#     #     print('shape of X_test:', np.shape(X_test))
#     #     X_train = normalize(X_train)
#     #     X_test = normalize(X_test)
#     #
#     #     y_train_1 = [float(i.strip()) for i in
#     #                  open(path_smi + '{}_regression_train_{}.label'.format(model,fold),
#     #                       'r').readlines()]
#     #     y_train_2 = [float(i.strip()) for i in
#     #                  open(path_smi + '{}_regression_valid_{}.label'.format(model,fold),
#     #                       'r').readlines()]
#     #     y_train = np.concatenate((y_train_1, y_train_2))
#     #     print('shape of y_train_1:', np.shape(y_train_1))
#     #     print('shape of y_train_2:', np.shape(y_train_2))
#     #     print('shape of y_train:', np.shape(y_train))
#     #     # print(type(y_train))
#     #     # print(y_train)
#     #     y_test = np.array([float(i.strip()) for i in
#     #                        open(path_smi + '{}_regression_test_{}.label'.format(model,fold),
#     #                             'r').readlines()])
#     #     print('shape of y_test:', np.shape(y_test))
#     #     # print(type(y_test))
#     #     # print(y_test)
#     #
#     #     print('>>>>>>>>>>>>>training.............', flush=True)
#     #     GBR = GradientBoostingRegressor(n_estimators      = args.n_estimators, \
#     #                                     learning_rate     = args.learning_rate, \
#     #                                     max_features      = args.max_features, \
#     #                                     max_depth         = args.max_depth, \
#     #                                     min_samples_split = args.min_samples_split, \
#     #                                     subsample         = args.subsample, \
#     #                                     n_iter_no_change  = args.n_iter_no_change, \
#     #                                     criterion         = args.criterion, \
#     #                                     loss              = args.loss, \
#     #                                     random_state      = args.random_seed)
#     #     GBR.fit(X_train, y_train)
#     #     results[test_idx] = GBR.predict(X_test)
#     #     y_pred = GBR.predict(X_test)
#     #
#     #     RMSD = np.sqrt(mean_squared_error(y_test, y_pred))
#     #     pearsonr = scipy.stats.pearsonr(y_test, y_pred)
#     #     r2 = r2_score(y_test, y_pred)
#     #     print('RMSD: %f, P^2: %f, R^2: %f' % (RMSD, pearsonr[0] * pearsonr[0], r2), flush=True)
#     #
#     # RMSD = np.sqrt(mean_squared_error(y_val, results))
#     # pearsonr = scipy.stats.pearsonr(y_val, results)
#     # determination = r2_score(y_val, results)
#     # print('%d-th Final RMSD: %f, P^2 %f, R^2: %f' % (ii, RMSD, pearsonr[0] * pearsonr[0], determination), flush=True)

# t_end = time.time()
# print('total time:', (t_end - t_start) / 3600, 'h', flush=True)
import numpy as np
import os
import argparse
import sys
from sklearn.model_selection import KFold
from sklearn.preprocessing import StandardScaler
import time

os.environ['MKL_THREADING_LAYER'] = 'GNU'
os.environ['MKL_SERVICE_FORCE_INTEL'] = '1'

t_start = time.time()

def normalize(X):
    scaler = StandardScaler().fit(X)
    return scaler.transform(X)

# ===============================
# 输入参数
# ===============================
model = sys.argv[1]

path_smi = f'/share/home/u2415173011/Aldisease/TOP25_CHEMBL/AE/{model}/'
path_label = path_smi

# ===============================
# 读取 SMILES
# ===============================
with open(path_smi + f'{model}.smi', 'r') as f:
    data = np.array([line.strip() for line in f.readlines()])

print('size of data:', np.shape(data), flush=True)

# ===============================
# 读取标签
# ===============================
y_val_list = []
with open(path_label + f'label_{model}.csv', 'r') as f:
    for line in f:
        y_val_list.append(float(line.strip()))

y_val = np.array(y_val_list)
print('size of y_val:', np.shape(y_val), flush=True)

# ===============================
# 划分训练集大小
# ===============================
train_size = int(0.8 * len(data))
print('size of train size:', train_size, flush=True)

# ===============================
# 10-fold CV
# ===============================
kf = KFold(n_splits=10, shuffle=True, random_state=0)

fold = 0
for train_idx, test_idx in kf.split(data):
    fold += 1
    print('fold =', fold, flush=True)

    X_trainset, X_testset = data[train_idx], data[test_idx]
    y_train, y_test = y_val[train_idx], y_val[test_idx]

    test_num = len(X_testset)
    train_num = train_size
    valid_num = len(X_trainset) - train_num

    print('train_num:', train_num)
    print('valid_num:', valid_num)
    print('test_num:', test_num)

    # ===============================
    # 写入 SMILES
    # ===============================
    with open(path_smi + f'{model}_regression_train_{fold}.smi', 'w') as f:
        for i in range(train_num):
            f.write(X_trainset[i] + '\n')

    with open(path_smi + f'{model}_regression_valid_{fold}.smi', 'w') as f:
        for i in range(train_num, train_num + valid_num):
            f.write(X_trainset[i] + '\n')

    with open(path_smi + f'{model}_regression_test_{fold}.smi', 'w') as f:
        for i in range(test_num):
            f.write(X_testset[i] + '\n')

    # ===============================
    # 写入 label
    # ===============================
    with open(path_smi + f'{model}_regression_train_{fold}.label', 'w') as f:
        for i in range(train_num):
            f.write(str(y_train[i]) + '\n')

    with open(path_smi + f'{model}_regression_valid_{fold}.label', 'w') as f:
        for i in range(train_num, train_num + valid_num):
            f.write(str(y_train[i]) + '\n')

    with open(path_smi + f'{model}_regression_test_{fold}.label', 'w') as f:
        for i in range(test_num):
            f.write(str(y_test[i]) + '\n')

    print('step1 finished!', flush=True)

    # ===============================
    # 生成 AE 特征（关键修复）
    # ===============================
    print("Generating AE features...", flush=True)

    cmd_train = f'cddd --input {path_smi}{model}_regression_train_{fold}.smi --out {path_smi}{model}_train_AE_{fold}.csv --no-preprocess'
    cmd_valid = f'cddd --input {path_smi}{model}_regression_valid_{fold}.smi --out {path_smi}{model}_valid_AE_{fold}.csv --no-preprocess'
    cmd_test  = f'cddd --input {path_smi}{model}_regression_test_{fold}.smi  --out {path_smi}{model}_test_AE_{fold}.csv  --no-preprocess'

    os.system(cmd_train)
    os.system(cmd_valid)
    os.system(cmd_test)

    print("AE features done!", flush=True)

t_end = time.time()
print('total time:', (t_end - t_start) / 3600, 'h', flush=True)