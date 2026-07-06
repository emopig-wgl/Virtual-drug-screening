import pandas as pd
import os

# 📂 你的文件夹路径
folder_path = r"C:\Users\lenovo\Desktop\文章4\TOP25_CHEMBL\filter_BA"

# 📌 用来存所有筛选结果
all_results = []

# 🔁 遍历所有 CSV 文件
for file in os.listdir(folder_path):
    if file.endswith(".csv"):
        file_path = os.path.join(folder_path, file)
        
        print(f"正在处理: {file}")
        
        df = pd.read_csv(file_path)

        # ✅ 检查必要列（防止报错）
        if "BA_pred" not in df.columns or "FDA Approved" not in df.columns:
            print(f"⚠️ 跳过 {file}（缺少必要列）")
            continue

        # ✅ 筛选条件
        df_filtered = df[
            (df["BA_pred"] < -9.54) &
            (df["FDA Approved"].isin(["approved", "investigational"]))
        ].copy()

        # ✅ 记录来源数据集（非常有用）
        df_filtered["source_file"] = file

        all_results.append(df_filtered)

# ✅ 合并所有结果
if len(all_results) > 0:
    final_df = pd.concat(all_results, ignore_index=True)
else:
    final_df = pd.DataFrame()

# 📄 输出 Excel 文件
output_path = os.path.join(folder_path, "BA_prediction_results(approved+investigational).xlsx")
final_df.to_excel(output_path, index=False)

print("\n✅ 筛选完成！")
print("总筛选分子数:", len(final_df))
print("结果已保存到:", output_path)