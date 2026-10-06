# ĐỒ ÁN 1: PHÂN TÍCH NHÂN KHẨU HỌC VÀ DỰ ĐOÁN MỨC THU NHẬP CÁ NHÂN (US ADULT CENSUS)

- **Khoa:** Khoa học Ứng dụng  
- **Bộ môn:** Toán & Khoa học Dữ liệu  
- **Nhóm thực hiện:** Nhóm 1_2 - Lớp: DHKL18A1HN  
- **Giảng viên hướng dẫn:** ThS. Trần Chí Lê  

---

## Danh sách thành viên

1. **Đào Đoàn Huy Phúc** (Trưởng nhóm) - MSV: `24174600034` - SĐT: `0359027493`
2. **Mai Đức Nhân** - MSV: `24174600026` - SĐT: `0355904136`
3. **Cao Nguyên Ngọc** - MSV: `24174600052` - SĐT: `0325142006`
4. **Nguyễn Văn Dũng** - MSV: `22174600097` - SĐT: `0971024809`
5. **Trịnh Phương Thùy**

---

## Cấu trúc thư mục dự án

```text
D:\Đồ án 1\
├── data/
│   ├── adult_raw.csv                 # Dữ liệu thô thu thập từ Kaggle (Task 1)
│   └── adult_cleaned.csv             # Dữ liệu đã làm sạch và mã hóa (Task 2)
│
├── figures/                          # 13 biểu đồ chất lượng cao (300 DPI)
│   ├── fig1_income_counts.png        # Biểu đồ cột phân bố thu nhập
│   ├── fig2_income_pie.png           # Biểu đồ tròn tỷ lệ thu nhập
│   ├── fig3_income_by_demographics.png # Phân bố thu nhập theo nhân khẩu học
│   ├── fig4_distribution_histograms.png # Histogram & KDE đơn biến (Dũng)
│   ├── fig5_distribution_boxplots.png   # Boxplot phát hiện ngoại lai (Dũng)
│   ├── fig6_group_boxplots_by_income.png# Boxplot so sánh theo nhóm thu nhập (Phúc)
│   ├── fig7_group_violin_plots.png   # Violin plot so sánh theo nhóm (Phúc)
│   ├── fig8_nested_stacked_bars.png  # Biểu đồ cột chồng lồng nhau (Dũng & Ngọc)
│   ├── fig9_correlation_heatmap.png # Ma trận tương quan Pearson (Phúc & Dũng)
│   ├── fig10_scatter_matrix.png      # Ma trận phân tán Pairplot (Phúc & Dũng)
│   ├── fig11_confusion_matrices.png  # Confusion Matrix Logistic & Tree (Task 8)
│   ├── fig12_roc_curves.png          # ROC-AUC so sánh 2 mô hình (Task 8)
│   └── fig13_feature_importance.png  # Đặc trưng quan trọng Decision Tree (Task 8)
│
├── notebooks/
│   ├── 01_data_cleaning_eda.ipynb    # Jupyter Notebook hoàn chỉnh phần EDA
│   └── 02_model_machine_learning.ipynb# Jupyter Notebook phần Machine Learning
│
├── reports/
│   ├── Bao_Cao_Do_An_1_Nhom_1_2.docx # Báo cáo Word hoàn chỉnh chuẩn form đồ án
│   ├── Bao_Cao_Do_An_1.md            # Bản thảo báo cáo Markdown chi tiết
│   ├── Slide_Thuyet_Trinh_Do_An_1.pptx # Slide thuyết trình PowerPoint chuyên nghiệp
│   ├── task1_data_summary.txt        # Tóm tắt cấu trúc dữ liệu thô
│   ├── task2_cleaning_summary.txt    # Tóm tắt kết quả tiền xử lý
│   ├── task4_descriptive_stats.csv   # Thống kê mô tả đơn biến (Dũng)
│   ├── task5_group_comparison.csv    # So sánh giữa nhóm <=50K và >50K (Phúc)
│   ├── task6_nested_proportions.csv  # Bảng tỷ lệ lồng nhau (Dũng & Ngọc)
│   ├── task7_chi_square_results.txt  # Kết quả kiểm định Chi-square (Phúc & Dũng)
│   └── task8_model_comparison.csv    # Bảng so sánh hiệu năng các mô hình
│
├── src/
│   ├── task1_thu_thap_du_lieu.py     # Script Task 1 (Thùy)
│   ├── task2_tien_xu_ly.py           # Script Task 2 (Nhân)
│   ├── task3_truc_quan_so_luong.py   # Script Task 3 (Ngọc)
│   ├── task4_phan_phoi_don_bien.py   # Script Task 4 (Dũng)
│   ├── task5_so_sanh_nhom.py         # Script Task 5 (Phúc)
│   ├── task6_ty_le_long_nhau.py      # Script Task 6 (Dũng & Ngọc)
│   ├── task7_da_bien_chi_square.py   # Script Task 7 (Phúc & Dũng)
│   ├── task8_machine_learning.py     # Script Task 8 (Phúc & Ngọc)
│   └── run_all_pipeline.py           # Chạy tự động toàn bộ 8 tasks
│
├── README.md
└── requirements.txt
```

---

## Hướng dẫn cài đặt và chạy

### 1. Cài đặt các thư viện cần thiết
```bash
pip install -r requirements.txt
```

### 2. Chạy toàn bộ pipeline tự động (từ Task 1 đến Task 8)
```bash
python "D:\Đồ án 1\src\run_all_pipeline.py"
```

### 3. Chạy từng task riêng lẻ
```bash
# Task 1: Thu thập & mô tả dữ liệu thô (Thùy)
python "D:\Đồ án 1\src\task1_thu_thap_du_lieu.py"

# Task 2: Tiền xử lý & làm sạch (Nhân)
python "D:\Đồ án 1\src\task2_tien_xu_ly.py"

# Task 3: Trực quan số lượng & tỷ lệ (Ngọc)
python "D:\Đồ án 1\src\task3_truc_quan_so_luong.py"

# Task 4: Khảo sát phân phối đơn biến & Outliers (Dũng)
python "D:\Đồ án 1\src\task4_phan_phoi_don_bien.py"

# Task 5: So sánh nhóm <=50K và >50K (Phúc)
python "D:\Đồ án 1\src\task5_so_sanh_nhom.py"

# Task 6: Nhóm tỷ lệ lồng nhau (Dũng & Ngọc)
python "D:\Đồ án 1\src\task6_ty_le_long_nhau.py"

# Task 7: Đa biến & Kiểm định Chi-square (Phúc & Dũng)
python "D:\Đồ án 1\src\task7_da_bien_chi_square.py"

# Task 8: Huấn luyện Machine Learning (Phúc & Ngọc)
python "D:\Đồ án 1\src\task8_machine_learning.py"
```

### 4. Mở Jupyter Notebook để báo cáo tương tác
```bash
cd "D:\Đồ án 1\notebooks"
jupyter notebook
```
Mở `01_data_cleaning_eda.ipynb` hoặc `02_model_machine_learning.ipynb`.
