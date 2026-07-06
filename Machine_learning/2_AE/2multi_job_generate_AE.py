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
# 			'CHEMBL4507', 'CHEMBL4607', 'CHEMBL4616', 'CHEMBL4691', 'CHEMBL4767', 'CHEMBL4789', 'CHEMBL4835', 'CHEMBL5247', 'CHEMBL5314', 'CHEMBL5319', 'CHEMBL5378',
# 			'CHEMBL5398', 'CHEMBL5480', 'CHEMBL5493', 'CHEMBL5918', 'CHEMBL6003', 'CHEMBL6007', 'CHEMBL1250348', 'CHEMBL1293255', 'CHEMBL1293293', 'CHEMBL1741179', 'CHEMBL1741186', 
# 			'CHEMBL1741200', 'CHEMBL1741213', 'CHEMBL2424504', 'CHEMBL3392948', 'CHEMBL3714079']
# #####for i in range(len(CHEMBL_dataset)):
# for i in range(len(CHEMBL_dataset)):
#     target_ID_input = CHEMBL_dataset[i]
#     feature_ID = 'AE'
#     f = open('%s_%s.pbs'%(target_ID_input,feature_ID), 'w')
#     f.write('#!/bin/bash\n')
#     f.write('#PBS -q batch\n')
#     f.write('########## Define Resources Needed with PBS Lines ##########\n')
#     f.write('#PBS -l walltime=10000:00:00\n')
#     f.write('#PBS -l nodes=node05:ppn=1\n')
#     f.write('#PBS -l mem=2gb\n')
#     f.write('#PBS -o %s_%s.out\n'%(target_ID_input,feature_ID))
#     f.write('#PBS -e %s_%s.err\n'%(target_ID_input,feature_ID))
#     f.write('cd /public/home/chenlong666/Chunhuanzhang/AE')
#     f.write('\n')
#     #f.write('module load python/conda/3.6\n')
#     f.write('source /public/home/chenlong666/anaconda3/bin/activate cddd\n')
#     f.write('python generate_AE_feature.py %s' % (target_ID_input))
#     f.close()
#     cmd = 'qsub %s_%s.pbs'%(target_ID_input,feature_ID)
#     os.system(cmd)



# CHEMBL_dataset = [
#     'CHEMBL216','CHEMBL1801','CHEMBL1836','CHEMBL1856','CHEMBL1995','CHEMBL2047',
#     'CHEMBL2068','CHEMBL2073','CHEMBL2083','CHEMBL2085','CHEMBL2107','CHEMBL2147',
#     'CHEMBL2319','CHEMBL2434','CHEMBL2525','CHEMBL2593','CHEMBL2717','CHEMBL2730',
#     'CHEMBL2778','CHEMBL2789','CHEMBL2889','CHEMBL2959','CHEMBL3018','CHEMBL3060',
#     'CHEMBL3100','CHEMBL3106','CHEMBL3119','CHEMBL3194','CHEMBL3286','CHEMBL3359',
#     'CHEMBL3401','CHEMBL3475','CHEMBL3544','CHEMBL3572','CHEMBL3650','CHEMBL3785',
#     'CHEMBL3869','CHEMBL4029','CHEMBL4073','CHEMBL4076','CHEMBL4223','CHEMBL4306',
#     'CHEMBL4394','CHEMBL4409','CHEMBL4427','CHEMBL4462','CHEMBL4507','CHEMBL4607',
#     'CHEMBL4616','CHEMBL4691','CHEMBL4767','CHEMBL4789','CHEMBL4835','CHEMBL5247',
#     'CHEMBL5314','CHEMBL5319','CHEMBL5378','CHEMBL5398','CHEMBL5480','CHEMBL5493',
#     'CHEMBL5918','CHEMBL6003','CHEMBL6007','CHEMBL1250348','CHEMBL1293255',
#     'CHEMBL1293293','CHEMBL1741179','CHEMBL1741186','CHEMBL1741200','CHEMBL1741213',
#     'CHEMBL2424504','CHEMBL3392948','CHEMBL3714079'
# ]
import os

CHEMBL_dataset = [
    'CHEMBL4801','CHEMBL2157','CHEMBL1909490','CHEMBL1784','CHEMBL5141'
]

base_dir = "/share/home/u2415173011/Aldisease/TOP25_CHEMBL/AE"

for target_ID_input in CHEMBL_dataset:
    feature_ID = "AE"
    sh_file = f"{target_ID_input}_{feature_ID}.sh"

    with open(sh_file, "w") as f:
        f.write("#!/bin/bash\n")
        f.write(f"#SBATCH -J {target_ID_input}_{feature_ID}\n")
        f.write("#SBATCH -p cpu\n")
        f.write("#SBATCH -N 1\n")
        f.write("#SBATCH -n 1\n")
        f.write("#SBATCH --time=48:00:00\n")
        f.write("#SBATCH --mem=8G\n")
        f.write(f"#SBATCH -o {base_dir}/{target_ID_input}/{target_ID_input}_{feature_ID}.out\n")
        f.write(f"#SBATCH -e {base_dir}/{target_ID_input}/{target_ID_input}_{feature_ID}.err\n")
        f.write("\n")
        f.write("module load anaconda3/4.12.0\n")
        f.write("source activate cddd36\n")
    
        # ✅ 在这里添加本地模型环境变量
        f.write("export CDDD_MODEL_DIR=/share/home/u2415173011/.local/share/cddd/default_model\n")
    
        f.write(f"cd {base_dir}\n")
        f.write(f"python 2generate_AE_feature.py {target_ID_input}\n")


    os.system(f"sbatch {sh_file}")
