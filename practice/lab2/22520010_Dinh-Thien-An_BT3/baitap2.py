import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np
import json

def baitap2():
    # URL API với mã bưu điện TP.HCM (70000)
    api_url = "https://samples.openweathermap.org/data/2.5/forecast/hourly?zip=70000&appid=b6907d289e10d714a6e88b30761fae22"
    
    print("Đang lấy dữ liệu thời tiết cho TP.HCM (Mã ZIP: 70000)...")
    
    try:
        # Gửi yêu cầu GET tới API với header hợp lệ
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, như Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()  # Gây lỗi nếu có lỗi HTTP
        
        # Phân tích dữ liệu JSON nhận được
        try:
            data = response.json()
        except json.JSONDecodeError:
            print("Lỗi: Không thể phân tích phản hồi JSON. Có thể API đã thay đổi.")
            return None
        
        # Kiểm tra xem API có trả dữ liệu hợp lệ không
        if 'list' not in data:
            print("Lỗi: Không thể lấy dữ liệu dự báo. Phản hồi API có thể đã thay đổi cấu trúc.")
            print("Phản hồi từ API:", data)
            return None
        
        if len(data['list']) == 0:
            print("Cảnh báo: API trả về danh sách dữ liệu rỗng.")
            return None
        
        # Trích xuất dữ liệu dự báo
        forecast_data = data['list']
        
        # Tạo DataFrame
        df = pd.DataFrame(forecast_data)
        
        # Chuyển đổi timestamp thành định dạng ngày giờ
        df['datetime'] = df['dt'].apply(lambda x: datetime.fromtimestamp(x))
        
        try:
            df['pressure'] = df['main'].apply(lambda x: x.get('pressure', 0))
            df['wind_speed'] = df['wind'].apply(lambda x: x.get('speed', 0))
            df['temp'] = df['main'].apply(lambda x: x.get('temp', 273.15) - 273.15)  # Chuyển từ Kelvin sang Celsius
            df['humidity'] = df['main'].apply(lambda x: x.get('humidity', 0))
        except KeyError as e:
            print(f"Lỗi khi trích xuất dữ liệu: {e}. Có thể cấu trúc API đã thay đổi.")
        
        # Nhóm theo ngày để trực quan hóa
        df['date'] = df['datetime'].dt.date
        agg_columns = {}
        for col in ['pressure', 'wind_speed', 'temp', 'humidity']:
            if col in df.columns:
                agg_columns[col] = 'mean'
        
        if not agg_columns:
            print("Lỗi: Không thể trích xuất bất kỳ cột dữ liệu nào.")
            return None
        
        daily_data = df.groupby('date').agg(agg_columns).reset_index()
        
        # Chuyển đổi ngày thành chuỗi để hiển thị dễ hơn trong biểu đồ
        daily_data['date_str'] = daily_data['date'].astype(str)
        
        print("\nTóm tắt dữ liệu thời tiết của TP.HCM (ZIP: 70000):")
        print(daily_data)
        
        # a) Vẽ biểu đồ áp suất không khí theo ngày
        if 'pressure' in daily_data.columns:
            plt.figure(figsize=(12, 6))
            plt.plot(daily_data['date_str'], daily_data['pressure'], marker='o', linestyle='-', linewidth=2)
            plt.title('Áp suất không khí trung bình theo ngày (TP.HCM)', fontsize=14)
            plt.ylabel('Áp suất (hPa)', fontsize=12)
            plt.xlabel('Ngày', fontsize=12)
            plt.grid(True, linestyle='--', alpha=0.7)
            plt.xticks(rotation=45)
            
            # Thêm nhãn giá trị phía trên mỗi điểm
            for i, p in enumerate(daily_data['pressure']):
                plt.annotate(f'{p:.1f}', 
                            (daily_data['date_str'][i], p),
                            textcoords="offset points", 
                            xytext=(0,10), 
                            ha='center')
            
            plt.tight_layout()
            plt.savefig('hcmc_pressure.png')
            print("Đã lưu biểu đồ áp suất vào 'hcmc_pressure.png'")
        else:
            print("Không thể tạo biểu đồ áp suất: không có dữ liệu áp suất")
        
        # b) Vẽ biểu đồ tốc độ gió theo ngày
        if 'wind_speed' in daily_data.columns:
            plt.figure(figsize=(12, 6))
            plt.plot(daily_data['date_str'], daily_data['wind_speed'], marker='o', linestyle='-', linewidth=2, color='green')
            plt.title('Tốc độ gió trung bình theo ngày (TP.HCM)', fontsize=14)
            plt.ylabel('Tốc độ gió (m/s)', fontsize=12)
            plt.xlabel('Ngày', fontsize=12)
            plt.grid(True, linestyle='--', alpha=0.7)
            plt.xticks(rotation=45)
            
            # Thêm nhãn giá trị phía trên mỗi điểm
            for i, w in enumerate(daily_data['wind_speed']):
                plt.annotate(f'{w:.1f}', 
                            (daily_data['date_str'][i], w),
                            textcoords="offset points", 
                            xytext=(0,10), 
                            ha='center')
            
            plt.tight_layout()
            plt.savefig('hcmc_wind_speed.png')
            print("Đã lưu biểu đồ tốc độ gió vào 'hcmc_wind_speed.png'")
        else:
            print("Không thể tạo biểu đồ tốc độ gió: không có dữ liệu tốc độ gió")
        
        # Phân tích bổ sung - nhiệt độ và độ ẩm
        if 'temp' in daily_data.columns and 'humidity' in daily_data.columns:
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
            
            # Biểu đồ nhiệt độ
            ax1.plot(daily_data['date_str'], daily_data['temp'], marker='o', linestyle='-', color='red', linewidth=2)
            ax1.set_title('Nhiệt độ trung bình theo ngày (TP.HCM)', fontsize=14)
            ax1.set_ylabel('Nhiệt độ (°C)', fontsize=12)
            ax1.grid(True, linestyle='--', alpha=0.7)
            ax1.tick_params(axis='x', rotation=45)
            
            # Biểu đồ độ ẩm
            ax2.plot(daily_data['date_str'], daily_data['humidity'], marker='o', linestyle='-', color='blue', linewidth=2)
            ax2.set_title('Độ ẩm trung bình theo ngày (TP.HCM)', fontsize=14)
            ax2.set_ylabel('Độ ẩm (%)', fontsize=12)
            ax2.set_xlabel('Ngày', fontsize=12)
            ax2.grid(True, linestyle='--', alpha=0.7)
            ax2.tick_params(axis='x', rotation=45)
            
            plt.tight_layout()
            plt.savefig('hcmc_temp_humidity.png')
            print("Đã lưu biểu đồ nhiệt độ và độ ẩm vào 'hcmc_temp_humidity.png'")
        
        return df
    
    except requests.exceptions.RequestException as e:
        print(f"Lỗi: Không thể kết nối đến API: {e}")
        print("Dịch vụ API có thể đang bị gián đoạn hoặc URL đã thay đổi.")
        print("Vui lòng kiểm tra xem API mẫu còn hoạt động tại:", api_url)
        return None
    except Exception as e:
        print(f"Lỗi không xác định: {e}")
        return None

if __name__ == "__main__":
    baitap2()
