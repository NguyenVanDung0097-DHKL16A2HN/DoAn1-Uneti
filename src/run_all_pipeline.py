"""
Pipeline Runner: Chạy toàn bộ các Task phân tích dữ liệu và mô hình Machine Learning
Đồ án 1: Phân tích nhân khẩu học và dự đoán mức thu nhập cá nhân (US Adult Census)
Nhóm: 1_2 - Lớp: DHKL18A1HN
"""

import os
import sys
import time

sys.stdout.reconfigure(encoding='utf-8')
src_dir = os.path.dirname(os.path.abspath(__file__))
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

from task1_thu_thap_du_lieu import inspect_raw_data
from task2_tien_xu_ly import clean_and_preprocess
from task3_truc_quan_so_luong import plot_quantities_and_proportions
from task4_phan_phoi_don_bien import plot_univariate_distributions
from task5_so_sanh_nhom import plot_group_comparisons
from task6_ty_le_long_nhau import plot_nested_proportions
from task7_da_bien_chi_square import analyze_multivariate_and_hypothesis_test
from task8_machine_learning import run_machine_learning_pipeline


def main():
    start_time = time.time()
    print("=" * 70)
    print("BẮT ĐẦU CHẠY TOÀN BỘ PIPELINE ĐỒ ÁN 1 (NHÓM 1_2 - DHKL18A1HN)")
    print("=" * 70)

    print("\n>>> [1/8] Đang thực hiện Task 1: Thu thập & Mô tả dữ liệu (Thùy)...")
    inspect_raw_data()

    print("\n>>> [2/8] Đang thực hiện Task 2: Làm sạch & Tiền xử lý (Nhân)...")
    clean_and_preprocess()

    print("\n>>> [3/8] Đang thực hiện Task 3: Trực quan số lượng & Tỷ lệ đơn (Ngọc)...")
    plot_quantities_and_proportions()

    print("\n>>> [4/8] Đang thực hiện Task 4: Trực quan phân phối đơn biến (Dũng)...")
    plot_univariate_distributions()

    print("\n>>> [5/8] Đang thực hiện Task 5: So sánh nhóm <=50K và >50K (Phúc)...")
    plot_group_comparisons()

    print("\n>>> [6/8] Đang thực hiện Task 6: Nhóm tỷ lệ lồng nhau (Dũng & Ngọc)...")
    plot_nested_proportions()

    print("\n>>> [7/8] Đang thực hiện Task 7: Đa biến & Kiểm định Chi-square (Phúc & Dũng)...")
    analyze_multivariate_and_hypothesis_test()

    print("\n>>> [8/8] Đang thực hiện Task 8: Machine Learning Logistic Regression & Decision Tree (Phúc & Ngọc)...")
    run_machine_learning_pipeline()

    elapsed = time.time() - start_time
    print("\n" + "=" * 70)
    print(f"HOÀN THÀNH TOÀN BỘ CÁC BƯỚC PIPELINE TRONG {elapsed:.2f} GIÂY!")
    print("Tất cả hình ảnh đã được lưu vào: D:\\Đồ án 1\\figures\\")
    print("Tất cả báo cáo số liệu đã được lưu vào: D:\\Đồ án 1\\reports\\")
    print("=" * 70)


if __name__ == "__main__":
    main()
