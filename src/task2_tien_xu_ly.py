"""
Task 2: Làm sạch và Tiền xử lý dữ liệu (Người thực hiện: Mai Đức Nhân)
Đồ án 1: Phân tích nhân khẩu học và dự đoán mức thu nhập cá nhân (US Adult Census)
Nhóm: 1_2 - Lớp: DHKL18A1HN
"""

import os
import sys
import numpy as np
import pandas as pd

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = r"D:\Đồ án 1"
RAW_DATA_PATH = os.path.join(BASE_DIR, "data", "adult_raw.csv")
CLEANED_DATA_PATH = os.path.join(BASE_DIR, "data", "adult_cleaned.csv")
REPORT_PATH = os.path.join(BASE_DIR, "reports", "task2_cleaning_summary.txt")


def clean_and_preprocess():
    print("=" * 60)
    print("TASK 2: LÀM SẠCH VÀ TIỀN XỬ LÝ DỮ LIỆU")
    print("Người thực hiện: Mai Đức Nhân")
    print("=" * 60)

    df = pd.read_csv(RAW_DATA_PATH)
    initial_rows, initial_cols = df.shape
    print(f"\n[+] Kích thước ban đầu: {initial_rows} dòng, {initial_cols} cột")

    # 1. Chuẩn hóa tên cột (đổi dấu '.' thành '_' cho chuẩn quy ước Python/R)
    df.columns = [c.strip().replace('.', '_').lower() for c in df.columns]
    print(f"[+] Danh sách cột sau chuẩn hóa tên: {list(df.columns)}")

    # 2. Xóa các bản ghi trùng lặp (Duplicates)
    dup_count = df.duplicated().sum()
    df = df.drop_duplicates().reset_index(drop=True)
    print(f"[+] Đã loại bỏ {dup_count} dòng trùng lặp. Còn lại {len(df)} dòng.")

    # 3. Chuẩn hóa chuỗi ký tự và thay thế '?' bằng NaN
    cat_cols = df.select_dtypes(include=['object']).columns.tolist()
    for col in cat_cols:
        df[col] = df[col].astype(str).str.strip()
        df[col] = df[col].replace('?', np.nan)

    # 4. Kiểm tra số lượng giá trị thiếu
    missing_series = df.isnull().sum()
    missing_cols = missing_series[missing_series > 0]
    print(f"\n[+] Các cột có giá trị thiếu:")
    for col, count in missing_cols.items():
        pct = round(count / len(df) * 100, 2)
        print(f"  - {col}: {count} dòng thiếu ({pct}%)")

    # 5. Xử lý giá trị thiếu cho biến phân loại bằng Mode (Most Frequent) theo đúng đề cương
    imputed_info = {}
    for col in missing_cols.index:
        mode_val = df[col].mode()[0]
        imputed_info[col] = mode_val
        df[col] = df[col].fillna(mode_val)
        print(f"  -> Điền cột '{col}' bằng giá trị phổ biến nhất (Mode): '{mode_val}'")

    # 6. Mã hóa biến mục tiêu 'income' sang dạng nhị phân (income_num: <=50K -> 0, >50K -> 1)
    df['income_num'] = (df['income'] == '>50K').astype(int)
    print(f"\n[+] Đã tạo biến mã hóa nhị phân 'income_num' (0: <=50K, 1: >50K)")
    print(df['income_num'].value_counts())

    # 7. Kiểm tra ngoại lai (Outliers) cho các biến định lượng bằng phương pháp IQR
    num_cols = ['age', 'education_num', 'hours_per_week', 'capital_gain', 'capital_loss']
    outlier_summary = {}
    for col in num_cols:
        q1 = df[col].quantile(0.25)
        q3 = df[col].quantile(0.75)
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]
        outlier_summary[col] = {
            "Q1": q1, "Q3": q3, "IQR": iqr,
            "Lower": lower_bound, "Upper": upper_bound,
            "Outlier_Count": len(outliers),
            "Outlier_Pct": round(len(outliers) / len(df) * 100, 2)
        }

    # 8. Lưu tập dữ liệu đã làm sạch
    df.to_csv(CLEANED_DATA_PATH, index=False)
    print(f"\n[✓] Đã xuất bộ dữ liệu sạch tại: {CLEANED_DATA_PATH}")
    print(f"    Kích thước sau làm sạch: {df.shape[0]} dòng, {df.shape[1]} cột")

    # 9. Ghi báo cáo tóm tắt làm sạch
    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        f.write("BÁO CÁO KẾT QUẢ LÀM SẠCH VÀ TIỀN XỬ LÝ DỮ LIỆU\n")
        f.write("=" * 60 + "\n")
        f.write(f"Số dòng ban đầu: {initial_rows}\n")
        f.write(f"Số bản ghi trùng lặp đã loại: {dup_count}\n")
        f.write(f"Số dòng sau làm sạch: {len(df)}\n\n")
        f.write("XỬ LÝ GIÁ TRỊ THIẾU (IMPUTATION BẰNG MODE):\n")
        for k, v in imputed_info.items():
            f.write(f"  - Cột {k}: điền bằng mode '{v}'\n")
        f.write("\nTHỐNG KÊ OUTLIERS THEO IQR:\n")
        for col, s in outlier_summary.items():
            f.write(f"  - {col}: {s['Outlier_Count']} ngoại lai ({s['Outlier_Pct']}%)\n")

    return df


if __name__ == "__main__":
    clean_and_preprocess()
