# BÁO CÁO THỰC HIỆN ĐỒ ÁN 1 (KHOA HỌC DỮ LIỆU)

**KHOA KHOA HỌC ỨNG DỤNG - BỘ MÔN TOÁN & KHOA HỌC DỮ LIỆU**  
**TÊN ĐỒ ÁN:** SỬ DỤNG NGÔN NGỮ PYTHON, R ĐỂ PHÂN TÍCH NHÂN KHẨU HỌC VÀ DỰ ĐOÁN MỨC THU NHẬP CÁ NHÂN (US ADULT CENSUS)  
**Nhóm sinh viên thực hiện:** Nhóm 1_2 - Lớp DHKL18A1HN  
**Giảng viên hướng dẫn:** ThS. Trần Chí Lê  

---

## DANH SÁCH THÀNH VIÊN NHÓM

| STT | Họ và tên | Mã sinh viên | Điện thoại | Vai trò trong nhóm |
| :---: | :--- | :---: | :---: | :--- |
| 1 | Đào Đoàn Huy Phúc | 24174600034 | 0359027493 | Trưởng nhóm |
| 2 | Mai Đức Nhân | 24174600026 | 0355904136 | Thành viên |
| 3 | Cao Nguyên Ngọc | 24174600052 | 0325142006 | Thành viên |
| 4 | Nguyễn Văn Dũng | 22174600097 | 0971024809 | Thành viên |
| 5 | Trịnh Phương Thùy | | | Thành viên |

---

## CHƯƠNG 1: GIỚI THIỆU VÀ MỤC TIÊU NGHIÊN CỨU

### 1.1. Đặt vấn đề
Thu nhập cá nhân là một chỉ báo kinh tế quan trọng phản ánh chất lượng đời sống và trình độ phát triển của xã hội. Việc khai thác dữ liệu nhân khẩu học giúp các nhà hoạch định chính sách, doanh nghiệp và các tổ chức nhận diện được sự phân bố của các nhóm dân cư theo độ tuổi, học vấn, nghề nghiệp, tình trạng hôn nhân và số giờ làm việc.

### 1.2. Mục tiêu nghiên cứu
- Thăm dò, làm sạch và trực quan hóa dữ liệu nhân khẩu học Hoa Kỳ (US Adult Census Income).
- Khảo sát các mối quan hệ đa biến, so sánh các phân nhóm dân cư và thực hiện kiểm định Chi-square độc lập giữa các biến phân loại với mức thu nhập.
- Xây dựng mô hình Machine Learning (Logistic Regression, Decision Tree) nhằm dự đoán phân lớp thu nhập (<=50K và >50K), so sánh và đánh giá hiệu năng mô hình.

---

## CHƯƠNG 2: THU THẬP VÀ TIỀN XỬ LÝ DỮ LIỆU

### 2.1. Cấu trúc bộ dữ liệu US Adult Census
Bộ dữ liệu gồm 32.561 dòng và 15 thuộc tính:
- Biến mục tiêu: `income` (`<=50K`: 24.720 dòng ~ 75,92%; `>50K`: 7.841 dòng ~ 24,08%).
- Biến định lượng: `age`, `fnlwgt`, `education.num`, `capital.gain`, `capital.loss`, `hours.per.week`.
- Biến định tính: `workclass`, `education`, `marital.status`, `occupation`, `relationship`, `race`, `sex`, `native.country`.

### 2.2. Quy trình làm sạch dữ liệu
1. **Chuẩn hóa tên cột:** Đổi dấu `.` thành `_` (e.g. `education_num`, `hours_per_week`).
2. **Loại bỏ dữ liệu trùng lặp:** Loại bỏ 24 dòng trùng lặp, còn lại 32.537 quan sát duy nhất.
3. **Xử lý giá trị thiếu (ký hiệu `?`):**
   - `workclass`: thiếu 1.836 dòng (5,64%) -> Điền Mode: `'Private'`.
   - `occupation`: thiếu 1.843 dòng (5,66%) -> Điền Mode: `'Prof-specialty'`.
   - `native_country`: thiếu 582 dòng (1,79%) -> Điền Mode: `'United-States'`.
4. **Mã hóa biến mục tiêu:** `income_num` (<=50K: 0, >50K: 1).

---

## CHƯƠNG 3: KHÁM PHÁ VÀ TRỰC QUAN HÓA DỮ LIỆU (EDA)

### 3.1. Trực quan số lượng & Tỷ lệ đơn (Ngọc)
- **Hình 3.1 & 3.2:** Biểu đồ cột và biểu đồ tròn thể hiện mức thu nhập `<=50K` chiếm 75,91% và `>50K` chiếm 24,09%. Cho thấy sự mất cân bằng giữa 2 lớp (3:1).
- **Hình 3.3:** Biểu đồ thu nhập theo Giới tính, Trình độ học vấn và Nghề nghiệp. Nam giới và các nhóm học vấn cao (Bachelors, Masters, Doctorate) có tỷ lệ thu nhập `>50K` cao vượt trội.

### 3.2. Phân phối đơn biến và phát hiện ngoại lai (Dũng)
- **Độ tuổi (Age):** Mean = 38,59; Median = 37,0; Std = 13,64. Phân phối lệch phải, phát hiện 142 ngoại lai (người trên 78 tuổi vẫn lao động).
- **Số năm học vấn (Education Num):** Mean = 10,08; Median = 10,0; Std = 2,57. Tập trung ở mốc 9 năm (HS-grad) và 13 năm (Bachelors).
- **Số giờ làm việc (Hours per Week):** Mean = 40,44; Median = 40,0. Có 9.002 trường hợp outlier (27,67%) phân tán ở các nhóm làm part-time (<35h) và overtime (>40h, cực đại 99h/tuần).
- **Capital Gain & Loss:** Độ lệch cực lớn (>11), đại đa số dân số có giá trị bằng 0.

### 3.3. So sánh phân phối theo nhóm thu nhập (Phúc)
- Người có thu nhập `>50K` có độ tuổi trung bình (44,25 tuổi) cao hơn đáng kể so với nhóm `<=50K` (36,79 tuổi).
- Số năm học vấn trung bình của nhóm `>50K` là 11,61 năm so với 9,60 năm của nhóm `<=50K`.
- Số giờ làm việc bình quân của nhóm `>50K` là 45,47 giờ/tuần so với 38,84 giờ/tuần của nhóm `<=50K`.

### 3.4. Trực quan nhóm tỷ lệ lồng nhau (Dũng & Ngọc)
- **Học vấn & Giới tính:** Ở tất cả các bậc học vấn, nam giới đều có tỷ lệ thu nhập >50K cao hơn nữ giới.
- **Học vấn & Hôn nhân:** Nhóm có gia đình (Married) kết hợp với bằng cấp đại học có tỷ lệ thu nhập >50K cao nhất toàn bộ tập dữ liệu (>65%).
- **Nghề nghiệp & Giờ làm việc:** Nhóm quản lý (Exec-managerial) làm việc trên 40h/tuần có xác suất đạt >50K vượt trội.

---

## CHƯƠNG 4: MỐI LIÊN HỆ ĐA BIẾN VÀ KIỂM ĐỊNH THỐNG KÊ (Dũng & Phúc)

### 4.1. Ma trận tương quan Pearson
- `education_num` tương quan dương mạnh nhất với `income_num` (r = +0,335).
- Tiếp theo là `age` (r = +0,234), `hours_per_week` (r = +0,230) và `capital_gain` (r = +0,223).
- Không xuất hiện hiện tượng đa cộng tuyến giữa các biến độc lập.

### 4.2. Kiểm định Chi-square về tính độc lập ($\alpha = 0{,}05$)
1. **Education × Income:** $\chi^2 = 4428{,}40$, dof = 15, $p < 0{,}0001$ -> Bác bỏ $H_0$.
2. **Sex × Income:** $\chi^2 = 1516{,}54$, dof = 1, $p < 0{,}0001$ -> Bác bỏ $H_0$.
3. **Occupation × Income:** $\chi^2 = 3197{,}61$, dof = 13, $p < 0{,}0001$ -> Bác bỏ $H_0$.
4. **Marital Status × Income:** $\chi^2 = 6510{,}33$, dof = 6, $p < 0{,}0001$ -> Bác bỏ $H_0$.

**Kết luận:** Mọi biến phân loại đều có mối liên hệ có ý nghĩa thống kê cực kỳ mạnh mẽ đối với mức thu nhập cá nhân.

---

## CHƯƠNG 5: MÔ HÌNH MACHINE LEARNING (Phúc & Ngọc)

### 5.1. Thiết lập mô hình
- Chia tập dữ liệu 80% Train (26.029 mẫu) và 20% Test (6.508 mẫu) có `stratify=y`.
- Mã hóa One-Hot Encoding biến phân loại (41 đặc trưng sau mã hóa).
- Chuẩn hóa thang đo `StandardScaler` cho biến định lượng.

### 5.2. Bảng so sánh hiệu năng trên tập Test

| Mô hình | Accuracy | Precision (>50K) | Recall (>50K) | F1-Score (>50K) | ROC-AUC |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Logistic Regression** | 85.22% | 73.67% | **60.14%** | **66.22%** | **0.8996** |
| **Decision Tree (max_depth=7)** | **85.48%** | **79.30%** | 53.76% | 64.08% | 0.8950 |

### 5.3. Nhận xét lựa chọn mô hình
- **Logistic Regression** có chỉ số F1-Score (66,22%) và ROC-AUC (0,8996) tốt hơn nhờ khả năng phát hiện người có thu nhập cao (Recall = 60,14%) vượt trội.
- **Decision Tree** đạt độ chính xác Precision cao (79,30%), phù hợp khi ưu tiên tính chắc chắn khi dự đoán thu nhập cao.
- **Top 3 đặc trưng quan trọng nhất:** Tình trạng hôn nhân (`marital_status_Married-civ-spouse`), Số năm học vấn (`education_num`) và Thu nhập từ vốn (`capital_gain`).

---

## CHƯƠNG 6: PHÂN CÔNG CÔNG VIỆC VÀ TỔNG KẾT

| STT | Công việc | Thời gian | Người thực hiện |
| :---: | :--- | :---: | :--- |
| 1 | Thu thập dữ liệu Adult Census | 5/10 - 7/10/2026 | Thùy |
| 2 | Làm sạch và tiền xử lý dữ liệu | 6/10 - 12/10/2026 | Nhân |
| 3 | Trực quan số lượng & Tỷ lệ đơn | 10/10 - 14/10/2026 | Ngọc |
| 4 | Trực quan hóa phân phối đơn biến | 11/10 - 16/10/2026 | Dũng |
| 5 | Trực quan so sánh nhóm | 13/10 - 18/10/2026 | Phúc |
| 6 | Trực quan nhóm tỷ lệ lồng nhau | 15/10 - 21/10/2026 | Dũng & Ngọc |
| 7 | Trực quan đa biến & Kiểm định Chi-square | 18/10 - 24/10/2026 | Phúc & Dũng |
| 8 | Mô hình hóa Machine Learning | 21/10 - 28/10/2026 | Phúc & Ngọc |
| 9 | Viết báo cáo và hoàn thiện slide | 20/10 - 31/10/2026 | Nhân & Thùy |
| 10 | Tổng hợp, rà soát và kiểm tra mã nguồn | 1/11 - 2/11/2026 | Cả nhóm |
