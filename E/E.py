import pandas as pd
import os

# 指定 Excel 檔案的完整路徑
a_excel_file = r"C:\Users\31628\Desktop\A.xlsx"
b_excel_file = r"C:\Users\31628\Desktop\B.xlsx"

# 測試檔案是否存在
if not os.path.exists(a_excel_file):
    raise FileNotFoundError(f"檔案 {a_excel_file} 不存在，請確認路徑！")
if not os.path.exists(b_excel_file):
    raise FileNotFoundError(f"檔案 {b_excel_file} 不存在，請確認路徑！")

# 讀取 Excel 檔案中的所有 Sheet
a_sheets = pd.read_excel(a_excel_file, sheet_name=None)  # A 檔案所有 Sheet
b_sheets = pd.read_excel(b_excel_file, sheet_name=None)  # B 檔案所有 Sheet

# 儲存結果
results = []

# 遍歷 A 和 B 檔案的 Sheet
for a_sheet_name, a_df in a_sheets.items():
    for b_sheet_name, b_df in b_sheets.items():
        # 確保需要的欄位存在
        if 'D' not in a_df.columns or 'C' not in b_df.columns or 'F' not in b_df.columns or 'G' not in b_df.columns:
            print(f"跳過比對：A 的 {a_sheet_name} 或 B 的 {b_sheet_name} 缺少必要欄位！")
            continue
        
        # 跳過含有空值的資料
        a_df = a_df.dropna(subset=['D'])  # 移除 A 的 D 欄有空值的行
        b_df = b_df.dropna(subset=['C', 'F', 'G'])  # 移除 B 的 C、F、G 欄有空值的行

        # 比對條件：A 的 D 欄與 B 的 C 欄
        a_df['Match_Found'] = a_df['D'].isin(b_df['C'])

        # 核對 F 和 G 欄是否皆不低於 80
        a_df['Valid_F_G'] = a_df['D'].apply(
            lambda x: all((b_df.loc[b_df['C'] == x, ['F', 'G']] >= 80).all(axis=1)) if x in b_df['C'].values else False
        )

        # 篩選出未通過的記錄
        invalid_records = a_df[~(a_df['Match_Found'] & a_df['Valid_F_G'])]

        # 添加 Sheet 資訊到結果
        if not invalid_records.empty:
            invalid_records['A_Sheet'] = a_sheet_name
            invalid_records['B_Sheet'] = b_sheet_name
            results.append(invalid_records)

# 匯出結果
if results:
    final_result = pd.concat(results)
    output_file = r"C:\Users\31628\Desktop\Mismatch_Report.xlsx"
    final_result.to_excel(output_file, index=False)
    print(f"比對完成！問題報告已儲存為 {output_file}")
else:
    print("所有資料均符合條件！")
