"""
Task 7: Trực quan mối liên hệ đa biến & Kiểm định Chi-square
Người thực hiện: Đào Đoàn Huy Phúc & Nguyễn Văn Dũng
Đồ án 1: Phân tích nhân khẩu học và dự đoán mức thu nhập cá nhân (US Adult Census)
Nhóm: 1_2 - Lớp: DHKL18A1HN
"""

import os
import sys
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from scipy.stats import chi2_contingency

sys.stdout.reconfigure(encoding='utf-8')

plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#333333'
plt.rcParams['axes.linewidth'] = 0.8

BASE_DIR = r"D:\Đồ án 1"
DATA_PATH = os.path.join(BASE_DIR, "data", "adult_cleaned.csv")
FIG_DIR = os.path.join(BASE_DIR, "figures")
REPORT_PATH = os.path.join(BASE_DIR, "reports", "task7_chi_square_results.txt")


def analyze_multivariate_and_hypothesis_test():
    print("=" * 60)
    print("TASK 7: TRỰC QUAN MỐI LIÊN HỆ ĐA BIẾN & KIỂM ĐỊNH CHI-SQUARE")
    print("Người thực hiện: Đào Đoàn Huy Phúc & Nguyễn Văn Dũng")
    print("=" * 60)

    df = pd.read_csv(DATA_PATH)
    num_cols = ['age', 'education_num', 'hours_per_week', 'capital_gain', 'capital_loss', 'income_num']
    num_labels = ['Age', 'Education Num', 'Hours / Week', 'Capital Gain', 'Capital Loss', 'Income (>50K)']

    # -------------------------------------------------------------
    # 1. BIỂU ĐỒ 9: HEATMAP MA TRẬN TƯƠNG QUAN (CORRELATION HEATMAP)
    # -------------------------------------------------------------
    corr_matrix = df[num_cols].corr()

    fig, ax = plt.subplots(figsize=(8, 6.5))
    sns.heatmap(
        corr_matrix,
        annot=True,
        fmt=".3f",
        cmap='coolwarm',
        vmin=-0.2, vmax=1.0,
        xticklabels=num_labels,
        yticklabels=num_labels,
        linewidths=0.5,
        ax=ax
    )
    ax.set_title("Biểu đồ 9: Ma trận hệ số tương quan Pearson giữa các biến định lượng",
                 fontsize=12, fontweight='bold', pad=15)
    plt.tight_layout()
    fig9_path = os.path.join(FIG_DIR, "fig9_correlation_heatmap.png")
    plt.savefig(fig9_path, dpi=300)
    plt.close()
    print(f"[✓] Đã lưu: {fig9_path}")

    # -------------------------------------------------------------
    # 2. BIỂU ĐỒ 10: SCATTER MATRIX (PAIRPLOT)
    # -------------------------------------------------------------
    # Chọn ngẫu nhiên mẫu (sample 3,000 dòng) để vẽ scatter plot mượt mà, trực quan
    sample_df = df.sample(n=3000, random_state=42)
    pairplot_cols = ['age', 'education_num', 'hours_per_week', 'income']

    pair = sns.pairplot(
        sample_df[pairplot_cols],
        hue='income',
        palette={'<=50K': '#3498db', '>50K': '#e74c3c'},
        plot_kws={'alpha': 0.4, 's': 20},
        diag_kind='kde'
    )
    pair.fig.subplots_adjust(top=0.94)
    pair.fig.suptitle("Biểu đồ 10: Ma trận phân tán (Scatter Matrix) giữa các biến chính",
                      fontsize=13, fontweight='bold')
    fig10_path = os.path.join(FIG_DIR, "fig10_scatter_matrix.png")
    pair.savefig(fig10_path, dpi=300)
    plt.close()
    print(f"[✓] Đã lưu: {fig10_path}")

    # -------------------------------------------------------------
    # 3. KIỂM ĐỊNH CHI-SQUARE (α = 0.05)
    # -------------------------------------------------------------
    alpha = 0.05
    results_text = []
    results_text.append("KẾT QUẢ KIỂM ĐỊNH CHI-SQUARE VỀ TÍNH ĐỘC LẬP")
    results_text.append("=" * 60)
    results_text.append(f"Mức ý nghĩa: alpha = {alpha}\n")

    tests = [
        ("education", "income", "Học vấn và Mức thu nhập (Education x Income)"),
        ("sex", "income", "Giới tính và Mức thu nhập (Sex x Income)"),
        ("occupation", "income", "Nghề nghiệp và Mức thu nhập (Occupation x Income)"),
        ("marital_status", "income", "Tình trạng hôn nhân và Mức thu nhập (Marital Status x Income)")
    ]

    print("\n[+] Kết quả kiểm định Chi-square:")
    for var1, var2, label in tests:
        contingency_table = pd.crosstab(df[var1], df[var2])
        chi2, p_val, dof, expected = chi2_contingency(contingency_table)

        is_significant = p_val < alpha
        decision = "Bác bỏ giả thuyết H0 (Có mối liên hệ có ý nghĩa thống kê)" if is_significant else "Chấp nhận H0 (Không có mối liên hệ)"

        line = (f"[*] Kiểm định: {label}\n"
                f"    - Bảng chéo kích thước: {contingency_table.shape}\n"
                f"    - Giá trị Chi-square thống kê: {chi2:.4f}\n"
                f"    - Bậc tự do (Degrees of Freedom - dof): {dof}\n"
                f"    - p-value: {p_val:.4e}\n"
                f"    - Kết luận (alpha={alpha}): {decision}\n")
        print(line)
        results_text.append(line)

    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(results_text))
    print(f"[✓] Đã xuất báo cáo kiểm định Chi-square tại: {REPORT_PATH}")


if __name__ == "__main__":
    analyze_multivariate_and_hypothesis_test()
