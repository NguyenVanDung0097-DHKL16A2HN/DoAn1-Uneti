"""
Task 3: Trực quan số lượng & Tỷ lệ đơn (Người thực hiện: Cao Nguyên Ngọc)
Đồ án 1: Phân tích nhân khẩu học và dự đoán mức thu nhập cá nhân (US Adult Census)
Nhóm: 1_2 - Lớp: DHKL18A1HN
"""

import os
import sys
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

sys.stdout.reconfigure(encoding='utf-8')

# Cấu hình giao diện biểu đồ chuyên nghiệp
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#333333'
plt.rcParams['axes.linewidth'] = 0.8

BASE_DIR = r"D:\Đồ án 1"
DATA_PATH = os.path.join(BASE_DIR, "data", "adult_cleaned.csv")
FIG_DIR = os.path.join(BASE_DIR, "figures")
os.makedirs(FIG_DIR, exist_ok=True)


def plot_quantities_and_proportions():
    print("=" * 60)
    print("TASK 3: TRỰC QUAN HÓA SỐ LƯỢNG VÀ TỶ LỆ ĐƠN")
    print("Người thực hiện: Cao Nguyên Ngọc")
    print("=" * 60)

    df = pd.read_csv(DATA_PATH)
    total = len(df)
    counts = df['income'].value_counts()
    pcts = df['income'].value_counts(normalize=True) * 100

    print(f"\n[+] Thống kê số lượng và tỷ lệ biến Income:")
    for val in counts.index:
        print(f"  - Nhóm {val}: {counts[val]:,} người ({pcts[val]:.2f}%)")

    # -------------------------------------------------------------
    # 1. BIỂU ĐỒ CỘT: SỐ LƯỢNG CÁ NHÂN THEO HAI NHÓM THU NHẬP
    # -------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(7, 5))
    colors = ['#2b5c8f', '#e67e22']
    bars = ax.bar(counts.index, counts.values, color=colors, width=0.5, edgecolor='black', alpha=0.9)
    ax.set_title("Biểu đồ 1: Phân bố số lượng cá nhân theo nhóm thu nhập", fontsize=13, fontweight='bold', pad=15)
    ax.set_xlabel("Mức thu nhập", fontsize=11, fontweight='bold')
    ax.set_ylabel("Số lượng cá nhân (người)", fontsize=11, fontweight='bold')
    ax.grid(axis='y', linestyle='--', alpha=0.6)

    # Hiển thị số lượng và phần trăm trên đầu cột
    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., h + 300,
                f"{int(h):,}\n({h/total*100:.1f}%)",
                ha='center', va='bottom', fontsize=10, fontweight='bold')

    plt.tight_layout()
    fig1_path = os.path.join(FIG_DIR, "fig1_income_counts.png")
    plt.savefig(fig1_path, dpi=300)
    plt.close()
    print(f"[✓] Đã lưu: {fig1_path}")

    # -------------------------------------------------------------
    # 2. BIỂU ĐỒ TRÒN: TỶ LỆ PHẦN TRĂM CỦA HAI NHÓM THU NHẬP
    # -------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(6, 6))
    explode = (0, 0.08)
    wedges, texts, autotexts = ax.pie(
        counts.values,
        labels=[f"{k}\n({v:,})" for k, v in counts.items()],
        autopct='%1.2f%%',
        startangle=140,
        colors=['#3498db', '#e74c3c'],
        explode=explode,
        shadow=True,
        textprops={'fontsize': 11, 'fontweight': 'bold'},
        wedgeprops={'edgecolor': 'black', 'linewidth': 1}
    )
    for at in autotexts:
        at.set_color('white')
        at.set_fontsize(12)
    ax.set_title("Biểu đồ 2: Tỷ lệ phần trăm giữa hai nhóm thu nhập (<=50K vs >50K)",
                 fontsize=12, fontweight='bold', pad=15)
    plt.tight_layout()
    fig2_path = os.path.join(FIG_DIR, "fig2_income_pie.png")
    plt.savefig(fig2_path, dpi=300)
    plt.close()
    print(f"[✓] Đã lưu: {fig2_path}")

    # -------------------------------------------------------------
    # 3. BIỂU ĐỒ PHÂN BỐ THEO CÁC BIẾN NHÂN KHẨU HỌC CHÍNH (Sex, Education, Occupation)
    # -------------------------------------------------------------
    fig, axes = plt.subplots(3, 1, figsize=(12, 16))

    # a. Giới tính
    sns.countplot(data=df, x='sex', hue='income', palette=['#3498db', '#e74c3c'], ax=axes[0], edgecolor='black')
    axes[0].set_title("(a) Phân bố mức thu nhập theo Giới tính (Sex)", fontsize=12, fontweight='bold')
    axes[0].set_xlabel("Giới tính", fontweight='bold')
    axes[0].set_ylabel("Số lượng", fontweight='bold')
    axes[0].grid(axis='y', linestyle='--', alpha=0.5)

    # b. Trình độ học vấn (sắp xếp theo số lượng giảm dần)
    edu_order = df['education'].value_counts().index
    sns.countplot(data=df, x='education', hue='income', order=edu_order,
                  palette=['#3498db', '#e74c3c'], ax=axes[1], edgecolor='black')
    axes[1].set_title("(b) Phân bố mức thu nhập theo Trình độ học vấn (Education)", fontsize=12, fontweight='bold')
    axes[1].set_xlabel("Trình độ học vấn", fontweight='bold')
    axes[1].set_ylabel("Số lượng", fontweight='bold')
    axes[1].tick_params(axis='x', rotation=45)
    axes[1].grid(axis='y', linestyle='--', alpha=0.5)

    # c. Nghề nghiệp
    occ_order = df['occupation'].value_counts().index
    sns.countplot(data=df, x='occupation', hue='income', order=occ_order,
                  palette=['#3498db', '#e74c3c'], ax=axes[2], edgecolor='black')
    axes[2].set_title("(c) Phân bố mức thu nhập theo Nghề nghiệp (Occupation)", fontsize=12, fontweight='bold')
    axes[2].set_xlabel("Nghề nghiệp", fontweight='bold')
    axes[2].set_ylabel("Số lượng", fontweight='bold')
    axes[2].tick_params(axis='x', rotation=45)
    axes[2].grid(axis='y', linestyle='--', alpha=0.5)

    plt.tight_layout()
    fig3_path = os.path.join(FIG_DIR, "fig3_income_by_demographics.png")
    plt.savefig(fig3_path, dpi=300)
    plt.close()
    print(f"[✓] Đã lưu: {fig3_path}")


if __name__ == "__main__":
    plot_quantities_and_proportions()
