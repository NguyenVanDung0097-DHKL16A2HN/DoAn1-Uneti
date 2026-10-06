"""
Task 4: Trực quan hóa phân phối đơn biến (Người thực hiện: Nguyễn Văn Dũng)
Đồ án 1: Phân tích nhân khẩu học và dự đoán mức thu nhập cá nhân (US Adult Census)
Nhóm: 1_2 - Lớp: DHKL18A1HN
"""

import os
import sys
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

sys.stdout.reconfigure(encoding='utf-8')

plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#333333'
plt.rcParams['axes.linewidth'] = 0.8

BASE_DIR = r"D:\Đồ án 1"
DATA_PATH = os.path.join(BASE_DIR, "data", "adult_cleaned.csv")
FIG_DIR = os.path.join(BASE_DIR, "figures")
REPORT_PATH = os.path.join(BASE_DIR, "reports", "task4_descriptive_stats.csv")


def plot_univariate_distributions():
    print("=" * 60)
    print("TASK 4: TRỰC QUAN HÓA PHÂN PHỐI ĐƠN BIẾN")
    print("Người thực hiện: Nguyễn Văn Dũng")
    print("=" * 60)

    df = pd.read_csv(DATA_PATH)
    num_cols = ['age', 'education_num', 'hours_per_week', 'capital_gain', 'capital_loss']
    col_names_vn = {
        'age': 'Độ tuổi (Age)',
        'education_num': 'Số năm học vấn (Education Num)',
        'hours_per_week': 'Số giờ làm việc / tuần (Hours per Week)',
        'capital_gain': 'Thu nhập từ vốn (Capital Gain)',
        'capital_loss': 'Khoản lỗ vốn (Capital Loss)'
    }

    # 1. Tính toán các chỉ số thống kê mô tả chi tiết
    stats_list = []
    print("\n[+] Bảng tóm tắt thống kê mô tả đơn biến:")
    for col in num_cols:
        series = df[col]
        q1 = series.quantile(0.25)
        q3 = series.quantile(0.75)
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        outliers_count = ((series < lower_bound) | (series > upper_bound)).sum()

        row = {
            "Tên biến": col_names_vn[col],
            "Ký hiệu": col,
            "Số mẫu": len(series),
            "Trung bình (Mean)": round(series.mean(), 2),
            "Độ lệch chuẩn (Std)": round(series.std(), 2),
            "Nhỏ nhất (Min)": series.min(),
            "Tứ phân vị 25% (Q1)": round(q1, 2),
            "Trung vị (Median)": round(series.median(), 2),
            "Tứ phân vị 75% (Q3)": round(q3, 2),
            "Lớn nhất (Max)": series.max(),
            "Độ lệch (Skewness)": round(series.skew(), 2),
            "Số Outliers (IQR)": outliers_count,
            "Tỷ lệ Outliers (%)": round(outliers_count / len(series) * 100, 2)
        }
        stats_list.append(row)

    stats_df = pd.DataFrame(stats_list)
    stats_df.to_csv(REPORT_PATH, index=False, encoding='utf-8-sig')
    print(stats_df[['Ký hiệu', 'Trung bình (Mean)', 'Trung vị (Median)', 'Độ lệch chuẩn (Std)', 'Số Outliers (IQR)', 'Tỷ lệ Outliers (%)']].to_string(index=False))
    print(f"\n[✓] Đã xuất bảng thống kê mô tả tại: {REPORT_PATH}")

    # -------------------------------------------------------------
    # 2. VẼ HISTOGRAM + DENSITY PLOT (KDE) CHO 5 BIẾN ĐỊNH LƯỢNG
    # -------------------------------------------------------------
    fig, axes = plt.subplots(3, 2, figsize=(14, 15))
    axes = axes.flatten()

    colors = ['#2980b9', '#27ae60', '#8e44ad', '#d35400', '#c0392b']

    for i, col in enumerate(num_cols):
        ax = axes[i]
        sns.histplot(df[col], kde=True, ax=ax, color=colors[i], bins=30, edgecolor='black', alpha=0.6)
        mean_val = df[col].mean()
        median_val = df[col].median()
        ax.axvline(mean_val, color='red', linestyle='--', linewidth=1.5, label=f'Mean: {mean_val:.1f}')
        ax.axvline(median_val, color='yellow', linestyle='-', linewidth=1.5, label=f'Median: {median_val:.1f}')
        ax.set_title(f"Phân phối {col_names_vn[col]} (Skew: {df[col].skew():.2f})", fontsize=11, fontweight='bold')
        ax.set_xlabel(col_names_vn[col], fontweight='bold')
        ax.set_ylabel("Tần số (Frequency)", fontweight='bold')
        ax.legend(fontsize=9)
        ax.grid(True, linestyle=':', alpha=0.6)

    # Ẩn subplot thứ 6 trống
    fig.delaxes(axes[5])

    plt.suptitle("Biểu đồ 4: Phân phối đơn biến (Histogram & Density KDE)", fontsize=14, fontweight='bold', y=0.99)
    plt.tight_layout()
    fig4_path = os.path.join(FIG_DIR, "fig4_distribution_histograms.png")
    plt.savefig(fig4_path, dpi=300)
    plt.close()
    print(f"[✓] Đã lưu: {fig4_path}")

    # -------------------------------------------------------------
    # 3. VẼ BOXPLOT ĐƠN BIẾN PHÁT HIỆN ĐIỂM DỮ LIỆU BẤT THƯỜNG (OUTLIERS)
    # -------------------------------------------------------------
    fig, axes = plt.subplots(1, 5, figsize=(18, 6))

    for i, col in enumerate(num_cols):
        ax = axes[i]
        sns.boxplot(y=df[col], ax=ax, color=colors[i], width=0.4,
                    flierprops=dict(marker='o', markersize=3, markerfacecolor='red', alpha=0.5))
        ax.set_title(col_names_vn[col], fontsize=10, fontweight='bold')
        ax.set_ylabel("Giá trị", fontweight='bold')
        ax.grid(True, linestyle=':', alpha=0.6)

    plt.suptitle("Biểu đồ 5: Biểu đồ hộp (Boxplot) phát hiện giá trị bất thường / Outliers",
                 fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()
    fig5_path = os.path.join(FIG_DIR, "fig5_distribution_boxplots.png")
    plt.savefig(fig5_path, dpi=300)
    plt.close()
    print(f"[✓] Đã lưu: {fig5_path}")


if __name__ == "__main__":
    plot_univariate_distributions()
