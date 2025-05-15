# Báo cáo Nhận xét và So sánh Mô hình Phân loại Hoạt động con người
**Tác giả: Đinh Thiên Ân**
**MSSV: 20120500**

## 1. Độ chính xác giữa các mô hình

Dựa trên báo cáo, các mô hình đã được huấn luyện và đánh giá với kết quả độ chính xác như sau:

| Mô hình | Độ chính xác |
|---------|--------------|
| Neural Network | 91.26% |
| Random Forest | 89.51% |
| SVM | 89.16% |
| KNN | 88.48% |

Từ bảng so sánh trên, có thể thấy:
- Neural Network cho hiệu suất tốt nhất với độ chính xác 91.26%, vượt trội hơn so với các mô hình khác
- Random Forest đứng thứ hai với 89.51%, chỉ kém Neural Network khoảng 1.75%
- SVM và KNN có hiệu suất thấp hơn, nhưng sự chênh lệch giữa các mô hình không quá lớn
- Tất cả các mô hình đều đạt độ chính xác khá cao (trên 88%), điều này cho thấy dữ liệu sau khi xử lý và giảm chiều vẫn giữ được các đặc trưng quan trọng để phân loại

Neural Network có hiệu suất tốt nhất có thể là do khả năng học các mối quan hệ phi tuyến phức tạp trong dữ liệu mà các mô hình khác không thể nắm bắt được hoàn toàn.

## 2. Hiệu quả dự đoán trên từng nhãn

Dựa trên ma trận nhầm lẫn của mô hình Random Forest (được hiển thị trong báo cáo), ta có thể phân tích hiệu quả dự đoán trên từng nhãn:

| Hoạt động | Precision | Recall | F1-score |
|-----------|-----------|--------|----------|
| WALKING | 0.90 | 0.86 | 0.88 |
| WALKING_UPSTAIRS | 0.83 | 0.92 | 0.87 |
| WALKING_DOWNSTAIRS | 0.87 | 0.82 | 0.85 |
| SITTING | 0.87 | 0.87 | 0.87 |
| STANDING | 0.89 | 0.88 | 0.89 |
| LAYING | 1.00 | 0.99 | 0.99 |

Từ bảng trên và ma trận nhầm lẫn, có thể thấy:
- LAYING có hiệu suất cao nhất với precision 1.00 và recall 0.99 (gần như hoàn hảo)
- WALKING_UPSTAIRS có precision thấp nhất (0.83) nhưng recall cao (0.92), cho thấy mô hình có xu hướng dự đoán nhiều mẫu vào lớp này nhưng không phải lúc nào cũng chính xác
- WALKING_DOWNSTAIRS có recall thấp nhất (0.82), nghĩa là mô hình bỏ sót nhiều mẫu thuộc lớp này
- Các hoạt động khác có hiệu suất tương đối đồng đều với precision và recall dao động từ 0.86 đến 0.90

## 3. Nhãn nào dự đoán tốt nhất, nhãn nào dự đoán không tốt và nguyên nhân

### Nhãn dự đoán tốt nhất:
**LAYING** với F1-score 0.99 (gần như hoàn hảo). Có 578/583 mẫu được phân loại chính xác.

Nguyên nhân:
- Hoạt động LAYING có đặc trưng rất khác biệt so với các hoạt động khác, đặc biệt là về góc nghiêng của điện thoại
- Từ biểu đồ PCA 2D, có thể thấy rằng các mẫu LAYING (màu vàng) tách biệt hoàn toàn với các mẫu khác, khiến việc phân loại trở nên dễ dàng hơn
- Hoạt động này có đặc trưng ổn định hơn các hoạt động khác (ít thay đổi về gia tốc và góc quay)

### Nhãn dự đoán không tốt:
**WALKING_DOWNSTAIRS** có F1-score thấp nhất (0.85), với recall 0.82 (chỉ 346/422 mẫu được phân loại chính xác).

Nguyên nhân:
- Hoạt động này có thể bị nhầm lẫn với WALKING và WALKING_UPSTAIRS do chúng đều là các hoạt động chuyển động
- Từ ma trận nhầm lẫn, ta thấy 47 mẫu WALKING_DOWNSTAIRS bị nhầm thành WALKING và 17 mẫu bị nhầm thành WALKING_UPSTAIRS
- Đặc trưng của WALKING_DOWNSTAIRS có thể bị chồng lấn với các hoạt động khác trong không gian PCA

## 4. Tỉ lệ nhầm lẫn của nhãn nào cao nhất

Từ ma trận nhầm lẫn trong báo cáo, tỉ lệ nhầm lẫn của từng nhãn như sau:

| Hoạt động | Số mẫu nhầm lẫn | Tổng số mẫu kiểm tra | Tỉ lệ nhầm lẫn |
|-----------|-----------------|----------------------|----------------|
| WALKING | 72 | 517 | 13.93% |
| WALKING_UPSTAIRS | 37 | 463 | 7.99% |
| WALKING_DOWNSTAIRS | 76 | 422 | 18.01% |
| SITTING | 69 | 533 | 12.95% |
| STANDING | 68 | 572 | 11.89% |
| LAYING | 5 | 583 | 0.86% |

**WALKING_DOWNSTAIRS** có tỉ lệ nhầm lẫn cao nhất (18.01%), với 76/422 mẫu bị phân loại sai. Đặc biệt:
- 47 mẫu bị nhầm thành WALKING
- 17 mẫu bị nhầm thành WALKING_UPSTAIRS
- 12 mẫu bị nhầm thành các hoạt động khác

Điều này cho thấy mô hình gặp khó khăn nhất trong việc phân biệt hoạt động đi xuống cầu thang với các hoạt động chuyển động khác, có thể do các đặc trưng của hoạt động này trong không gian PCA có sự chồng lấp đáng kể với các hoạt động khác.

## 5. Kết luận và đề xuất cải tiến

### Kết luận:
- Neural Network cho hiệu suất tốt nhất trong tất cả các mô hình được thử nghiệm
- Hoạt động LAYING dễ phân loại nhất do đặc trưng rất khác biệt
- Hoạt động WALKING_DOWNSTAIRS khó phân loại nhất và thường bị nhầm với các hoạt động chuyển động khác
- Phương pháp giảm chiều PCA hiệu quả trong việc giữ lại thông tin quan trọng để phân loại

### Đề xuất cải tiến:
1. **Trích xuất đặc trưng bổ sung:** Tạo thêm các đặc trưng đặc biệt để phân biệt tốt hơn giữa các hoạt động chuyển động (WALKING, WALKING_UPSTAIRS, WALKING_DOWNSTAIRS)
2. **Thử nghiệm kỹ thuật ensemble:** Kết hợp kết quả từ nhiều mô hình để nâng cao độ chính xác
3. **Tinh chỉnh tham số mô hình:** Thực hiện tìm kiếm lưới (grid search) để tối ưu hóa tham số cho các mô hình, đặc biệt là Neural Network
4. **Tăng cường dữ liệu:** Thu thập thêm dữ liệu cho các hoạt động có tỉ lệ nhầm lẫn cao
5. **Thử nghiệm các phương pháp giảm chiều khác:** Ngoài PCA, có thể thử t-SNE hoặc UMAP để xem có cải thiện khả năng phân tách các lớp không