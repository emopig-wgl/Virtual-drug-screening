# from sklearn.svm import SVR
# from sklearn.metrics import accuracy_score
# from sklearn.ensemble import RandomForestRegressor
# import numpy as np
# import scipy.stats
# from sklearn.ensemble import GradientBoostingRegressor
# from sklearn.linear_model import LinearRegression
# from sklearn.metrics import mean_squared_error
# from sklearn.model_selection import KFold
# from sklearn.preprocessing import StandardScaler
# import pickle, scipy, h5py, argparse, sys, os
# from random import randrange, seed
# from sklearn.metrics import matthews_corrcoef
# from sklearn.metrics import roc_auc_score
# from sklearn.metrics import r2_score
# import time, csv

# os.environ['MKL_THREADING_LAYER'] = 'GNU'
# os.environ['MKL_SERVICE_FORCE_INTEL'] = '1'

# t_start = time.time()


# # 定义一个归一化函数，使用StandardScaler对数据进行归一化处理
# def normalize(X):
#     scaler = StandardScaler().fit(X)
#     return scaler.transform(X)


# # 定义一个函数，将CSV文件转换为numpy数组。
# def csv_to_npy(filename):
#     nlist = []
#     with open(filename, encoding='utf-8-sig') as f:
#         for row in csv.reader(f, skipinitialspace=True):
#             # print(row)
#             if 'cddd_1' in row:  # 删除第一行
#                 continue
#             row_list = []
#             for i in row[2:]:
#                 row_list.append(eval(i))
#             nlist.append(row_list)
#     f.close()
#     nlist = np.array(nlist)
#     return nlist


# # 输入文件的类别名称、从命令行参数获取数据集名称、设置SMILES字符串和标签的路径、读取SMILES字符串文件，并将其转换为numpy数组。
# model = sys.argv[1]  # 数据集名称，如CHEMBL205
# path_smi = '/public/home/chenlong666/Chunhuanzhang/path_smi/{}/'.format(model)
# path_label = '/public/home/chenlong666/Chunhuanzhang/path_smi/{}/'.format(model)
# file = open(path_smi + '{}.smi'.format(model, model), 'r')
# data = [line for line in file.readlines()]
# data = np.array(data)
# print('size of data:', np.shape(data), flush=True)
# # y_val = np.load(path_label + 'label_%s_%s_reg.npy' % (target_ID, cator), allow_pickle=True)

# # 获取标签文件的矩阵形式
# # 读取标签文件，并将其转换为numpy数组。
# y_val_ori = open(path_label + 'label_{}.csv'.format(model, model), 'r')
# y_val_list = []
# for i in y_val_ori.readlines():
#     i = eval(i.strip())
#     y_val_list.append(i)
# y_val = np.array(y_val_list)
# # print('size of y_val:', np.shape(y_val), flush=True)

# # 设置训练集大小为数据总量的80%。
# train_size = int(float(np.shape(data)[0]) * 0.8)  # 训练集大小
# print('size of train size:', train_size, flush=True)
# # 设置机器学习参数，根据训练集的大小设置GBDT模型的不同参数。
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

# # 使用argparse库解析命令行参数，并打印出来。
# paperGBDT = argparse.ArgumentParser(description='GBDT inputs')
# paperGBDT.add_argument('--n_estimators', default=10000, type=int,
#                        help='Maximum tree depth')
# paperGBDT.add_argument('--dataset', default=model, type=str,
#                        help='Dataset selected')
# paperGBDT.add_argument('--max_depth', default=max_depth, type=int,
#                        help='Maximum tree depth')
# paperGBDT.add_argument('--learning_rate', default=0.01, type=float,
#                        help='Learning rate for gbrt')
# paperGBDT.add_argument('--criterion', default='friedman_mse', type=str,
#                        help='Loss function for gbrt')
# paperGBDT.add_argument('--subsample', default=subsample, type=float,
#                        help='Subsample for fitting individual learners')
# paperGBDT.add_argument('--max_features', default='sqrt', type=str,
#                        help='Number of features to be considered')
# paperGBDT.add_argument('--min_samples_split', default=min_samples_split, type=int,
#                        help='Minimum sample num of each leaf node.')
# paperGBDT.add_argument('--loss', default='ls', type=str,
#                        help='Loss function to be optimized.')
# paperGBDT.add_argument('--n_iter_no_change', default=None, type=int,
#                        help='Early stopping will be used to terminate training')
# paperGBDT.add_argument('--random_seed', default=0, type=int,
#                        help='random seed')
# # args = paperGBDT.parse_args() # 报错
# argsGBDT = paperGBDT.parse_known_args()[0]
# print('GBDT parameter', flush=True)
# print(argsGBDT, flush=True)

# # paperRF = argparse.ArgumentParser(description='RF inputs')
# # paperRF.add_argument('--n_estimators', default=10000, type=int,
# #                      help='Number of trees in the forest')
# # paperRF.add_argument('--dataset', default=model, type=str,
# #                      help='Dataset selected')
# # paperRF.add_argument('--max_depth', default=max_depth, type=int,
# #                      help='Maximum depth of the trees')
# # paperRF.add_argument('--min_samples_split', default=min_samples_split, type=int,
# #                      help='Minimum number of samples required to split a node')
# # paperRF.add_argument('--min_samples_leaf', default=min_samples_leaf, type=int,
# #                      help='Minimum number of samples required to be at a leaf node')
# # paperRF.add_argument('--criterion', default='mse', type=str,
# #                      help='Function to measure the quality of a split')
# # paperRF.add_argument('--random_seed', default=0, type=int,
# #                      help='random seed')
# # # args = paperRF.parse_args() # 报错
# # argsRF = paperRF.parse_known_args()[0]
# # print('RF parameter', flush=True)
# # print(argsRF, flush=True)
# #
# # paperSVM = argparse.ArgumentParser(description='SVM inputs')
# #
# # paperSVM.add_argument('--dataset', default=model, type=str,
# #                       help='Dataset selected')
# # paperSVM.add_argument('--C', default=C, type=float,
# #                       help='Penalty parameter C of the error term')
# # paperSVM.add_argument('--kernel', default='rbf', type=str,
# #                       help='Kernel type to be used in the algorithm')
# # paperSVM.add_argument('--gamma', default='scale', type=str,
# #                       help='Kernel coefficient for rbf, poly and sigmoid')
# # paperSVM.add_argument('--random_seed', default=0, type=int,
# #                       help='random seed')
# # argsSVM = paperSVM.parse_known_args()[0]
# # print('SVM parameter', flush=True)
# # print(argsSVM, flush=True)

# # 初始化结果数组
# for ii in range(1):

#     ##初始化几个numpy数组
#     GBDT_results_AE = np.zeros(y_val.shape)
#     GBDT_results_BET = np.zeros(y_val.shape)
#     GBDT_results_ECFP = np.zeros(y_val.shape)
#     GBDT_results_AE_BET = np.zeros(y_val.shape)
#     GBDT_results_AE_ECFP = np.zeros(y_val.shape)
#     GBDT_results_BET_ECFP = np.zeros(y_val.shape)
#     GBDT_results_AE_BET_ECFP = np.zeros(y_val.shape)

#     # RF_results = np.zeros(y_val.shape)
#     # RF_results_BET = np.zeros(y_val.shape)
#     # RF_results_AE = np.zeros(y_val.shape)
#     # SVM_results = np.zeros(y_val.shape)
#     # SVM_results_BET = np.zeros(y_val.shape)
#     # SVM_results_AE = np.zeros(y_val.shape)

#     ##十折交叉验证
#     kf = KFold(n_splits=10, shuffle=True, random_state=ii)
#     fold = 0
#     for train_idx, test_idx in kf.split(data):
#         fold += 1
#         print('fold=', fold, flush=True)
#         #####################################################路径###########################################
#         path_BET_npy = '/public/home/chenlong666/Chunhuanzhang/huizong_GBDT/all_BET_npy/'
#         # path_BET_f_npy = '/public/home/chenlong666/desktop/my_desk2/result/BET_f_npy/'
#         path_AE_npy = '/public/home/chenlong666/Chunhuanzhang/huizong_GBDT/all_AE_CSV/'
#         path_ECFP_npy = '/public/home/chenlong666/Chunhuanzhang/huizong_GBDT/all_ECFP_npy/'  # 新增ECFP特征路径

#         #####################################################BET###########################################
#         X_train_1_BET = np.load(path_BET_npy + '{}_train_BET_{}.npy'.format(model, fold),
#                                 allow_pickle=True)
#         X_train_2_BET = np.load(path_BET_npy + '{}_valid_BET_{}.npy'.format(model, fold),
#                                 allow_pickle=True)
#         X_train_BET = np.concatenate((X_train_1_BET, X_train_2_BET))
#         # print('shape of X_train_1_BET:', np.shape(X_train_1_BET))
#         # print('shape of X_train_2_BET:', np.shape(X_train_2_BET))
#         # print('shape of X_train_BET:', np.shape(X_train_BET))
#         X_test_BET = np.load(path_BET_npy + '{}_test_BET_{}.npy'.format(model, fold),
#                              allow_pickle=True)
#         # print('shape of X_test_BET:', np.shape(X_test_BET))
#         X_train_BET = normalize(X_train_BET)
#         X_test_BET = normalize(X_test_BET)

#         y_train_1_BET = [float(i.strip()) for i in
#                          open(path_smi + '{}_regression_train_{}.label'.format(model, fold),
#                               'r').readlines()]
#         y_train_2_BET = [float(i.strip()) for i in
#                          open(path_smi + '{}_regression_valid_{}.label'.format(model, fold),
#                               'r').readlines()]
#         y_train_BET = np.concatenate((y_train_1_BET, y_train_2_BET))
#         # print('shape of y_train_1_BET:', np.shape(y_train_1_BET))
#         # print('shape of y_train_2_BET:', np.shape(y_train_2_BET))
#         # print('shape of y_train_BET:', np.shape(y_train_BET))
#         # print(type(y_train))
#         # print(y_train)
#         y_test_BET = np.array([float(i.strip()) for i in
#                                open(path_smi + '{}_regression_test_{}.label'.format(model, fold),
#                                     'r').readlines()])

#         #####################################################AE###########################################
#         X_train_1_AE = csv_to_npy(path_AE_npy + '{}_train_AE_{}.csv'.format(model, fold), )
#         X_train_2_AE = csv_to_npy(path_AE_npy + '{}_valid_AE_{}.csv'.format(model, fold), )
#         X_train_AE = np.concatenate((X_train_1_AE, X_train_2_AE))
#         # print('shape of X_train_1_AE:', np.shape(X_train_1_AE))
#         # print('shape of X_train_2_AE:', np.shape(X_train_2_AE))
#         # print('shape of X_train:', np.shape(X_train_AE))
#         X_test_AE = csv_to_npy(path_AE_npy + '{}_test_AE_{}.csv'.format(model, fold), )
#         # print('shape of X_test_AE:', np.shape(X_test_AE))
#         X_train_AE = normalize(X_train_AE)
#         X_test_AE = normalize(X_test_AE)

#         y_train_1_AE = [float(i.strip()) for i in
#                         open(path_smi + '{}_regression_train_{}.label'.format(model, fold),
#                              'r').readlines()]
#         y_train_2_AE = [float(i.strip()) for i in
#                         open(path_smi + '{}_regression_valid_{}.label'.format(model, fold),
#                              'r').readlines()]
#         y_train_AE = np.concatenate((y_train_1_AE, y_train_2_AE))
#         # print('shape of y_train_1_AE:', np.shape(y_train_1_AE))
#         # print('shape of y_train_2_AE:', np.shape(y_train_2_AE))
#         # print('shape of y_train_AE:', np.shape(y_train_AE))
#         # print(type(y_train))
#         # print(y_train)
#         y_test_AE = np.array([float(i.strip()) for i in
#                               open(path_smi + '{}_regression_test_{}.label'.format(model, fold),
#                                    'r').readlines()])
#         # print('shape of y_test_AE:', np.shape(y_test_AE))
#         # print(type(y_test))
#         # print(y_test)

#         #####################################################ECFP###########################################
#         X_train_1_ECFP = np.load(path_ECFP_npy + '{}_train_ECFP_{}.npy'.format(model, fold),
#                                  allow_pickle=True)
#         X_train_2_ECFP = np.load(path_ECFP_npy + '{}_valid_ECFP_{}.npy'.format(model, fold),
#                                  allow_pickle=True)
#         X_train_ECFP = np.concatenate((X_train_1_ECFP, X_train_2_ECFP))
#         # print('shape of X_train_1_BET:', np.shape(X_train_1_BET))
#         # print('shape of X_train_2_BET:', np.shape(X_train_2_BET))
#         # print('shape of X_train_BET:', np.shape(X_train_BET))
#         X_test_ECFP = np.load(path_ECFP_npy + '{}_test_ECFP_{}.npy'.format(model, fold),
#                               allow_pickle=True)
#         # print('shape of X_test_BET:', np.shape(X_test_BET))
#         X_train_ECFP = normalize(X_train_ECFP)
#         X_test_ECFP = normalize(X_test_ECFP)

#         y_train_1_ECFP = [float(i.strip()) for i in
#                           open(path_smi + '{}_regression_train_{}.label'.format(model, fold),
#                                'r').readlines()]
#         y_train_2_ECFP = [float(i.strip()) for i in
#                           open(path_smi + '{}_regression_valid_{}.label'.format(model, fold),
#                                'r').readlines()]
#         y_train_ECFP = np.concatenate((y_train_1_ECFP, y_train_2_ECFP))
#         # print('shape of y_train_1_BET:', np.shape(y_train_1_BET))
#         # print('shape of y_train_2_BET:', np.shape(y_train_2_BET))
#         # print('shape of y_train_BET:', np.shape(y_train_BET))
#         # print(type(y_train))
#         # print(y_train)
#         y_test_ECFP = np.array([float(i.strip()) for i in
#                                 open(path_smi + '{}_regression_test_{}.label'.format(model, fold),
#                                      'r').readlines()])
#         # print('shape of y_test_BET:', np.shape(y_test_BET))
#         # print(type(y_test))
#         # print(y_test)

#         #####################################################AE###########################################
#         print('>>>>>>>>>>>>>training.............', flush=True)
#         # print('>>>>>>>>>>>>>GBDTtraining.............', flush=True)
#         print(
#             '###############################################GBDT#####################################################',
#             flush=True)

#         ##初始化GBR模型，并设置相关参数
#         GBR = GradientBoostingRegressor(n_estimators=argsGBDT.n_estimators, \
#                                         learning_rate=argsGBDT.learning_rate, \
#                                         max_features=argsGBDT.max_features, \
#                                         max_depth=argsGBDT.max_depth, \
#                                         min_samples_split=argsGBDT.min_samples_split, \
#                                         subsample=argsGBDT.subsample, \
#                                         n_iter_no_change=argsGBDT.n_iter_no_change, \
#                                         criterion=argsGBDT.criterion, \
#                                         loss=argsGBDT.loss, \
#                                         random_state=argsGBDT.random_seed)

#         # 使用BET特征进行训练和评估
#         GBR.fit(X_train_BET, y_train_BET)  # 使用BET特征训练GBR模型，X_train_BET 是训练集的BET特征数据。y_train_BET 是训练集的标签数据
#         GBDT_results_BET[test_idx] = GBR.predict(
#             X_test_BET)  # 这行代码使用训练好的GBR模型对测试集的BET特征数据进行预测，X_test_BET 是测试集的BET特征数据，GBDT_results_BET[test_idx] 将预测结果存储在对应的位置。
#         GBDT_y_pred_BET = GBR.predict(X_test_BET)  # 再次使用训练好的GBR模型对测试集的BET特征数据进行预测,GBDT_y_pred_BET 存储预测结果。
#         # print(f'y_test_BET：{y_test_BET}', flush=True)
#         print(f'GBDT_BET的BA值：{np.min(GBDT_y_pred_BET)}', flush=True)  # 打印GBDT模型在BET特征上的预测结果的最小值
#         GBDT_RMSD_BET = np.sqrt(mean_squared_error(y_test_BET, GBDT_y_pred_BET))  # 计算GBDT模型在BET特征上的均方根误差（RMSD
#         GBDT_pearsonr_BET = scipy.stats.pearsonr(y_test_BET, GBDT_y_pred_BET)  # GBDT模型在BET特征上的皮尔逊相关系数
#         GBDT_r2_BET = r2_score(y_test_BET, GBDT_y_pred_BET)  # 计算GBDT模型在BET特征上的R^2评分
#         print('GBDT_BET:RMSD: %f, P: %f, R^2: %f' % (
#             GBDT_RMSD_BET, GBDT_pearsonr_BET[0] , GBDT_r2_BET), flush=True)

#         # 使用AE特征进行训练和评估
#         GBR.fit(X_train_AE, y_train_AE)
#         GBDT_results_AE[test_idx] = GBR.predict(X_test_AE)
#         GBDT_y_pred_AE = GBR.predict(X_test_AE)
#         print(f'GBDT_AE的BA值 ：{np.min(GBDT_y_pred_AE)}', flush=True)
#         GBDT_RMSD_AE = np.sqrt(mean_squared_error(y_test_AE, GBDT_y_pred_AE))
#         GBDT_pearsonr_AE = scipy.stats.pearsonr(y_test_AE, GBDT_y_pred_AE)
#         GBDT_r2_AE = r2_score(y_test_AE, GBDT_y_pred_AE)
#         print('GBDT_AE :RMSD: %f, P: %f, R^2: %f' % (
#             GBDT_RMSD_AE, GBDT_pearsonr_AE[0], GBDT_r2_AE), flush=True)

#         # 使用ECFP特征进行训练和评估
#         GBR.fit(X_train_ECFP, y_train_ECFP)
#         GBDT_results_ECFP[test_idx] = GBR.predict(X_test_ECFP)
#         GBDT_y_pred_ECFP = GBR.predict(X_test_ECFP)
#         print(f'GBDT_ECFP的BA值 ：{np.min(GBDT_y_pred_ECFP)}', flush=True)
#         GBDT_RMSD_ECFP = np.sqrt(mean_squared_error(y_test_ECFP, GBDT_y_pred_ECFP))
#         GBDT_pearsonr_ECFP = scipy.stats.pearsonr(y_test_ECFP, GBDT_y_pred_ECFP)
#         GBDT_r2_ECFP = r2_score(y_test_ECFP, GBDT_y_pred_ECFP)
#         print('GBDT_ECFP :RMSD: %f, P: %f, R^2: %f' % (
#             GBDT_RMSD_ECFP, GBDT_pearsonr_ECFP[0] , GBDT_r2_ECFP), flush=True)

#         ##AE与BET特征组合
#         GBDT_results_AE_BET[test_idx] = (GBDT_results_BET[test_idx] + GBDT_results_AE[test_idx]) / 2
#         GBDT_y_pred_AE_BET = (GBDT_y_pred_BET + GBDT_y_pred_AE) / 2
#         y_test_AE_BET = (y_test_AE + y_test_BET) / 2
#         print(f'GBDT_AE_BET的BA值    ：{np.min(GBDT_y_pred_AE_BET)}', flush=True)
#         GBDT_RMSD_AE_BET = np.sqrt(mean_squared_error(y_test_AE_BET, GBDT_y_pred_AE_BET))
#         GBDT_pearsonr_AE_BET = scipy.stats.pearsonr(y_test_AE_BET, GBDT_y_pred_AE_BET)
#         GBDT_r2_AE_BET = r2_score(y_test_AE_BET, GBDT_y_pred_AE_BET)
#         print('GBDT_AE_BET    :RMSD: %f, P: %f, R^2: %f' % (
#         GBDT_RMSD_AE_BET, GBDT_pearsonr_AE_BET[0] , GBDT_r2_AE_BET),
#               flush=True)

#         ##AE与ECFP特征组合
#         GBDT_results_AE_ECFP[test_idx] = (GBDT_results_ECFP[test_idx] + GBDT_results_AE[test_idx]) / 2
#         GBDT_y_pred_AE_ECFP = (GBDT_y_pred_ECFP + GBDT_y_pred_AE) / 2
#         y_test_AE_ECFP = (y_test_ECFP + y_test_AE) / 2
#         print(f'GBDT_AE_ECFP的BA值    ：{np.min(GBDT_y_pred_AE_ECFP)}', flush=True)
#         GBDT_RMSD_AE_ECFP = np.sqrt(mean_squared_error(y_test_AE_ECFP, GBDT_y_pred_AE_ECFP))
#         GBDT_pearsonr_AE_ECFP = scipy.stats.pearsonr(y_test_AE_ECFP, GBDT_y_pred_AE_ECFP)
#         GBDT_r2_AE_ECFP = r2_score(y_test_AE_ECFP, GBDT_y_pred_AE_ECFP)
#         print('GBDT_AE_ECFP    :RMSD: %f, P: %f, R^2: %f' % (
#         GBDT_RMSD_AE_ECFP, GBDT_pearsonr_AE_ECFP[0] , GBDT_r2_AE_ECFP),
#               flush=True)

#         ##BET与ECFP特征组合
#         GBDT_results_BET_ECFP[test_idx] = (GBDT_results_ECFP[test_idx] + GBDT_results_BET[test_idx]) / 2
#         GBDT_y_pred_BET_ECFP = (GBDT_y_pred_ECFP + GBDT_y_pred_BET) / 2
#         y_test_BET_ECFP = (y_test_ECFP + y_test_BET) / 2
#         print(f'GBDT_BET_ECFP的BA值    ：{np.min(GBDT_y_pred_BET_ECFP)}', flush=True)
#         GBDT_RMSD_BET_ECFP = np.sqrt(mean_squared_error(y_test_BET_ECFP, GBDT_y_pred_BET_ECFP))
#         GBDT_pearsonr_BET_ECFP = scipy.stats.pearsonr(y_test_BET_ECFP, GBDT_y_pred_BET_ECFP)
#         GBDT_r2_BET_ECFP = r2_score(y_test_BET_ECFP, GBDT_y_pred_BET_ECFP)
#         print('GBDT_BET_ECFP    :RMSD: %f, P: %f, R^2: %f' % (
#         GBDT_RMSD_BET_ECFP, GBDT_pearsonr_BET_ECFP[0] , GBDT_r2_BET_ECFP),
#               flush=True)

#         ##AE、BET与ECFP特征组合
#         GBDT_results_AE_BET_ECFP[test_idx] = (GBDT_results_ECFP[test_idx] + GBDT_results_BET[test_idx] +
#                                               GBDT_results_AE[test_idx]) / 3
#         GBDT_y_pred_AE_BET_ECFP = (GBDT_y_pred_ECFP + GBDT_y_pred_BET + GBDT_y_pred_AE) / 3
#         y_test_AE_BET_ECFP = (y_test_ECFP + y_test_BET + y_test_AE) / 3
#         print(f'GBDT_AE_BET_ECFP的BA值    ：{np.min(GBDT_y_pred_AE_BET_ECFP)}', flush=True)
#         GBDT_RMSD_AE_BET_ECFP = np.sqrt(mean_squared_error(y_test_AE_BET_ECFP, GBDT_y_pred_AE_BET_ECFP))
#         GBDT_pearsonr_AE_BET_ECFP = scipy.stats.pearsonr(y_test_AE_BET_ECFP, GBDT_y_pred_AE_BET_ECFP)
#         GBDT_r2_AE_BET_ECFP = r2_score(y_test_AE_BET_ECFP, GBDT_y_pred_AE_BET_ECFP)
#         print('GBDT_AE_BET_ECFP    :RMSD: %f, P: %f, R^2: %f' % (
#         GBDT_RMSD_AE_BET_ECFP, GBDT_pearsonr_AE_BET_ECFP[0] , GBDT_r2_AE_BET_ECFP),
#               flush=True)



#     #######################################################最终结果#######################################################################
#     print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@最终结果@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@',
#           flush=True)
#     print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@最终结果@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@',
#           flush=True)
#     print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%GBDT%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%',
#           flush=True)

#     ##BET
#     GBDT_RMSD_BET = np.sqrt(mean_squared_error(y_val, GBDT_results_BET))
#     GBDT_pearsonr_BET = scipy.stats.pearsonr(y_val, GBDT_results_BET)
#     GBDT_determination_BET = r2_score(y_val, GBDT_results_BET)
#     print('GBDT_BET:%d-th Final RMSD: %f, Final P: %f, Final R^2: %f' % (
#         ii, GBDT_RMSD_BET, GBDT_pearsonr_BET[0] , GBDT_determination_BET), flush=True)

#     ##AE
#     GBDT_RMSD_AE = np.sqrt(mean_squared_error(y_val, GBDT_results_AE))
#     GBDT_pearsonr_AE = scipy.stats.pearsonr(y_val, GBDT_results_AE)
#     GBDT_determination_AE = r2_score(y_val, GBDT_results_AE)
#     print('GBDT_AE :%d-th Final RMSD: %f, Final P: %f, Final R^2: %f' % (
#         ii, GBDT_RMSD_AE, GBDT_pearsonr_AE[0] , GBDT_determination_AE), flush=True)

#     ##ECFP
#     GBDT_RMSD_ECFP = np.sqrt(mean_squared_error(y_val, GBDT_results_ECFP))
#     GBDT_pearsonr_ECFP = scipy.stats.pearsonr(y_val, GBDT_results_ECFP)
#     GBDT_determination_ECFP = r2_score(y_val, GBDT_results_ECFP)
#     print('GBDT_ECFP :%d-th Final RMSD: %f, Final P: %f, Final R^2: %f' % (
#         ii, GBDT_RMSD_ECFP, GBDT_pearsonr_ECFP[0] , GBDT_determination_ECFP), flush=True)

#     ##AE_BET
#     GBDT_RMSD_AE_BET = np.sqrt(mean_squared_error(y_val, GBDT_results_AE_BET))
#     GBDT_pearsonr_AE_BET = scipy.stats.pearsonr(y_val, GBDT_results_AE_BET)
#     GBDT_determination_AE_BET = r2_score(y_val, GBDT_results_AE_BET)
#     print('GBDT_AE_BET    :%d-th Final RMSD: %f, Final P: %f, Final R^2: %f' % (
#         ii, GBDT_RMSD_AE_BET, GBDT_pearsonr_AE_BET[0] , GBDT_determination_AE_BET), flush=True)

#     ##AE_ECFP
#     GBDT_RMSD_AE_ECFP = np.sqrt(mean_squared_error(y_val, GBDT_results_AE_ECFP))
#     GBDT_pearsonr_AE_ECFP = scipy.stats.pearsonr(y_val, GBDT_results_AE_ECFP)
#     GBDT_determination_AE_ECFP = r2_score(y_val, GBDT_results_AE_ECFP)
#     print('GBDT_AE_ECFP    :%d-th Final RMSD: %f, Final P: %f, Final R^2: %f' % (
#         ii, GBDT_RMSD_AE_ECFP, GBDT_pearsonr_AE_ECFP[0] , GBDT_determination_AE_ECFP),
#           flush=True)

#     ##BET_ECFP
#     GBDT_RMSD_BET_ECFP = np.sqrt(mean_squared_error(y_val, GBDT_results_BET_ECFP))
#     GBDT_pearsonr_BET_ECFP = scipy.stats.pearsonr(y_val, GBDT_results_BET_ECFP)
#     GBDT_determination_BET_ECFP = r2_score(y_val, GBDT_results_BET_ECFP)
#     print('GBDT_BET_ECFP    :%d-th Final RMSD: %f, Final P: %f, Final R^2: %f' % (
#         ii, GBDT_RMSD_BET_ECFP, GBDT_pearsonr_BET_ECFP[0], GBDT_determination_BET_ECFP),
#           flush=True)

#     ##AE_BET_ECFP
#     GBDT_RMSD_AE_BET_ECFP = np.sqrt(mean_squared_error(y_val, GBDT_results_AE_BET_ECFP))
#     GBDT_pearsonr_AE_BET_ECFP = scipy.stats.pearsonr(y_val, GBDT_results_AE_BET_ECFP)
#     GBDT_determination_AE_BET_ECFP = r2_score(y_val, GBDT_results_AE_BET_ECFP)
#     print('GBDT_AE_BET_ECFP    :%d-th Final RMSD: %f, Final P: %f, Final R^2: %f' % (
#         ii, GBDT_RMSD_AE_BET_ECFP, GBDT_pearsonr_AE_BET_ECFP[0] ,
#         GBDT_determination_AE_BET_ECFP),
#           flush=True)

#     # print(f'{ii}-th GBDT_BET的BA值：{np.min(GBDT_y_pred_BET):f}', flush=True)
#     # print(f'{ii}-th GBDT_AE的BA值 ：{np.min(GBDT_y_pred_AE):f}', flush=True)
#     # print(f'{ii}-th GBDT的BA值    ：{np.min(GBDT_y_pred):f}', flush=True)
#     print(f'{ii}-th GBDT_AE的BA值 ：{np.min(GBDT_results_AE):f}', flush=True)
#     print(f'{ii}-th GBDT_BET的BA值：{np.min(GBDT_results_BET):f}', flush=True)
#     print(f'{ii}-th GBDT_ECFP的BA值 ：{np.min(GBDT_results_ECFP):f}', flush=True)
#     print(f'{ii}-th GBDT_AE_BET的BA值：{np.min(GBDT_results_AE_BET):f}', flush=True)
#     print(f'{ii}-th GBDT_AE_ECFP的BA值    ：{np.min(GBDT_results_AE_ECFP):f}', flush=True)
#     print(f'{ii}-th GBDT_BET_ECFP的BA值    ：{np.min(GBDT_results_BET_ECFP):f}', flush=True)
#     print(f'{ii}-th GBDT_AE_BET_ECFP的BA值    ：{np.min(GBDT_results_AE_BET_ECFP):f}', flush=True)



# t_end = time.time()
# print('total time:', (t_end - t_start) / 3600, 'h', flush=True)
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import KFold
from sklearn.preprocessing import StandardScaler
import numpy as np
import scipy.stats
import argparse, sys, os, time, csv

os.environ['MKL_THREADING_LAYER'] = 'GNU'
os.environ['MKL_SERVICE_FORCE_INTEL'] = '1'

t_start = time.time()

# ====================== 工具函数 ======================
def normalize(X):
    scaler = StandardScaler().fit(X)
    return scaler.transform(X)

def csv_to_npy(filename):
    nlist = []
    with open(filename, encoding='utf-8-sig') as f:
        for row in csv.reader(f, skipinitialspace=True):
            if len(row) == 0:
                continue
            if 'cddd_1' in row:
                continue
            row_list = []
            for i in row[2:]:
                row_list.append(float(i))
            nlist.append(row_list)
    return np.array(nlist)

# ====================== 数据路径 ======================
model = sys.argv[1]

base_dir = '/share/home/u2415173011/Aldisease/TOP25_CHEMBL'

output_dir = \
'/share/home/u2415173011/Aldisease/TOP25_CHEMBL/MLmodels/new'

os.makedirs(output_dir, exist_ok=True)

path_smi = f'{base_dir}/AE/{model}/'
path_label = f'{base_dir}/AE/{model}/'
path_BET_npy = f'{base_dir}/BET/'
path_AE_npy = f'{base_dir}/AE/{model}/'

# ✅ 关键修复
path_ECFP_npy = f'{base_dir}/ECFP/{model}/'

# ====================== 读取数据 ======================
file = open(path_smi + f'{model}.smi', 'r')
data = np.array([line for line in file.readlines()])
print('size of data:', np.shape(data), flush=True)

y_val_ori = open(path_label + f'label_{model}.csv', 'r')
y_val = np.array([eval(i.strip()) for i in y_val_ori.readlines()])

# ====================== 参数设置 ======================
train_size = int(len(data) * 0.8)

if train_size < 1000:
    max_depth, min_samples_split = 7, 3
    subsample = 0.7
elif train_size < 5000:
    max_depth, min_samples_split = 8, 4
    subsample = 0.5
else:
    max_depth, min_samples_split = 9, 7
    subsample = 0.3

parser = argparse.ArgumentParser()
parser.add_argument('--n_estimators', default=10000, type=int)
parser.add_argument('--learning_rate', default=0.01, type=float)
parser.add_argument('--max_features', default='sqrt')
parser.add_argument('--random_seed', default=0, type=int)

args = parser.parse_known_args()[0]

print('GBDT parameter:', args, flush=True)

# ====================== 结果初始化 ======================
GBDT_results_AE = np.zeros(y_val.shape)
GBDT_results_BET = np.zeros(y_val.shape)
GBDT_results_ECFP = np.zeros(y_val.shape)
GBDT_results_AE_BET = np.zeros(y_val.shape)
GBDT_results_AE_ECFP = np.zeros(y_val.shape)
GBDT_results_BET_ECFP = np.zeros(y_val.shape)
GBDT_results_AE_BET_ECFP = np.zeros(y_val.shape)

# ====================== 十折交叉验证 ======================
kf = KFold(n_splits=10, shuffle=True, random_state=0)
fold = 0

for train_idx, test_idx in kf.split(data):
    fold += 1
    print('fold=', fold, flush=True)

    # ===== BET =====
    X_train_BET = np.concatenate((
        np.load(path_BET_npy + f'{model}_train_BET_{fold}.npy', allow_pickle=True),
        np.load(path_BET_npy + f'{model}_valid_BET_{fold}.npy', allow_pickle=True)
    ))
    X_test_BET = np.load(path_BET_npy + f'{model}_test_BET_{fold}.npy', allow_pickle=True)

    X_train_BET = normalize(X_train_BET)
    X_test_BET = normalize(X_test_BET)

    # ===== 标签 =====
    y_train = np.concatenate((
        [float(i.strip()) for i in open(path_smi + f'{model}_regression_train_{fold}.label')],
        [float(i.strip()) for i in open(path_smi + f'{model}_regression_valid_{fold}.label')]
    ))
    y_test = np.array([float(i.strip()) for i in open(path_smi + f'{model}_regression_test_{fold}.label')])

    # ===== AE =====
    X_train_AE = np.concatenate((
        csv_to_npy(path_AE_npy + f'{model}_train_AE_{fold}.csv'),
        csv_to_npy(path_AE_npy + f'{model}_valid_AE_{fold}.csv')
    ))
    X_test_AE = csv_to_npy(path_AE_npy + f'{model}_test_AE_{fold}.csv')

    X_train_AE = normalize(X_train_AE)
    X_test_AE = normalize(X_test_AE)

    # ===== ECFP（关键修复路径）=====
    X_train_ECFP = np.concatenate((
        np.load(path_ECFP_npy + f'{model}_train_ECFP_{fold}.npy', allow_pickle=True),
        np.load(path_ECFP_npy + f'{model}_valid_ECFP_{fold}.npy', allow_pickle=True)
    ))
    X_test_ECFP = np.load(path_ECFP_npy + f'{model}_test_ECFP_{fold}.npy', allow_pickle=True)

    X_train_ECFP = normalize(X_train_ECFP)
    X_test_ECFP = normalize(X_test_ECFP)

    # ===== Feature Fusion =====

    X_train_AE_BET = np.hstack((X_train_AE, X_train_BET))
    X_test_AE_BET = np.hstack((X_test_AE, X_test_BET))

    X_train_AE_ECFP = np.hstack((X_train_AE, X_train_ECFP))
    X_test_AE_ECFP = np.hstack((X_test_AE, X_test_ECFP))

    X_train_BET_ECFP = np.hstack((X_train_BET, X_train_ECFP))
    X_test_BET_ECFP = np.hstack((X_test_BET, X_test_ECFP))

    X_train_AE_BET_ECFP = np.hstack(
        (X_train_AE,
        X_train_BET,
        X_train_ECFP)
    )

    X_test_AE_BET_ECFP = np.hstack(
        (X_test_AE,
        X_test_BET,
        X_test_ECFP)
    )

    # ====================== 模型 ======================
    GBR = GradientBoostingRegressor(
        n_estimators=args.n_estimators,
        learning_rate=args.learning_rate,
        max_depth=max_depth,
        min_samples_split=min_samples_split,
        subsample=subsample,
        random_state=args.random_seed
    )

    # ===== BET =====
    GBR.fit(X_train_BET, y_train)
    GBDT_results_BET[test_idx] = GBR.predict(X_test_BET)

    # ===== AE =====
    GBR.fit(X_train_AE, y_train)
    GBDT_results_AE[test_idx] = GBR.predict(X_test_AE)

    # ===== ECFP =====
    GBR.fit(X_train_ECFP, y_train)
    GBDT_results_ECFP[test_idx] = GBR.predict(X_test_ECFP)

    # ===== AE+BET =====
    GBR.fit(X_train_AE_BET, y_train)
    GBDT_results_AE_BET[test_idx] = GBR.predict(X_test_AE_BET)

    # ===== AE+ECFP =====
    GBR.fit(X_train_AE_ECFP, y_train)
    GBDT_results_AE_ECFP[test_idx] = GBR.predict(X_test_AE_ECFP)

    # ===== BET+ECFP =====
    GBR.fit(X_train_BET_ECFP, y_train)
    GBDT_results_BET_ECFP[test_idx] = GBR.predict(X_test_BET_ECFP)

    # ===== AE+BET+ECFP =====
    GBR.fit(X_train_AE_BET_ECFP, y_train)
    GBDT_results_AE_BET_ECFP[test_idx] = GBR.predict(
        X_test_AE_BET_ECFP
    )

# ====================== 最终结果 ======================
print('\n========== FINAL RESULT ==========', flush=True)

def report(name, y_true, y_pred):
    rmsd = np.sqrt(mean_squared_error(y_true, y_pred))
    p = scipy.stats.pearsonr(y_true, y_pred)[0]
    r2 = r2_score(y_true, y_pred)
    print(f'{name} -> RMSD: {rmsd:.4f}, P: {p:.4f}, R2: {r2:.4f}', flush=True)

report('GBDT_BET', y_val, GBDT_results_BET)
report('GBDT_AE', y_val, GBDT_results_AE)
report('GBDT_ECFP', y_val, GBDT_results_ECFP)

report('GBDT_AE_BET', y_val, GBDT_results_AE_BET)
report('GBDT_AE_ECFP', y_val, GBDT_results_AE_ECFP)
report('GBDT_BET_ECFP', y_val, GBDT_results_BET_ECFP)

report(
    'GBDT_AE_BET_ECFP',
    y_val,
    GBDT_results_AE_BET_ECFP
)

# ====================== 保存结果 ======================
# ====================== 保存结果 ======================

output_dir = '/share/home/u2415173011/Aldisease/TOP25_CHEMBL/MLmodels/new'
os.makedirs(output_dir, exist_ok=True)

np.save(
    os.path.join(output_dir,
                 f'{model}_GBDT_BET.npy'),
    GBDT_results_BET
)

np.save(
    os.path.join(output_dir,
                 f'{model}_GBDT_AE.npy'),
    GBDT_results_AE
)

np.save(
    os.path.join(output_dir,
                 f'{model}_GBDT_ECFP.npy'),
    GBDT_results_ECFP
)

np.save(
    os.path.join(output_dir,
                 f'{model}_GBDT_AE_BET.npy'),
    GBDT_results_AE_BET
)

np.save(
    os.path.join(output_dir,
                 f'{model}_GBDT_AE_ECFP.npy'),
    GBDT_results_AE_ECFP
)

np.save(
    os.path.join(output_dir,
                 f'{model}_GBDT_BET_ECFP.npy'),
    GBDT_results_BET_ECFP
)

np.save(
    os.path.join(output_dir,
                 f'{model}_GBDT_AE_BET_ECFP.npy'),
    GBDT_results_AE_BET_ECFP
)

t_end = time.time()
print('total time:', (t_end - t_start) / 3600, 'h', flush=True)