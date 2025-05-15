# Báo cáo Phân tích và Xử lý Dữ liệu UCI HAR Dataset
**Tác giả: Đinh Thiên Ân**
**MSSV: 20120500**

## 1. Giới thiệu
Báo cáo này trình bày việc phân tích và xử lý dữ liệu từ bộ dữ liệu UCI Human Activity Recognition (HAR) Dataset. Bộ dữ liệu này ghi lại thông tin từ các cảm biến gia tốc và con quay hồi chuyển trên điện thoại thông minh trong quá trình người dùng thực hiện các hoạt động khác nhau như đi bộ, đi lên cầu thang, đi xuống cầu thang, ngồi, đứng và nằm.

## 2. Đọc dữ liệu
Bước đầu tiên là đọc dữ liệu từ bộ UCI HAR Dataset bao gồm:
- Dữ liệu huấn luyện (train)
- Dữ liệu kiểm tra (test)
- Danh sách các đặc trưng (features)
- Nhãn hoạt động (activity labels)

Kết quả:
- X_train: (7352, 561) mẫu dữ liệu huấn luyện
- y_train: (7352, 1) nhãn tương ứng
- X_test: (2947, 561) mẫu dữ liệu kiểm tra
- y_test: (2947, 1) nhãn tương ứng

## 3. Xử lý dữ liệu
Trong bước này, chúng tôi:
- Đặt tên cho các cột dữ liệu dựa trên tập tin features.txt
- Ghép dữ liệu huấn luyện và kiểm tra
- Ánh xạ ID hoạt động sang tên hoạt động

Thông tin về dữ liệu:
- Tổng số mẫu: 10299
- Số lượng đặc trưng: 561
- Phân bố các hoạt động:
  - LAYING: 1944 mẫu
  - STANDING: 1906 mẫu
  - SITTING: 1777 mẫu
  - WALKING: 1722 mẫu
  - WALKING_UPSTAIRS: 1544 mẫu
  - WALKING_DOWNSTAIRS: 1406 mẫu

## 4. Phân tích dữ liệu thô
### Phân bố các loại hoạt động
![Phân bố các loại hoạt động](images/activity_distribution.png)

Biểu đồ trên thể hiện phân bố các loại hoạt động trong tập dữ liệu. Ta có thể thấy các hoạt động được phân bố tương đối đồng đều, với LAYING có số lượng mẫu nhiều nhất và WALKING_DOWNSTAIRS có số lượng mẫu ít nhất.

### Phân bố đối tượng tham gia
![Phân bố đối tượng tham gia](images/subject_distribution.png)

Biểu đồ này thể hiện số lượng mẫu theo từng đối tượng tham gia. Có 30 đối tượng tham gia và số lượng mẫu trên mỗi đối tượng tương đối đồng đều.

### Phân tích các đặc trưng theo hoạt động
![Phân tích đặc trưng](images/features_boxplots.png)

Biểu đồ này so sánh các đặc trưng gia tốc và góc quay giữa các hoạt động khác nhau. Ta có thể thấy rõ sự khác biệt giữa các hoạt động, đặc biệt là giữa các hoạt động tĩnh (SITTING, STANDING, LAYING) và các hoạt động chuyển động (WALKING, WALKING_UPSTAIRS, WALKING_DOWNSTAIRS).

## 5. Chuẩn hóa dữ liệu
Để chuẩn bị cho bước giảm chiều dữ liệu, chúng tôi:
- Chọn các đặc trưng có chứa "mean()" và "std()" trong tên, giảm số lượng đặc trưng từ 561 xuống còn 66
- Sử dụng StandardScaler để chuẩn hóa dữ liệu

![Đặc trưng sau chuẩn hóa](images/normalized_features.png)

Biểu đồ trên hiển thị phân bố của một số đặc trưng sau khi chuẩn hóa. Có thể thấy dữ liệu đã được điều chỉnh về phân phối chuẩn với giá trị trung bình 0 và độ lệch chuẩn 1.

## 6. Giảm chiều dữ liệu với PCA
Để giảm chiều dữ liệu, chúng tôi sử dụng phương pháp PCA (Principal Component Analysis) với tham số giữ lại 95% phương sai.

Kết quả:
- Số chiều sau khi áp dụng PCA: 17 (giảm từ 66)
- Tổng phương sai giải thích: 95.29%

![Phương sai PCA](images/pca_variance.png)

Biểu đồ trên hiển thị phương sai giải thích của các thành phần chính. Đường màu đỏ là phương sai tích lũy, cho thấy chỉ cần 17 thành phần chính đã có thể giải thích được 95% phương sai trong dữ liệu.

### Trực quan hóa dữ liệu giảm chiều
![PCA 2D](images/pca_2d_visualization.png)

Biểu đồ này thể hiện dữ liệu sau khi giảm xuống còn 2 chiều bằng PCA. Ta có thể thấy rõ sự phân nhóm của các hoạt động, đặc biệt là hoạt động LAYING (màu vàng) tách biệt rõ với các hoạt động khác.

## 7. Huấn luyện mô hình và đánh giá
Chúng tôi sử dụng mô hình Random Forest để phân loại các hoạt động dựa trên dữ liệu đã được giảm chiều.

Kết quả:
- Độ chính xác của mô hình: 89.51%

### Ma trận nhầm lẫn
![Ma trận nhầm lẫn](images/confusion_matrix.png)

Ma trận nhầm lẫn cho thấy mô hình phân loại khá tốt cho tất cả các lớp. Hoạt động LAYING được phân loại chính xác nhất với 578/583 mẫu đúng. Các hoạt động khác cũng đạt độ chính xác tốt trên 80%.

## 8. So sánh các mô hình
Chúng tôi so sánh hiệu suất của 4 mô hình:
- Random Forest: 89.51%
- SVM: 89.16%
- KNN: 88.48%
- Neural Network: 91.26%

![So sánh mô hình](images/model_comparison.png)

Từ biểu đồ so sánh các mô hình, ta thấy Neural Network cho kết quả tốt nhất với độ chính xác 91.26%, tiếp theo là Random Forest với 89.51%.

## 9. Phân tích đặc trưng quan trọng
![Đặc trưng quan trọng](images/feature_importance_pca.png)

Biểu đồ trên hiển thị tầm quan trọng của các thành phần PCA trong mô hình Random Forest. PC1 và PC2 là hai thành phần quan trọng nhất đóng góp vào việc phân loại hoạt động.

## 10. Tổng kết
### Kết quả chính:
- Đã giảm số lượng đặc trưng từ 561 xuống còn 66 (chỉ sử dụng mean và std)
- Áp dụng PCA giảm tiếp xuống còn 17 thành phần chính (95.29% phương sai)
- Neural Network cho kết quả tốt nhất với độ chính xác 91.26%

### Kết luận:
1. Dữ liệu UCI HAR Dataset chứa các đặc trưng về gia tốc và góc quay từ smartphone
2. Đã giảm chiều dữ liệu từ nhiều đặc trưng xuống còn ít hơn nhưng vẫn giữ được 95% thông tin
3. Neural Network cho kết quả tốt nhất trong việc phân loại 6 hoạt động khác nhau
4. Các đặc trưng quan trọng đã được phân tích và trực quan hóa
5. Kết quả cho thấy mô hình có thể nhận dạng hoạt động con người với độ chính xác cao