"""
File chính để chạy ứng dụng xử lý địa chỉ
"""
import time
from datetime import datetime

from data_loader import load_and_process_address_data
from address_processor import create_standardized_address_data
from file_utils import save_results, export_to_excel
from config import validate_config

def main():
    """
    Hàm chính thực hiện xử lý
    """
    start_time = time.time()
    
    try:
        print(f"Bắt đầu xử lý: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Kiểm tra cấu hình
        if not validate_config():
            print("❌ Lỗi cấu hình")
            return False
        
        # Tải dữ liệu
        data_result = load_and_process_address_data()
        if data_result is None:
            print("❌ Lỗi tải dữ liệu")
            return False
        
        df_input, df_sample = data_result
        
        # Xử lý dữ liệu
        result_df = create_standardized_address_data(df_input, df_sample)
        if result_df is None:
            print("❌ Lỗi xử lý dữ liệu")
            return False
        
        # Lưu kết quả
        save_results(result_df)
        export_to_excel(result_df)
        
        # Tính thời gian
        end_time = time.time()
        duration = end_time - start_time
        
        print(f" Hoàn thành: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Thời gian xử lý: {duration:.2f} giây")
        print(f"Đã xử lý {len(result_df)} dòng dữ liệu")
        
        return True
        
    except Exception as e:
        end_time = time.time()
        duration = end_time - start_time
        
        print(f"Lỗi: {str(e)}")
        print(f" Thời gian chạy: {duration:.2f} giây")
        return False

if __name__ == "__main__":
    main() 