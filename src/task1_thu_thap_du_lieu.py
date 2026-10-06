"""
Task 1: Thu thập và Khảo sát cấu trúc dữ liệu thô (Người thực hiện: Trịnh Phương Thùy)
Đồ án 1: Phân tích nhân khẩu học và dự đoán mức thu nhập cá nhân (US Adult Census)
Nhóm: 1_2 - Lớp: DHKL18A1HN
"""

import os
import sys
import pandas as pd

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = r"D:\Đồ án 1"
RAW_DATA_PATH = os.path.join(BASE_DIR, "data", "adult_raw.csv")
REPORT_PATH = os.path.join(BASE_DIR, "reports", "task1_data_summary.txt")


def inspect_raw_data():
    print("=" * 60)
    print("TASK 1: THU THẬP VÀ MÔ TẢ CẤU TRÚC DỮ LIỆU BAN ĐẦU")
    print("Người thực hiện: Trịnh Phương Thùy")
    print("=" * 60)

    if not os.path.exists(RAW_DATA_PATH):
        raise FileNotFoundError(f"Không tìm thấy file: {RAW_DATA_PATH}")

    df = pd.read_csv(RAW_DATA_PATH)
    n_rows, n_cols = df.shape
    print(f"\n[+] Kích thước tập dữ liệu thô: {n_rows} dòng x {n_cols} cột")

    # Xác định danh sách cột và kiểu dữ liệu
    print("\n[+] Danh sách các biến và kiểu dữ liệu:")
    col_info = []
    for col in df.columns:
        dtype = str(df[col].dtype)
        # Đếm số lượng dấu '?' (missing values đặc thù của bộ Adult Census)
        q_count = (df[col] == '?').sum() if dtype == 'object' else 0
        null_count = df[col].isnull().sum()
        total_missing = q_count + null_count
        col_info.append({
            "Tên biến": col,
            "Kiểu dữ liệu": dtype,
            "Số giá trị thiếu (?)": q_count,
            "Tỷ lệ thiếu (%)": round(total_missing / n_rows * 100, 2),
            "Số giá trị duy nhất": df[col].nunique()
        })
        print(f"  - {col:<18} | Dtype: {dtype:<8} | Missing (?): {total_missing:<6} | Unique: {df[col].nunique()}")

    info_df = pd.DataFrame(col_info)

    # Kiểm tra biến mục tiêu
    target_col = 'income'
    print(f"\n[+] Phân bố biến mục tiêu '{target_col}':")
    target_counts = df[target_col].value_counts()
    for val, count in target_counts.items():
        pct = round(count / n_rows * 100, 2)
        print(f"  - {val}: {count} mẫu ({pct}%)")

    # Kiểm tra bản ghi trùng lặp
    dup_count = df.duplicated().sum()
    print(f"\n[+] Số bản ghi trùng lặp (duplicated rows): {dup_count} ({round(dup_count/n_rows*100, 2)}%)")

    # Xuất báo cáo tóm tắt
    os.makedirs(os.path.dirname(REPORT_PATH), exist_ok=True)
    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        f.write("BÁO CÁO CẤU TRÚC DỮ LIỆU THÔ - US ADULT CENSUS\n")
        f.write("=" * 60 + "\n")
        f.write(f"Số dòng: {n_rows}\nSố cột: {n_cols}\n")
        f.write(f"Số bản ghi trùng lặp: {dup_count}\n\n")
        f.write("CHI TIẾT CÁC CỘT:\n")
        f.write(info_df.to_string(index=False) + "\n\n")
        f.write("PHÂN BỐ BIẾN MỤC TIÊU:\n")
        f.write(target_counts.to_string() + "\n")

    print(f"\n[✓] Đã xuất báo cáo cấu trúc dữ liệu thô tại: {REPORT_PATH}")
    return df


if __name__ == "__main__":
    inspect_raw_data()
