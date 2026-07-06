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
# 			'CHEMBL1741200', 'CHEMBL1741213', 'CHEMBL2424504', 'CHEMBL3392948', 'CHEMBL3714079', 'CHEMBL3989381', 'CHEMBL4105860']
# #import os
# #import numpy as np

# for i in range(len(CHEMBL_dataset)):
#     target_ID_input = CHEMBL_dataset[i]
#     feature_ID = 'ECFP'
#     f = open(f'{target_ID_input}_{feature_ID}.pbs', 'w')
#     f.write('#!/bin/bash\n')
#     f.write('#PBS -q batch\n')
#     f.write('########## Define Resources Needed with PBS Lines ##########\n')
#     f.write('#PBS -l walltime=10000:00:00\n')
#     f.write('#PBS -l nodes=node05:ppn=1\n')  # Using 48 cores as in your pool
#     f.write('#PBS -l mem=2gb\n')  # Increased memory for parallel processing
#     f.write('#PBS -o %s_%s.out\n' % (target_ID_input, feature_ID))
#     f.write('#PBS -e %s_%s.err\n' % (target_ID_input, feature_ID))
#     #f.write('cd /mnt/ufs18/rs-045/guowei-search.5/HongyanDu/\n')  # Adjust to your working directory
#     f.write('cd /public/home/chenlong666/Chunhuanzhang/ECFP')
#     f.write('\n')
#     # f.write('source /mnt/ufs18/rs-045/guowei-search.5/HongyanDu/miniconda3/bin/activate\n')
#     # f.write('conda activate /mnt/ufs18/rs-045/guowei-search.5/HongyanDu/miniconda3/envs/cddd/\n')
#     f.write('source /public/home/chenlong666/anaconda3/bin/activate cddd\n')
#     f.write('python generate_ECFP_feature.py %s\n' % target_ID_input)  # Assuming you'll save the code to this file
#     f.close()
#     cmd = 'qsub %s_%s.pbs' % (target_ID_input, feature_ID)
#     os.system(cmd)

#!/usr/bin/env python3


# import os

# # 这里你可以手动修改 chembl_list，每次放 5 个数据集
# chembl_list = [
#     'CHEMBL216','CHEMBL1801','CHEMBL1836','CHEMBL1856','CHEMBL1995'
# ]

# submit_file = "submit_ecfp.sh"

# with open(submit_file, "w") as f:
#     f.write("#!/bin/bash\n")
#     f.write("#SBATCH --job-name=ecfp_job\n")
#     f.write("#SBATCH --output=ecfp_job.out\n")
#     f.write("#SBATCH --error=ecfp_job.err\n")
#     f.write("#SBATCH --time=72:00:00\n")
#     f.write("#SBATCH --partition=cpu\n")
#     f.write("#SBATCH --nodes=1\n")
#     f.write("#SBATCH --ntasks=1\n")
#     f.write("#SBATCH --cpus-per-task=48\n")
#     f.write("#SBATCH --mem=32G\n\n")
#     f.write("source ~/.bashrc\n")
#     f.write("conda activate ecfp\n\n")

#     for target in chembl_list:
#         f.write(f"echo Running: python /share/home/u2415173011/ML/TOP300_CHEMBL/4generate_ECFP_feature.py {target}\n")
#         f.write(f"python /share/home/u2415173011/ML/TOP300_CHEMBL/4generate_ECFP_feature.py {target}\n\n")

# print(f"Generated {submit_file}. Now you can run:")
# print("sbatch submit_ecfp.sh")


#!/usr/bin/python
#!/bin/bash
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
# 			'CHEMBL1741200', 'CHEMBL1741213', 'CHEMBL2424504', 'CHEMBL3392948', 'CHEMBL3714079', 'CHEMBL3989381', 'CHEMBL4105860']
# #import os
# #import numpy as np

# for i in range(len(CHEMBL_dataset)):
#     target_ID_input = CHEMBL_dataset[i]
#     feature_ID = 'ECFP'
#     f = open(f'{target_ID_input}_{feature_ID}.pbs', 'w')
#     f.write('#!/bin/bash\n')
#     f.write('#PBS -q batch\n')
#     f.write('########## Define Resources Needed with PBS Lines ##########\n')
#     f.write('#PBS -l walltime=10000:00:00\n')
#     f.write('#PBS -l nodes=node05:ppn=1\n')  # Using 48 cores as in your pool
#     f.write('#PBS -l mem=2gb\n')  # Increased memory for parallel processing
#     f.write('#PBS -o %s_%s.out\n' % (target_ID_input, feature_ID))
#     f.write('#PBS -e %s_%s.err\n' % (target_ID_input, feature_ID))
#     #f.write('cd /mnt/ufs18/rs-045/guowei-search.5/HongyanDu/\n')  # Adjust to your working directory
#     f.write('cd /public/home/chenlong666/Chunhuanzhang/ECFP')
#     f.write('\n')
#     # f.write('source /mnt/ufs18/rs-045/guowei-search.5/HongyanDu/miniconda3/bin/activate\n')
#     # f.write('conda activate /mnt/ufs18/rs-045/guowei-search.5/HongyanDu/miniconda3/envs/cddd/\n')
#     f.write('source /public/home/chenlong666/anaconda3/bin/activate cddd\n')
#     f.write('python generate_ECFP_feature.py %s\n' % target_ID_input)  # Assuming you'll save the code to this file
#     f.close()
#     cmd = 'qsub %s_%s.pbs' % (target_ID_input, feature_ID)
#     os.system(cmd)

import os
import time
import numpy as np

# =============================
# 数据集列表
# =============================
CHEMBL_dataset = [
    'CHEMBL4801','CHEMBL2157','CHEMBL1909490','CHEMBL1784','CHEMBL5141'
]

# =============================
# 循环生成并提交任务
# =============================
for i, target_ID_input in enumerate(CHEMBL_dataset):
    feature_ID = 'ECFP'
    pbs_name = f'{target_ID_input}_{feature_ID}.sh'

    # 生成单独的任务脚本
    with open(pbs_name, 'w') as f:
        f.write('#!/bin/bash\n')
        f.write('#SBATCH -J ECFP_JOB\n')
        f.write('#SBATCH -p cpu\n')
        f.write('#SBATCH -N 1\n')
        f.write('#SBATCH -n 1\n')
        f.write('#SBATCH --time=48:00:00\n')
        f.write('#SBATCH --mem=8G\n')
        f.write(f'#SBATCH -o {target_ID_input}_{feature_ID}.out\n')
        f.write(f'#SBATCH -e {target_ID_input}_{feature_ID}.err\n\n')

        # 切换到工作目录
        f.write('cd /share/home/u2415173011/Aldisease/TOP25_CHEMBL/ECFP/\n')

        # 调用 ECFP 环境运行 Python 脚本
        f.write(f'/share/home/u2415173011/.conda/envs/ecfp37/bin/python 4generate_ECFP_feature.py {target_ID_input}\n')

    # 提交作业
    os.system(f'sbatch {pbs_name}')
    print(f'已提交任务: {target_ID_input}_{feature_ID}')

    # 每提交10个任务暂停60秒，防止超出调度系统上限
    if (i + 1) % 10 == 0:
        print(f'\n🚦 已提交 {i + 1} 个任务，等待 60 秒以避免超出 QOS 限制...\n')
        time.sleep(60)

print("✅ 所有任务已生成并分批提交完成。")



