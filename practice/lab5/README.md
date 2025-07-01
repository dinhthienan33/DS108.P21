# Xử lý và chuẩn hóa dữ liệu địa chỉ

Module xử lý dữ liệu địa chỉ từ file `address_full_0712.xlsx` và chuẩn hóa theo format file mẫu `D_data_address.csv`.

## Cấu trúc dự án

```
lab5/
├── data/                           # Dữ liệu đầu vào
│   ├── address_full_0712.xlsx     # File dữ liệu chính
│   └── D_data_address.csv         # File mẫu
├── main.py                        # File chính
├── data_loader.py                 # Module tải dữ liệu
├── address_processor.py           # Module xử lý địa chỉ
├── file_utils.py                  # Module xuất file
├── config.py                      # Cấu hình
└── requirements.txt               # Thư viện cần thiết
```

## Cài đặt

```bash
pip install -r requirements.txt
```

## Sử dụng

```bash
python main.py
```

## Kết quả

- `output/processed_addresses.csv` - File CSV kết quả
- `output/processed_addresses.xlsx` - File Excel kết quả

## Cấu trúc dữ liệu đầu ra

| Cột | Mô tả |
|-----|-------|
| `id` | ID duy nhất |
| `street_id` | ID đường/phố |
| `ward_id` | ID phường/xã |
| `district_id` | ID quận/huyện |
| `city_id` | ID tỉnh/thành phố |
| `country_id` | ID quốc gia |
| `full_address` | Địa chỉ đầy đủ |
| `created_at` | Thời gian tạo |
| `updated_at` | Thời gian cập nhật |
| `tsv` | Text Search Vector |

## Tính năng chính

### 1. Trích xuất thông tin địa chỉ
- Tự động nhận diện **đường/phố** (đường, phố, ngõ, hẻm)
- Tự động nhận diện **phường/xã** (phường, xã, thị trấn)
- Tự động nhận diện **quận/huyện** (quận, huyện, thị xã)
- Tự động nhận diện **tỉnh/thành phố** (tỉnh, thành phố)

### 2. Chuẩn hóa dữ liệu
- Loại bỏ ký tự đặc biệt và từ không cần thiết
- Chuẩn hóa format (viết hoa chữ cái đầu)
- Xử lý các từ viết tắt thông dụng
- Tạo TSV (Text Search Vector) để tìm kiếm

### 3. Xử lý lỗi và backup
- Tự động tạo backup file gốc
- Xử lý lỗi gracefully
- Thống kê chi tiết về kết quả

### 4. Xuất nhiều format
- CSV cho xử lý tiếp
- Excel với thống kê
- Text file cho báo cáo

## Cấu hình

Các cấu hình chính trong `config.py`:

```python
class Config:
    DATA_DIR = 'data'
    OUTPUT_DIR = 'output'
    BACKUP_DIR = 'backup'
    
    INPUT_FILE = 'address_full_0712.xlsx'
    SAMPLE_FILE = 'D_data_address - D_data_address.csv'
    
    BATCH_SIZE = 100        # Kích thước batch để in tiến trình
    MAX_TSV_WORDS = 15      # Số từ tối đa trong TSV
    ID_OFFSET = 1000000     # Offset cho ID
```

## Xử lý lỗi thường gặp

### 1. File không tồn tại
```
Lỗi: Không tìm thấy file đầu vào: data/address_full_0712.xlsx
```
**Giải pháp:** Đảm bảo file tồn tại trong thư mục `data/`

### 2. Lỗi thư viện
```
ModuleNotFoundError: No module named 'pandas'
```
**Giải pháp:** Chạy `pip install -r requirements.txt`

### 3. Lỗi quyền ghi file
```
Lỗi khi lưu file: [Errno 13] Permission denied
```
**Giải pháp:** Đảm bảo có quyền ghi trong thư mục hiện tại

## Thống kê và đánh giá

Chương trình sẽ cung cấp thống kê chi tiết về:
- Số lượng địa chỉ được xử lý
- Tỷ lệ thành công cho từng thành phần (tỉnh, quận, phường, đường)
- Thời gian xử lý
- Chất lượng dữ liệu đầu ra

## Mở rộng

Để mở rộng chương trình:
1. **Thêm pattern mới** trong `config.py` → `AddressPatterns`
2. **Thêm từ viết tắt** trong `CleaningRules.ABBREVIATION_MAP`
3. **Thêm ID mapping** trong `DatabaseConfig`
4. **Customzie logic xử lý** trong `address_processor.py`

## Tác giả

- **Dự án:** Lab5 - PreProcessingData
- **Mục tiêu:** Xây dựng module xử lý và chuẩn hóa dữ liệu địa chỉ
- **Năm:** 2024 