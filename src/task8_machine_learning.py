"""
Task 8: Chủ đề nâng cao - Huấn luyện & Đánh giá mô hình Machine Learning
Người thực hiện: Đào Đoàn Huy Phúc & Cao Nguyên Ngọc
Đồ án 1: Phân tích nhân khẩu học và dự đoán mức thu nhập cá nhân (US Adult Census)
Nhóm: 1_2 - Lớp: DHKL18A1HN
"""

import os
import sys
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix, classification_report, roc_curve
)

sys.stdout.reconfigure(encoding='utf-8')

plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#333333'
plt.rcParams['axes.linewidth'] = 0.8

BASE_DIR = r"D:\Đồ án 1"
DATA_PATH = os.path.join(BASE_DIR, "data", "adult_cleaned.csv")
FIG_DIR = os.path.join(BASE_DIR, "figures")
REPORT_PATH = os.path.join(BASE_DIR, "reports", "task8_model_comparison.csv")


def run_machine_learning_pipeline():
    print("=" * 60)
    print("TASK 8: CHỦ ĐỀ NÂNG CAO - MACHINE LEARNING DỰ ĐOÁN THU NHẬP")
    print("Người thực hiện: Đào Đoàn Huy Phúc & Cao Nguyên Ngọc")
    print("=" * 60)

    df = pd.read_csv(DATA_PATH)

    # 1. Chuẩn bị đặc trưng (Features) và Biến mục tiêu (Target)
    feature_cols = [
        'age', 'workclass', 'education_num', 'marital_status',
        'occupation', 'relationship', 'race', 'sex',
        'capital_gain', 'capital_loss', 'hours_per_week'
    ]
    X = df[feature_cols].copy()
    y = df['income_num'].copy()

    # Xác định các cột phân loại và số
    cat_cols = ['workclass', 'marital_status', 'occupation', 'relationship', 'race', 'sex']
    num_cols = ['age', 'education_num', 'capital_gain', 'capital_loss', 'hours_per_week']

    # One-Hot Encoding cho các biến phân loại
    X_encoded = pd.get_dummies(X, columns=cat_cols, drop_first=True)
    feature_names = X_encoded.columns.tolist()

    # 2. Phân chia tập Train/Test theo tỷ lệ 80/20 có Stratify
    X_train, X_test, y_train, y_test = train_test_split(
        X_encoded, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"\n[+] Kích thước tập Train: {X_train.shape[0]} mẫu, {X_train.shape[1]} đặc trưng")
    print(f"[+] Kích thước tập Test:  {X_test.shape[0]} mẫu, {X_test.shape[1]} đặc trưng")

    # 3. Chuẩn hóa đặc trưng định lượng bằng StandardScaler
    scaler = StandardScaler()
    X_train_scaled = X_train.copy()
    X_test_scaled = X_test.copy()

    X_train_scaled[num_cols] = scaler.fit_transform(X_train[num_cols])
    X_test_scaled[num_cols] = scaler.transform(X_test[num_cols])

    # 4. Huấn luyện các mô hình
    models = {
        "Logistic Regression": LogisticRegression(max_iter=1000, random_state=42),
        "Decision Tree": DecisionTreeClassifier(max_depth=7, min_samples_split=20, random_state=42)
    }

    results = []
    y_preds = {}
    y_probas = {}

    for name, model in models.items():
        print(f"\n[+] Đang huấn luyện: {name}...")
        model.fit(X_train_scaled, y_train)

        y_pred = model.predict(X_test_scaled)
        y_proba = model.predict_proba(X_test_scaled)[:, 1]

        y_preds[name] = y_pred
        y_probas[name] = y_proba

        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred)
        rec = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        auc = roc_auc_score(y_test, y_proba)

        results.append({
            "Mô hình": name,
            "Accuracy": round(acc, 4),
            "Precision": round(prec, 4),
            "Recall": round(rec, 4),
            "F1-Score": round(f1, 4),
            "ROC-AUC": round(auc, 4)
        })

        print(f"--- Báo cáo phân loại {name} ---")
        print(classification_report(y_test, y_pred, target_names=['<=50K', '>50K']))

    res_df = pd.DataFrame(results)
    res_df.to_csv(REPORT_PATH, index=False, encoding='utf-8-sig')
    print("\n[+] BẢNG SO SÁNH KẾT QUẢ CÁC MÔ HÌNH:")
    print(res_df.to_string(index=False))
    print(f"[✓] Đã xuất bảng so sánh mô hình tại: {REPORT_PATH}")

    # -------------------------------------------------------------
    # 5. BIỂU ĐỒ 11: CONFUSION MATRIX
    # -------------------------------------------------------------
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    for idx, (name, y_pred) in enumerate(y_preds.items()):
        cm = confusion_matrix(y_test, y_pred)
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=axes[idx],
                    xticklabels=['<=50K', '>50K'], yticklabels=['<=50K', '>50K'])
        axes[idx].set_title(f"Confusion Matrix: {name}", fontsize=12, fontweight='bold')
        axes[idx].set_xlabel("Dự đoán (Predicted)", fontweight='bold')
        axes[idx].set_ylabel("Thực tế (Actual)", fontweight='bold')

    plt.suptitle("Biểu đồ 11: Ma trận nhầm lẫn (Confusion Matrix) của 2 mô hình",
                 fontsize=13, fontweight='bold', y=1.02)
    plt.tight_layout()
    fig11_path = os.path.join(FIG_DIR, "fig11_confusion_matrices.png")
    plt.savefig(fig11_path, dpi=300)
    plt.close()
    print(f"[✓] Đã lưu: {fig11_path}")

    # -------------------------------------------------------------
    # 6. BIỂU ĐỒ 12: ĐƯỜNG CONG ROC CURVE
    # -------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(7, 6))
    colors = ['#2980b9', '#e67e22']

    for idx, (name, y_proba) in enumerate(y_probas.items()):
        fpr, tpr, _ = roc_curve(y_test, y_proba)
        auc = roc_auc_score(y_test, y_proba)
        ax.plot(fpr, tpr, color=colors[idx], lw=2, label=f'{name} (AUC = {auc:.3f})')

    ax.plot([0, 1], [0, 1], color='gray', linestyle='--', lw=1.5)
    ax.set_title("Biểu đồ 12: So sánh đường cong ROC giữa các mô hình", fontsize=12, fontweight='bold', pad=12)
    ax.set_xlabel("Tỷ lệ dương tính giả (False Positive Rate)", fontweight='bold')
    ax.set_ylabel("Tỷ lệ dương tính thật (True Positive Rate)", fontweight='bold')
    ax.legend(loc="lower right", fontsize=10)
    ax.grid(True, linestyle=':', alpha=0.6)

    plt.tight_layout()
    fig12_path = os.path.join(FIG_DIR, "fig12_roc_curves.png")
    plt.savefig(fig12_path, dpi=300)
    plt.close()
    print(f"[✓] Đã lưu: {fig12_path}")

    # -------------------------------------------------------------
    # 7. BIỂU ĐỒ 13: ĐẶC TRƯNG QUAN TRỌNG NHẤT (FEATURE IMPORTANCE)
    # -------------------------------------------------------------
    dt_model = models["Decision Tree"]
    importances = dt_model.feature_importances_
    feat_df = pd.DataFrame({"Feature": feature_names, "Importance": importances})
    feat_df = feat_df.sort_values(by="Importance", ascending=False).head(10)

    fig, ax = plt.subplots(figsize=(9, 6))
    bars = ax.barh(feat_df["Feature"][::-1], feat_df["Importance"][::-1],
                   color='#16a085', edgecolor='black', alpha=0.85)
    ax.set_title("Biểu đồ 13: Top 10 đặc trưng quan trọng nhất (Decision Tree)", fontsize=12, fontweight='bold', pad=12)
    ax.set_xlabel("Mức độ quan trọng (Feature Importance)", fontweight='bold')
    ax.grid(axis='x', linestyle=':', alpha=0.6)

    for bar in bars:
        w = bar.get_width()
        ax.text(w + 0.005, bar.get_y() + bar.get_height()/2., f"{w:.3f}",
                va='center', ha='left', fontsize=9, fontweight='bold')

    plt.tight_layout()
    fig13_path = os.path.join(FIG_DIR, "fig13_feature_importance.png")
    plt.savefig(fig13_path, dpi=300)
    plt.close()
    print(f"[✓] Đã lưu: {fig13_path}")


if __name__ == "__main__":
    run_machine_learning_pipeline()
