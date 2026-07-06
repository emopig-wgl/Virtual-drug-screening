# #!/usr/bin/python
# #!/bin/bash
# import numpy as np
# from numpy import arange
# import os
# import math
# import numpy



# CHEMBL_dataset = ['CHEMBL216','CHEMBL1801','CHEMBL1836','CHEMBL1856','CHEMBL1995','CHEMBL2047','CHEMBL2068','CHEMBL2073','CHEMBL2083','CHEMBL2085', 'CHEMBL2107',
# 			'CHEMBL2147', 'CHEMBL2319', 'CHEMBL2434', 'CHEMBL2525', 'CHEMBL2593', 'CHEMBL2717' , 'CHEMBL2730' , 'CHEMBL2778' ,'CHEMBL2789' , 'CHEMBL2889' , 'CHEMBL2959', 'CHEMBL3018',
# 			'CHEMBL3060' , 'CHEMBL3100', 'CHEMBL3106', 'CHEMBL3119' , 'CHEMBL3194', 'CHEMBL3286', 'CHEMBL3359' ,'CHEMBL3401', 'CHEMBL3475' , 'CHEMBL3544' , 'CHEMBL3572',
# 			'CHEMBL3650','CHEMBL3785', 'CHEMBL3869', 'CHEMBL4029', 'CHEMBL4073', 'CHEMBL4076', 'CHEMBL4223', 'CHEMBL4306', 'CHEMBL4394', 'CHEMBL4409', 'CHEMBL4427', 'CHEMBL4462',
# 			'CHEMBL4506', 'CHEMBL4507', 'CHEMBL4607', 'CHEMBL4616', 'CHEMBL4691', 'CHEMBL4767', 'CHEMBL4789', 'CHEMBL4835', 'CHEMBL5247', 'CHEMBL5314', 'CHEMBL5319', 'CHEMBL5378',
# 			'CHEMBL5398', 'CHEMBL5480', 'CHEMBL5493', 'CHEMBL5918', 'CHEMBL6003', 'CHEMBL6007', 'CHEMBL1250348', 'CHEMBL1293255', 'CHEMBL1293293', 'CHEMBL1741179', 'CHEMBL1741186', 
# 			'CHEMBL1741200', 'CHEMBL1741213', 'CHEMBL2424504', 'CHEMBL3392948', 'CHEMBL3714079', 'CHEMBL3989381', 'CHEMBL4105860'
#                   ]

# #####for i in range(len(CHEMBL_dataset)):
# for i in range(len(CHEMBL_dataset)):
#     target_ID_input = CHEMBL_dataset[i]
#     feature_ID = 'smi'
#     f = open('%s_%s.pbs'%(target_ID_input,feature_ID), 'w')
#     f.write('#!/bin/bash\n')
#     f.write('#PBS -q batch\n')
#     f.write('########## Define Resources Needed with PBS Lines ##########\n')
#     f.write('#PBS -l nodes=node05:ppn=1\n')
#     f.write('#PBS -l mem=2gb\n')
#     f.write('#PBS -o %s_%s.out\n'%(target_ID_input,feature_ID))
#     f.write('#PBS -e %s_%s.err\n'%(target_ID_input,feature_ID))
#     #f.write('cd /public/home/chenlong666/Chunhuanzhang/top300_chembl')
#     #f.write('\n')
#     #f.write('source /etc/profile\n')
#     #f.write('module load python/conda/3.6\n')
#     #f.write('source /public/home/chenlong666/anaconda3/bin/activate pre-gpu\n')
#     f.write('python get-smi-labels.py %s' % (target_ID_input))
#     f.close()
#     cmd = 'qsub %s_%s.pbs'%(target_ID_input,feature_ID)
#     os.system(cmd)

#!/usr/bin/env python3


import os
import subprocess
import sys
from pathlib import Path

# 假设 get-smi-labels.py 和 multi_job.py 在同一目录下
SCRIPT_PATH = Path(__file__).parent / "1get-smi-labels.py"
# 您的CHEMBL数据集列表
CHEMBL_dataset = [
    'CHEMBL216', 'CHEMBL1801', 'CHEMBL1836', 'CHEMBL1856', 'CHEMBL1995', 'CHEMBL2047', 'CHEMBL2068',
    'CHEMBL2073', 'CHEMBL2083', 'CHEMBL2085', 'CHEMBL2107', 'CHEMBL2147', 'CHEMBL2319', 'CHEMBL2434',
    'CHEMBL2525', 'CHEMBL2593', 'CHEMBL2717', 'CHEMBL2730', 'CHEMBL2778', 'CHEMBL2789', 'CHEMBL2889',
    'CHEMBL2959', 'CHEMBL3018', 'CHEMBL3060', 'CHEMBL3100', 'CHEMBL3106', 'CHEMBL3119', 'CHEMBL3194',
    'CHEMBL3286', 'CHEMBL3359', 'CHEMBL3401', 'CHEMBL3475', 'CHEMBL3544', 'CHEMBL3572', 'CHEMBL3650',
    'CHEMBL3785', 'CHEMBL3869', 'CHEMBL4029', 'CHEMBL4073', 'CHEMBL4076', 'CHEMBL4223', 'CHEMBL4306',
    'CHEMBL4394', 'CHEMBL4409', 'CHEMBL4427', 'CHEMBL4462', 'CHEMBL4506', 'CHEMBL4507', 'CHEMBL4607',
    'CHEMBL4616', 'CHEMBL4691', 'CHEMBL4767', 'CHEMBL4789', 'CHEMBL4835', 'CHEMBL5247', 'CHEMBL5314',
    'CHEMBL5319', 'CHEMBL5378', 'CHEMBL5398', 'CHEMBL5480', 'CHEMBL5493', 'CHEMBL5918', 'CHEMBL6003',
    'CHEMBL6007', 'CHEMBL1250348', 'CHEMBL1293255', 'CHEMBL1293293', 'CHEMBL1741179', 'CHEMBL1741186',
    'CHEMBL1741200', 'CHEMBL1741213', 'CHEMBL2424504', 'CHEMBL3392948', 'CHEMBL3714079', 'CHEMBL3989381',
    'CHEMBL4105860'
]

# CHEMBL_dataset = [
#     'CHEMBL1801'
# ]

def run_script_for_dataset(chembl_id):
    """为单个CHEMBL数据集运行处理脚本"""
    try:
        # 构建命令：python get-smi-labels.py CHEMBL_ID
        cmd = [sys.executable, str(SCRIPT_PATH), chembl_id]
        print(f"[INFO] 开始处理: {chembl_id}")
        print(f"[CMD] {' '.join(cmd)}")
        
        # 运行命令，并捕获输出
        result = subprocess.run(cmd, capture_output=True, text=True, check=True, cwd=Path(__file__).parent)
        
        # 打印标准输出和错误（如果有的话）
        if result.stdout:
            print(f"[STDOUT] {result.stdout}")
        if result.stderr:
            print(f"[STDERR] {result.stderr}")
            
        print(f"[SUCCESS] 完成: {chembl_id}\n")
        return True
        
    except subprocess.CalledProcessError as e:
        # 如果脚本返回非零退出码，表示执行出错
        print(f"[ERROR] 处理 {chembl_id} 时出错 (退出码: {e.returncode}):")
        print(f"[STDERR] {e.stderr}")
        if e.stdout:
            print(f"[STDOUT] {e.stdout}")
        print()
        return False
    except FileNotFoundError:
        print(f"[ERROR] 脚本文件未找到: {SCRIPT_PATH}. 请确保 get-smi-labels.py 与本脚本在同一目录下。")
        return False
    except Exception as e:
        print(f"[ERROR] 处理 {chembl_id} 时发生未知错误: {e}")
        return False

def main():
    """主函数：遍历所有CHEMBL数据集并处理"""
    print("=" * 50)
    print("开始批量处理 CHEMBL 数据集")
    print("=" * 50)
    
    success_count = 0
    fail_count = 0
    failed_ids = []
    
    # 检查脚本是否存在
    if not SCRIPT_PATH.exists():
        print(f"[FATAL ERROR] 找不到处理脚本: {SCRIPT_PATH}")
        print("请确保 get-smi-labels.py 与 multi_job.py 位于同一目录下。")
        return
    
    # 遍历所有CHEMBL ID并处理
    for chembl_id in CHEMBL_dataset:
        success = run_script_for_dataset(chembl_id)
        if success:
            success_count += 1
        else:
            fail_count += 1
            failed_ids.append(chembl_id)
    
    # 输出总结报告
    print("=" * 50)
    print("处理完成！")
    print("=" * 50)
    print(f"成功: {success_count}")
    print(f"失败: {fail_count}")
    
    if failed_ids:
        print("失败的数据集ID:")
        for fid in failed_ids:
            print(f"  - {fid}")
    else:
        print("所有数据集均已成功处理！")

if __name__ == "__main__":
    main()