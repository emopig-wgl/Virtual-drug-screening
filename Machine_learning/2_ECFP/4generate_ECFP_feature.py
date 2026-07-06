# import os

# import pandas as pd
# import numpy as np
# import math
# from rdkit import Chem as ch
# from rdkit import rdBase, Chem, DataStructs
# from rdkit.Avalon import pyAvalonTools
# from rdkit.Chem import AllChem, Draw
# import multiprocessing
# import time
# import sys

# os.system('export MKL_THREADING_LAYER=GNU')
# t_start = time.time()

# def Morgan(smi):
#     mol = Chem.MolFromSmiles(smi)
#     fp = AllChem.GetMorganFingerprintAsBitVect(mol, 2, 2048)
#     return list(fp)


# if __name__ == "__main__":
#     name = sys.argv[1]  # Get target from command line

#     lines = open(f'/share/home/u2415173011/ML/TOP300_CHEMBL/{name}/{name}.smi', 'r').readlines()
#     mols = [line.strip() for line in lines]
#     pool = multiprocessing.Pool(48)
#     re = pool.starmap(Morgan, zip(mols))
#     pool.close()
#     pool.join()
#     np.save(f'/share/home/u2415173011/ML/TOP300_CHEMBL/ECFP/{name}_ECFP.npy', np.array(re))

# #os.system(cmd)
# t_end = time.time()
# print('total time:',(t_end-t_start)/3600,'h',flush=True)


import os
import pandas as pd
import numpy as np
import math
from rdkit import Chem as ch
from rdkit import rdBase, Chem, DataStructs
from rdkit.Avalon import pyAvalonTools
from rdkit.Chem import AllChem, Draw
import multiprocessing
import time
import sys

# 防止 MKL 冲突
os.system('export MKL_THREADING_LAYER=GNU')
t_start = time.time()


def Morgan(smi):
    mol = Chem.MolFromSmiles(smi)
    fp = AllChem.GetMorganFingerprintAsBitVect(mol, 2, 2048)
    return list(fp)


if __name__ == "__main__":
    # 从命令行读取目标名称
    name = sys.argv[1]

    # SMILES 文件路径
    smi_path = f'/share/home/u2415173011/Aldisease/TOP25_CHEMBL/ECFP/{name}/{name}.smi'
    # 输出路径
    save_path = f'/share/home/u2415173011/Aldisease/TOP25_CHEMBL/ECFP/{name}/{name}_ECFP.npy'

    # 读取 SMILES
    lines = open(smi_path, 'r').readlines()
    mols = [line.strip() for line in lines]

    # 多进程计算指纹
    pool = multiprocessing.Pool(48)
    re = pool.starmap(Morgan, zip(mols))
    pool.close()
    pool.join()

    # 保存为 numpy 文件
    np.save(save_path, np.array(re))

    t_end = time.time()
    print('total time:', (t_end - t_start) / 3600, 'h', flush=True)
