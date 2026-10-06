"""
Task 6: Trực quan nhóm tỷ lệ lồng nhau (Người thực hiện: Nguyễn Văn Dũng & Cao Nguyên Ngọc)
Đồ án 1: Phân tích nhân khẩu học và dự đoán mức thu nhập cá nhân (US Adult Census)
Nhóm: 1_2 - Lớp: DHKL18A1HN
"""

import os
import sys
import matplotlib.pyplot as plt
import pandas as pd

sys.stdout.reconfigure(encoding='utf-8')

plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#333333'
plt.rcParams['axes.linewidth'] = 0.8

BASE_DIR = r"D:\Đồ án 1"
DATA_PATH = os.path.join(BASE_DIR, "data", "adult_cleaned.csv")
FIG_DIR = os.path.join(BASE_DIR, "figures")
REPORT_PATH = os.path.join(BASE_DIR, "reports", "task6_nested_proportions.csv")


def plot_nested_proportions():
    print("=" * 60)
    print("TASK 6: TRỰC QUAN NHÓM TỶ LỆ LỒNG NHAU")
    print("Người thực hiện: Nguyễn Văn Dũng & Cao Nguyên Ngọc")
    print("=" * 60)

    df = pd.read_csv(DATA_PATH)

    # Chia nhóm số giờ làm việc thành các khoảng: <35h (Part-time), 35-40h (Standard), >40h (Overtime)
    df['hours_group'] = pd.cut(
        df['hours_per_week'],
        bins=[0, 34, 40, 100],
        labels=['Part-time (<35h)', 'Standard (35-40h)', 'Overtime (>40h)']
    )

    # Đơn giản hóa một số biến phân loại để biểu đồ trực quan, dễ đọc
    # Nhóm học vấn chính
    edu_map = {
        'Preschool': 'Pre-HS', '1st-4th': 'Pre-HS', '5th-6th': 'Pre-HS', '7th-8th': 'Pre-HS',
        '9th': 'HS-Dropout', '10th': 'HS-Dropout', '11th': 'HS-Dropout', '12th': 'HS-Dropout',
        'HS-grad': 'HS-grad', 'Some-college': 'Some-college', 'Assoc-voc': 'Assoc',
        'Assoc-acdm': 'Assoc', 'Bachelors': 'Bachelors', 'Masters': 'Masters',
        'Prof-school': 'Prof-school', 'Doctorate': 'Doctorate'
    }
    df['edu_grouped'] = df['education'].map(edu_map).fillna('Other')

    # Nhóm hôn nhân
    mar_map = {
        'Married-civ-spouse': 'Married', 'Married-AF-spouse': 'Married', 'Married-spouse-absent': 'Separated',
        'Never-married': 'Single', 'Divorced': 'Divorced', 'Separated': 'Separated', 'Widowed': 'Widowed'
    }
    df['marital_grouped'] = df['marital_status'].map(mar_map).fillna('Other')

    fig, axes = plt.subplots(2, 2, figsize=(16, 14))

    # 1. Học vấn & Giới tính vs Thu nhập
    ct1 = pd.crosstab(index=[df['edu_grouped'], df['sex']], columns=df['income'], normalize='index') * 100
    top_ct1 = ct1.loc[['HS-grad', 'Some-college', 'Bachelors', 'Masters', 'Doctorate']]
    top_ct1.plot(kind='barh', stacked=True, color=['#3498db', '#e74c3c'], ax=axes[0, 0], edgecolor='black')
    axes[0, 0].set_title("(a) Tỷ lệ thu nhập theo Trình độ học vấn & Giới tính", fontsize=11, fontweight='bold')
    axes[0, 0].set_xlabel("Tỷ lệ phần trăm (%)", fontweight='bold')
    axes[0, 0].set_ylabel("Học vấn - Giới tính", fontweight='bold')
    axes[0, 0].legend(title='Income', loc='lower right')
    axes[0, 0].grid(axis='x', linestyle=':', alpha=0.6)

    # 2. Nghề nghiệp & Giới tính vs Thu nhập
    # Lấy top 6 nghề phổ biến nhất
    top_occ = df['occupation'].value_counts().head(6).index
    df_top_occ = df[df['occupation'].isin(top_occ)]
    ct2 = pd.crosstab(index=[df_top_occ['occupation'], df_top_occ['sex']], columns=df_top_occ['income'], normalize='index') * 100
    ct2.plot(kind='barh', stacked=True, color=['#3498db', '#e74c3c'], ax=axes[0, 1], edgecolor='black')
    axes[0, 1].set_title("(b) Tỷ lệ thu nhập theo Nghề nghiệp & Giới tính (Top 6 nghề)", fontsize=11, fontweight='bold')
    axes[0, 1].set_xlabel("Tỷ lệ phần trăm (%)", fontweight='bold')
    axes[0, 1].set_ylabel("Nghề nghiệp - Giới tính", fontweight='bold')
    axes[0, 1].legend(title='Income', loc='lower right')
    axes[0, 1].grid(axis='x', linestyle=':', alpha=0.6)

    # 3. Học vấn & Tình trạng hôn nhân vs Thu nhập
    df_edu_mar = df[df['edu_grouped'].isin(['HS-grad', 'Bachelors', 'Masters', 'Doctorate'])]
    ct3 = pd.crosstab(index=[df_edu_mar['edu_grouped'], df_edu_mar['marital_grouped']], columns=df_edu_mar['income'], normalize='index') * 100
    ct3.plot(kind='barh', stacked=True, color=['#3498db', '#e74c3c'], ax=axes[1, 0], edgecolor='black')
    axes[1, 0].set_title("(c) Tỷ lệ thu nhập theo Học vấn & Tình trạng hôn nhân", fontsize=11, fontweight='bold')
    axes[1, 0].set_xlabel("Tỷ lệ phần trăm (%)", fontweight='bold')
    axes[1, 0].set_ylabel("Học vấn - Hôn nhân", fontweight='bold')
    axes[1, 0].legend(title='Income', loc='lower right')
    axes[1, 0].grid(axis='x', linestyle=':', alpha=0.6)

    # 4. Nghề nghiệp & Số giờ làm việc vs Thu nhập
    ct4 = pd.crosstab(index=[df_top_occ['occupation'], df_top_occ['hours_group']], columns=df_top_occ['income'], normalize='index') * 100
    ct4.plot(kind='barh', stacked=True, color=['#3498db', '#e74c3c'], ax=axes[1, 1], edgecolor='black')
    axes[1, 1].set_title("(d) Tỷ lệ thu nhập theo Nghề nghiệp & Số giờ làm việc", fontsize=11, fontweight='bold')
    axes[1, 1].set_xlabel("Tỷ lệ phần trăm (%)", fontweight='bold')
    axes[1, 1].set_ylabel("Nghề nghiệp - Khung giờ làm", fontweight='bold')
    axes[1, 1].legend(title='Income', loc='lower right')
    axes[1, 1].grid(axis='x', linestyle=':', alpha=0.6)

    plt.suptitle("Biểu đồ 8: Trực quan nhóm tỷ lệ lồng nhau (100% Stacked Bar Charts)",
                 fontsize=14, fontweight='bold', y=0.99)
    plt.tight_layout()
    fig8_path = os.path.join(FIG_DIR, "fig8_nested_stacked_bars.png")
    plt.savefig(fig8_path, dpi=300)
    plt.close()
    print(f"[✓] Đã lưu: {fig8_path}")

    # Xuất dữ liệu bảng tỷ lệ sang file CSV để đưa vào báo cáo
    ct1.reset_index().to_csv(REPORT_PATH, index=False, encoding='utf-8-sig')
    print(f"[✓] Đã xuất báo cáo tỷ lệ lồng nhau tại: {REPORT_PATH}")


if __name__ == "__main__":
    plot_nested_proportions()
