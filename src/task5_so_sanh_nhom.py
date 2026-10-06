"""
Task 5: Trực quan so sánh nhóm (<=50K và >50K) (Người thực hiện: Đào Đoàn Huy Phúc)
Đồ án 1: Phân tích nhân khẩu học và dự đoán mức thu nhập cá nhân (US Adult Census)
Nhóm: 1_2 - Lớp: DHKL18A1HN
"""

import os
import sys
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

sys.stdout.reconfigure(encoding='utf-8')

plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#333333'
plt.rcParams['axes.linewidth'] = 0.8

BASE_DIR = r"D:\Đồ án 1"
DATA_PATH = os.path.join(BASE_DIR, "data", "adult_cleaned.csv")
FIG_DIR = os.path.join(BASE_DIR, "figures")
REPORT_PATH = os.path.join(BASE_DIR, "reports", "task5_group_comparison.csv")


def plot_group_comparisons():
    print("=" * 60)
    print("TASK 5: TRỰC QUAN SO SÁNH GIỮA HAI NHÓM THU NHẬP (<=50K vs >50K)")
    print("Người thực hiện: Đào Đoàn Huy Phúc")
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

    # 1. Bảng so sánh trung bình & trung vị giữa 2 nhóm
    comp_records = []
    print("\n[+] So sánh các đặc trưng định lượng giữa 2 nhóm thu nhập:")
    for col in num_cols:
        grp = df.groupby('income')[col]
        mean_low, mean_high = grp.mean()['<=50K'], grp.mean()['>50K']
        med_low, med_high = grp.median()['<=50K'], grp.median()['>50K']
        comp_records.append({
            "Biến": col_names_vn[col],
            "Mean (<=50K)": round(mean_low, 2),
            "Mean (>50K)": round(mean_high, 2),
            "Chênh lệch Mean": round(mean_high - mean_low, 2),
            "Median (<=50K)": round(med_low, 2),
            "Median (>50K)": round(med_high, 2)
        })

    comp_df = pd.DataFrame(comp_records)
    comp_df.to_csv(REPORT_PATH, index=False, encoding='utf-8-sig')
    print(comp_df.to_string(index=False))
    print(f"\n[✓] Đã xuất báo cáo so sánh nhóm: {REPORT_PATH}")

    # -------------------------------------------------------------
    # 2. VẼ BOXPLOT SO SÁNH THEO NHÓM THU NHẬP
    # -------------------------------------------------------------
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    palette = {'<=50K': '#3498db', '>50K': '#e74c3c'}

    plot_cols = ['age', 'education_num', 'hours_per_week']
    for i, col in enumerate(plot_cols):
        sns.boxplot(data=df, x='income', y=col, palette=palette, ax=axes[i], width=0.4,
                    flierprops=dict(marker='o', markersize=2, alpha=0.3))
        axes[i].set_title(f"So sánh {col_names_vn[col]}", fontsize=11, fontweight='bold')
        axes[i].set_xlabel("Mức thu nhập", fontweight='bold')
        axes[i].set_ylabel(col_names_vn[col], fontweight='bold')
        axes[i].grid(axis='y', linestyle='--', alpha=0.5)

    plt.suptitle("Biểu đồ 6: So sánh phân phối các biến chính theo nhóm thu nhập (Boxplot)",
                 fontsize=13, fontweight='bold', y=1.02)
    plt.tight_layout()
    fig6_path = os.path.join(FIG_DIR, "fig6_group_boxplots_by_income.png")
    plt.savefig(fig6_path, dpi=300)
    plt.close()
    print(f"[✓] Đã lưu: {fig6_path}")

    # -------------------------------------------------------------
    # 3. VẼ VIOLIN PLOT SO SÁNH THEO NHÓM THU NHẬP
    # -------------------------------------------------------------
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    for i, col in enumerate(plot_cols):
        sns.violinplot(data=df, x='income', y=col, palette=palette, ax=axes[i],
                       inner='quartile', cut=0)
        axes[i].set_title(f"Mật độ {col_names_vn[col]} theo Thu nhập", fontsize=11, fontweight='bold')
        axes[i].set_xlabel("Mức thu nhập", fontweight='bold')
        axes[i].set_ylabel(col_names_vn[col], fontweight='bold')
        axes[i].grid(axis='y', linestyle='--', alpha=0.5)

    plt.suptitle("Biểu đồ 7: So sánh mật độ phân phối theo nhóm thu nhập (Violin Plot)",
                 fontsize=13, fontweight='bold', y=1.02)
    plt.tight_layout()
    fig7_path = os.path.join(FIG_DIR, "fig7_group_violin_plots.png")
    plt.savefig(fig7_path, dpi=300)
    plt.close()
    print(f"[✓] Đã lưu: {fig7_path}")


if __name__ == "__main__":
    plot_group_comparisons()
