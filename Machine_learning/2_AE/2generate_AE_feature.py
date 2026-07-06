# import os
# import time
# import sys

# os.system('export MKL_THREADING_LAYER=GNU')
# t_start = time.time()

# name = sys.argv[1]
# cmd='cddd --input /public/home/chenlong666/Chunhuanzhang/AE/{}/{}.smi --out /public/home/chenlong666/Chunhuanzhang/AE/{}_AE.csv --smiles_header smiles --no-preprocess'.format(name, name, name)
# os.system(cmd)
# t_end = time.time()
# print('total time:',(t_end-t_start)/3600,'h',flush=True)

# import os
# import time
# import sys

# t_start = time.time()
# name = sys.argv[1]

# base_dir = "/share/home/u2415173011/Aldisease/TOP25_CHEMBL/AE"
# smi_file = f"{base_dir}/{name}/{name}.smi"
# out_file = f"{base_dir}/{name}/{name}_AE.csv"

# # 直接在 shell 命令里设置环境变量
# # cmd = f"CDDD_MODEL_DIR=/share/home/u2415173011/.local/share/cddd/default_model cddd --input {smi_file} --out {out_file} --smiles_header smiles --no-preprocess"
# cmd='cddd --input /share/home/u2415173011/Aldisease/TOP25_CHEMBL/AE/{}/{}.smi --out /share/home/u2415173011/Aldisease/TOP25_CHEMBL/AE/{}/{}_AE.csv --smiles_header smiles --no-preprocess'.format(name, name, name)
# # os.system(cmd)
# import subprocess
# subprocess.run(cmd, shell=True)

# t_end = time.time()
# print("total time:", (t_end - t_start) / 3600, "h", flush=True)




#通用版本从这里开始

# import os
# import time
# import sys

# t_start = time.time()
# name = sys.argv[1]

# base_dir = "/share/home/u2415173011/Aldisease/TOP25_CHEMBL/AE"
# smi_file = f"{base_dir}/{name}/{name}.smi"
# out_file = f"{base_dir}/{name}/{name}_AE.csv"

# cmd = f"cddd --input {smi_file} --out {out_file}"
# os.system(cmd)

# t_end = time.time()
# print("total time:", (t_end - t_start) / 3600, "h", flush=True)
import os
import time
import sys
from rdkit import Chem
import pandas as pd
import numpy as np

t_start = time.time()
name = sys.argv[1]

base_dir = "/share/home/u2415173011/Aldisease/TOP25_CHEMBL/AE"
smi_file = f"{base_dir}/{name}/{name}.smi"
clean_smi_file = f"{base_dir}/{name}/{name}_clean.smi"
out_file = f"{base_dir}/{name}/{name}_AE.csv"

# ✅ Step 1: 记录 valid_idx（关键！）
valid_smiles = []
valid_idx = []

with open(smi_file, 'r') as f:
    for idx, line in enumerate(f):
        smi = line.strip().split()[0]
        mol = Chem.MolFromSmiles(smi)
        if mol is not None:
            valid_smiles.append(smi)
            valid_idx.append(idx)

# 保存 clean smi
with open(clean_smi_file, 'w') as f:
    for smi in valid_smiles:
        f.write(smi + '\n')

print("原始分子数:", sum(1 for _ in open(smi_file)))
print("有效分子数:", len(valid_smiles))

# ✅ Step 2: 跑 CDDD
cmd = f"cddd --input {clean_smi_file} --out {out_file}"
os.system(cmd)

# ✅ Step 3: 删除 embedding 失败行
df = pd.read_csv(out_file)
df_clean = df.dropna()

# ⚠️ 关键：同步裁剪 valid_idx
valid_idx = np.array(valid_idx)
valid_idx = valid_idx[df.dropna().index]

# 保存
df_clean.to_csv(out_file, index=False)
np.save(f"{base_dir}/{name}/{name}_valid_idx.npy", valid_idx)

print("最终有效分子数:", len(valid_idx))

t_end = time.time()
print("total time:", (t_end - t_start) / 3600, "h", flush=True)