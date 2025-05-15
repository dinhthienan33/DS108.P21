# Đồ Án Phân Tích Dữ Liệu Việc Làm Tại Việt Nam

## Giới Thiệu
Đây là đồ án môn DS108.P21, thuộc phạm vi trường Đại học Công nghệ Thông tin (UIT), tập trung vào việc thu thập và phân tích dữ liệu việc làm tại Việt Nam. Dự án nhằm mục đích cung cấp cái nhìn sâu sắc về thị trường lao động Việt Nam thông qua việc phân tích dữ liệu từ các nền tảng tuyển dụng.

## Thành Viên
- **Đinh Thiên Ân** - 22520010
- **Huỳnh Trọng Nghĩa** - 22520003



## Mục Lục
- [Đồ Án Phân Tích Dữ Liệu Việc Làm Tại Việt Nam](#đồ-án-phân-tích-dữ-liệu-việc-làm-tại-việt-nam)
  - [Giới Thiệu](#giới-thiệu)
  - [Thành Viên](#thành-viên)
  - [Mục Lục](#mục-lục)
  - [Cấu Trúc Dự Án](#cấu-trúc-dự-án)
  - [Các Giai Đoạn Dự Án](#các-giai-đoạn-dự-án)
    - [1. Thu Thập Dữ Liệu (Completed)](#1-thu-thập-dữ-liệu-completed)
    - [2. Tiền Xử Lý Dữ Liệu (Completed)](#2-tiền-xử-lý-dữ-liệu-completed)
    - [3. Phân Tích Dữ Liệu (Completed)](#3-phân-tích-dữ-liệu-completed)
    - [4. Mô Hình Dự Đoán Lương (Coming Soon)](#4-mô-hình-dự-đoán-lương-coming-soon)
    - [5. Triển Khai Hệ Thống MLOps (Coming Soon)](#5-triển-khai-hệ-thống-mlops-coming-soon)
  - [Hướng Dẫn Sử Dụng](#hướng-dẫn-sử-dụng)
    - [Yêu Cầu](#yêu-cầu)
    - [Cài Đặt](#cài-đặt)
    - [Thu Thập Dữ Liệu](#thu-thập-dữ-liệu)
    - [Tiền Xử Lý Dữ Liệu](#tiền-xử-lý-dữ-liệu)
    - [Phân Tích Dữ Liệu (EDA)](#phân-tích-dữ-liệu-eda)
  - [Kết Quả](#kết-quả)
  - [Tài Liệu Tham Khảo](#tài-liệu-tham-khảo)
  - [Giấy Phép](#giấy-phép)

## Cấu Trúc Dự Án
```
DS108/
│
├── data/                  # Thư mục chứa dữ liệu
│   ├── raw/               # Dữ liệu thô sau khi thu thập
│   ├── processed/         # Dữ liệu đã qua xử lý
│   └── final/             # Dữ liệu cuối cùng để phân tích
│
├── notebooks/             # Jupyter notebooks
│   ├── data_collection/   # Notebooks thu thập dữ liệu
│   ├── preprocessing/     # Notebooks tiền xử lý dữ liệu
│   └── analysis/          # Notebooks phân tích dữ liệu
│
├── src/                   # Mã nguồn
│   ├── data_collection/   # Scripts thu thập dữ liệu
│   ├── preprocessing/     # Scripts tiền xử lý dữ liệu
│   ├── analysis/          # Scripts phân tích dữ liệu
│   └── models/            # Scripts cho các mô hình ML
│
├── models/                # Mô hình đã huấn luyện
│
├── reports/               # Báo cáo và kết quả phân tích
│   ├── figures/           # Biểu đồ và hình ảnh
│   └── results/           # Kết quả phân tích
│
├── app/                   # Ứng dụng web (sẽ phát triển)
│
├── tests/                 # Unit tests
│
├── requirements.txt       # Các thư viện Python cần thiết
├── setup.py               # Script cài đặt dự án
└── README.md              # Tập tin này
```

## Các Giai Đoạn Dự Án

### 1. Thu Thập Dữ Liệu (Completed)
Dữ liệu việc làm được thu thập từ các nền tảng tuyển dụng trực tuyến tại Việt Nam thông qua các kỹ thuật web scraping. Quá trình này thu thập thông tin về:
- Lĩnh vực công việc
- Yêu cầu kinh nghiệm
- Địa điểm làm việc
- Quy mô công ty
- Mức lương
- Yêu cầu công việc
- URL của tin tuyển dụng

Thư mục `src/data_collection` chứa các scripts để thu thập dữ liệu từ các trang web tuyển dụng. Kết quả thu được là file `job_details_full.csv`.

### 2. Tiền Xử Lý Dữ Liệu (Completed)
Dữ liệu thô sau khi thu thập được làm sạch và chuyển đổi thành định dạng phù hợp cho phân tích. Các bước bao gồm:
- Xử lý giá trị thiếu (missing values)
- Chuẩn hóa dữ liệu văn bản
- Chuyển đổi dữ liệu kinh nghiệm sang số năm
- Phân tích và chuẩn hóa thông tin lương
- Tạo các biến mới có ích cho phân tích

Thư mục `src/preprocessing` chứa các scripts tiền xử lý dữ liệu.

### 3. Phân Tích Dữ Liệu (Completed)
Dữ liệu sau khi xử lý được phân tích để tìm ra các insights về thị trường lao động Việt Nam. Phân tích bao gồm:
- Phân bố việc làm theo lĩnh vực
- Phân bố việc làm theo địa điểm
- Phân bố việc làm theo yêu cầu kinh nghiệm
- Phân bố việc làm theo quy mô công ty
- Phân tích mức lương theo các yếu tố khác nhau

Kết quả phân tích được lưu trong notebook `EDA.ipynb` và các báo cáo trong thư mục `reports`.

### 4. Mô Hình Dự Đoán Lương (Coming Soon)
Sử dụng các thuật toán học máy để dự đoán mức lương dựa trên các yếu tố như lĩnh vực, kinh nghiệm, địa điểm, và quy mô công ty. Các mô hình dự kiến sẽ bao gồm:
- Linear Regression
- Random Forest
- Gradient Boosting
- Neural Networks

### 5. Triển Khai Hệ Thống MLOps (Coming Soon)
Xây dựng hệ thống MLOps để tự động hóa quy trình từ thu thập dữ liệu, tiền xử lý, huấn luyện mô hình đến triển khai ứng dụng dự đoán lương.
Sơ đồ quy trình:
 ```mermaid
graph TD
    A[Raw Data] --> B[Data Loading]
    B --> C[Clean Data]
    C --> D[Clean Salary]
    D --> E[Extract NLP Features]
    E --> F[Encode Categorical Features]
    F --> G[Split Data]
    G --> H[Processed Data]
    G --> I[Preprocessor Artifacts]

    H --> J[train.py]
    I --> J
    J --> K[Initialize WandB Run]
    K --> L[Train Decision Tree]
    K --> M[Train Random Forest]
    K --> N[Train XGBoost]
    K --> O[Train Neural Network]
    L --> P[Model Objects]
    M --> P
    N --> P
    O --> P
    P --> Q[Evaluate Models]
    H --> Q
    Q --> R[Log Metrics/Plots]
    P --> S[Save Models]
    I --> S
    S --> T[Saved Models]
    S --> U[Log Artifacts]

    H --> V[test.py]
    T --> V
    V --> W[Load Models]
    W --> X[Evaluate Models]
    X --> Y[Save Evaluation Results]
    Y --> Z[Generate Comparison Report]

    AA[User Input] --> BB[predict_salary.py]
    T --> BB
    I --> BB
    BB --> CC[Load Models]
    CC --> DD[Preprocess Input]
    DD --> EE[Predict Salary]
    EE --> FF[Predicted Output]

    style A fill:#f9f,stroke:#333,stroke-width:2px
    style H fill:#ccf,stroke:#333,stroke-width:1px
    style I fill:#ccf,stroke:#333,stroke-width:1px
    style T fill:#ccf,stroke:#333,stroke-width:1px
    style Y fill:#cfc,stroke:#333,stroke-width:1px
    style Z fill:#cfc,stroke:#333,stroke-width:1px
    style FF fill:#cfc,stroke:#333,stroke-width:1px
    style AA fill:#f9f,stroke:#333,stroke-width:2px
    style B fill:#bbf,stroke:#333,stroke-width:2px
    style J fill:#bbf,stroke:#333,stroke-width:2px
    style V fill:#bbf,stroke:#333,stroke-width:2px
    style BB fill:#bbf,stroke:#333,stroke-width:2px
    style R fill:#fdb,stroke:#333,stroke-width:1px
    style U fill:#fdb,stroke:#333,stroke-width:1px
    style K fill:#fdb,stroke:#333,stroke-width:1px
```
## Hướng Dẫn Sử Dụng

### Yêu Cầu
- Python 3.8+
- Các thư viện được liệt kê trong `requirements.txt`

### Cài Đặt
```bash
# Clone dự án
git clone https://github.com/username/DS108.git
cd DS108

# Tạo và kích hoạt môi trường ảo
python -m venv venv
source venv/bin/activate  # Trên Windows: venv\Scripts\activate

# Cài đặt các thư viện cần thiết
pip install -r requirements.txt
```

### Thu Thập Dữ Liệu
```bash
# Chạy script thu thập dữ liệu
python src/data_collection/scraper.py

# Hoặc sử dụng Jupyter notebook
jupyter notebook notebooks/data_collection/job_scraping.ipynb
```

### Tiền Xử Lý Dữ Liệu
```bash
# Chạy script tiền xử lý
python src/preprocessing/data_cleaning.py

# Hoặc sử dụng Jupyter notebook
jupyter notebook notebooks/preprocessing/data_preprocessing.ipynb
```

### Phân Tích Dữ Liệu (EDA)
```bash
# Mở notebook phân tích dữ liệu
jupyter notebook EDA.ipynb
```

## Kết Quả
Dự án này cung cấp cái nhìn chi tiết về thị trường việc làm Việt Nam, từ đó giúp:
- Người tìm việc hiểu rõ hơn về cơ hội việc làm và mức lương trong các lĩnh vực
- Nhà tuyển dụng nắm bắt xu hướng thị trường và điều chỉnh chính sách tuyển dụng
- Các nhà hoạch định chính sách hiểu rõ hơn về nhu cầu thị trường lao động

Kết quả chi tiết có thể xem trong thư mục `reports` và các notebooks phân tích.

## Tài Liệu Tham Khảo
- [Python Documentation](https://docs.python.org/3/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Scikit-learn Documentation](https://scikit-learn.org/stable/documentation.html)
- [Beautiful Soup Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [Selenium Documentation](https://selenium-python.readthedocs.io/)

## Giấy Phép
MIT License

© 2025 Đinh Thiên Ân, Huỳnh Trọng Nghĩa
