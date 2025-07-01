"""
Module tải dữ liệu
"""
import pandas as pd

def load_and_process_address_data():
    """
    Tải dữ liệu từ file Excel và file mẫu
    """
    
    try:
        df_input = pd.read_excel('data/address_full_0712.xlsx')
        print(f"Đã tải {len(df_input)} dòng dữ liệu")
    except Exception as e:
        print(f"Lỗi đọc file Excel: {e}")
        return None
    
    try:
        df_sample = pd.read_csv('data/D_data_address - D_data_address.csv')
    except Exception as e:
        print(f"Lỗi đọc file mẫu: {e}")
        return None
    
    return df_input, df_sample

def find_address_column(df):
    """
    Tìm cột chứa địa chỉ
    """
    address_keywords = ['address', 'địa chỉ', 'diachi', 'addr']
    
    for col in df.columns:
        for keyword in address_keywords:
            if keyword in col.lower():
                return col
    
    return df.columns[0] 