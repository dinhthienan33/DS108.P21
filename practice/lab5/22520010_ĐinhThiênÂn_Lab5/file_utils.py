"""
Module tiện ích xử lý file
"""
import pandas as pd
import os

def save_results(result_df, output_filename='processed_addresses.csv', output_dir='output'):
    """
    Lưu kết quả ra file CSV
    """
    try:
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, output_filename)
        result_df.to_csv(output_path, index=False, encoding='utf-8')
        print(f"Đã lưu CSV: {output_path}")
        return output_path
    except Exception as e:
        print(f"Lỗi lưu CSV: {e}")
        return None

def export_to_excel(result_df, excel_filename='processed_addresses.xlsx', output_dir='output'):
    """
    Xuất kết quả ra file Excel
    """
    try:
        os.makedirs(output_dir, exist_ok=True)
        excel_path = os.path.join(output_dir, excel_filename)
        
        with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
            result_df.to_excel(writer, sheet_name='Processed_Addresses', index=False)
        
        print(f"Đã lưu Excel: {excel_path}")
        return excel_path
    except Exception as e:
        print(f"Lỗi lưu Excel: {e}")
        return None 