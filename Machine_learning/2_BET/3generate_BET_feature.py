# import os
# import time
# import sys

# os.system('export MKL_THREADING_LAYER=GNU')
# t_start = time.time()

# name = sys.argv[1]

# cmd='python "/public/home/chenlong666/desktop/PretrainModels/bt_pro/generate_bt_fps.py" --model_name_or_path "/public/home/chenlong666/desktop/PretrainModels/examples/models/"  --checkpoint_file "/public/home/chenlong666/desktop/PretrainModels/checkpoint_best.pt" --data_name_or_path  "/public/home/chenlong666/desktop/PretrainModels/examples/models/" --dict_file "/public/home/chenlong666/desktop/PretrainModels/examples/models/dict.txt" --target_file "/public/home/chenlong666/Chunhuanzhang/top300_chembl/{}/{}.smi" --save_feature_path "/public/home/chenlong666/Chunhuanzhang/BET/{}_BET.npy"'.format(name, name, name)
# os.system(cmd)
# t_end = time.time()
# print('total time:',(t_end-t_start)/3600,'h',flush=True)

import os
import time
import sys

# 保证 MKL 库在 HPC 环境下能正常工作
os.system('export MKL_THREADING_LAYER=GNU')

# 注册自定义的 smi 分词器
sys.path.append('/share/home/u2415173011/Aldisease/TOP25_CHEMBL/BET')
import register_smi_bpe

t_start = time.time()

name = sys.argv[1]

cmd = (
    '/share/home/u2415173011/.conda/envs/bet/bin/python '
    '"/share/home/u2415173011/Aldisease/TOP25_CHEMBL/BET/generate_bt_fps.py" '
    '--model_name_or_path "/share/home/u2415173011/Aldisease/TOP25_CHEMBL/BET" '
    '--checkpoint_file "/share/home/u2415173011/Aldisease/TOP25_CHEMBL/BET/checkpoint_best.pt" '
    '--data_name_or_path "/share/home/u2415173011/Aldisease/TOP25_CHEMBL/BET/" '
    '--dict_file "/share/home/u2415173011/Aldisease/TOP25_CHEMBL/BET/dict.txt" '
    '--target_file "/share/home/u2415173011/Aldisease/TOP25_CHEMBL/BET/{}/{}.smi" '
    '--save_feature_path "/share/home/u2415173011/Aldisease/TOP25_CHEMBL/BET/{}/{}_BET.npy"'
).format(name, name, name, name)

os.system(cmd)

t_end = time.time()
print('total time:', (t_end - t_start) / 3600, 'h', flush=True)




# import sys
# import os
# import pandas as pd
# import torch

# if len(sys.argv) < 2:
#     print("Usage: python 3generate_BET_feature.py CHEMBLxxx")
#     sys.exit(1)

# chembl_id = sys.argv[1]

# # 基础目录
# base_dir = "/share/home/u2415173011/ML/TOP300_CHEMBL"
# chembl_dir = os.path.join(base_dir, chembl_id)

# # 输入和输出
# input_file = os.path.join(chembl_dir, f"{chembl_id}.smi")
# output_file = os.path.join(chembl_dir, f"{chembl_id}_BET.csv")

# # 模型路径（需要你手动下载后放到这里）
# model_dir = os.path.join(base_dir, "bet_model")

# # 检查输入文件
# if not os.path.exists(input_file):
#     print(f"ERROR: {input_file} not found.")
#     sys.exit(1)

# # 读取 smiles
# smiles_list = []
# with open(input_file, "r") as f:
#     for line in f:
#         smiles_list.append(line.strip())

# print(f"Loaded {len(smiles_list)} molecules from {input_file}")

# # 这里加载模型 (示例，实际你要替换成真实加载逻辑)
# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# print(f"Using device: {device}")
# # model = torch.load(os.path.join(model_dir, "checkpoint_best.pt"), map_location=device)

# # 生成特征 (这里只是示例，用 smiles 长度代替)
# features = [{"smiles": smi, "bet_feature": len(smi)} for smi in smiles_list]

# # 保存结果
# df = pd.DataFrame(features)
# # 保存为 csv
# df.to_csv(output_file, index=False)
# print(f"Saved results to {output_file}")

# # 另存为 npy
# import numpy as np
# npy_output_file = output_file.replace(".csv", ".npy")
# np.save(npy_output_file, features)   # features 是你生成的 512 维向量的数组
# print(f"Saved numpy array to {npy_output_file}")

