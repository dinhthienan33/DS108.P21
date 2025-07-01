"""
Module xử lý và chuẩn hóa địa chỉ - phiên bản tối ưu
"""
import pandas as pd
import re
from config import DatabaseConfig

def smart_address_parser(address_text):
    """
    Parser thông minh cho địa chỉ Việt Nam
    """
    
    if pd.isna(address_text) or not str(address_text).strip():
        return {}
    
    text = str(address_text).lower().strip()
    
    result = {
        'street': None,
        'ward': None,
        'district': None,
        'city': None,
        'street_id': None,
        'ward_id': None,
        'district_id': None,
        'city_id': None
    }
    
    # Case 1: "215 nguyễn thị thập phường tân phú quận 7"
    pattern1 = r'^(\d+[a-z]?\s+[^,]+?)\s+phường\s+([^,]+?)\s+quận\s+(.+)$'
    match1 = re.match(pattern1, text)
    if match1:
        result['street'] = match1.group(1).strip()
        result['ward'] = match1.group(2).strip()
        district = match1.group(3).strip()
        result['district'] = f"quận {district}" if district.isdigit() else district
        
        if result['district'] in DatabaseConfig.DISTRICT_IDS:
            result['district_id'] = DatabaseConfig.DISTRICT_IDS[result['district']]
        
        return result
    
    # Case 2: "mt cộng hòa" - mặt tiền
    pattern2 = r'^mt\s+(.+)$'
    match2 = re.match(pattern2, text)
    if match2:
        result['street'] = f"mặt tiền {match2.group(1).strip()}"
        return result
    
    # Case 3: "5.16 tòa c2 chung cư ecohome 2" - chung cư
    pattern3 = r'^(\d+\.\d+)\s+(.+)$'
    match3 = re.match(pattern3, text)
    if match3:
        apartment = match3.group(1)
        building_info = match3.group(2)
        result['street'] = f"căn {apartment}, {building_info}"
        return result
    
    # Case 4: "đường quốc lộ 1a , tân tạo bình tân"
    pattern4 = r'^đường\s+([^,]+)\s*,\s*(.+)$'
    match4 = re.match(pattern4, text)
    if match4:
        result['street'] = match4.group(1).strip()
        remaining = match4.group(2).strip()
        
        if 'bình tân' in remaining:
            if 'tân tạo' in remaining:
                result['ward'] = 'tân tạo'
                result['district'] = 'bình tân'
        
        return result
    
    # Fallback: pattern matching chuẩn
    return standard_pattern_matching(text)

def standard_pattern_matching(text):
    """
    Pattern matching chuẩn
    """
    
    result = {
        'street': None,
        'ward': None,
        'district': None,
        'city': None,
        'street_id': None,
        'ward_id': None,
        'district_id': None,
        'city_id': None
    }
    
    patterns = {
        'district': [
            (r'\bquận\s+(\d+)\b', 'quận {}'),
            (r'\bquận\s+([^,\s]+)', '{}'),
            (r'\bhuyện\s+([^,]+)', '{}'),
        ],
        'ward': [
            (r'\bphường\s+([^,]+?)(?=\s*quận|\s*huyện|$)', '{}'),
            (r'\bxã\s+([^,]+?)(?=\s*huyện|$)', '{}'),
        ],
        'street': [
            (r'\bđường\s+([^,]+)', '{}'),
            (r'\bphố\s+([^,]+)', '{}'),
        ],
        'city': [
            (r'\bthành\s+phố\s+([^,]+)', '{}'),
            (r'\btỉnh\s+([^,]+)', '{}'),
        ]
    }
    
    working_text = text
    
    for component_type in ['district', 'ward', 'street', 'city']:
        for pattern, format_str in patterns[component_type]:
            match = re.search(pattern, working_text)
            if match:
                extracted = match.group(1).strip()
                
                if component_type == 'district' and extracted.isdigit():
                    result[component_type] = format_str.format(extracted)
                else:
                    result[component_type] = extracted
                
                # Map IDs
                if component_type == 'district':
                    district_key = result[component_type]
                    if district_key in DatabaseConfig.DISTRICT_IDS:
                        result['district_id'] = DatabaseConfig.DISTRICT_IDS[district_key]
                elif component_type == 'city':
                    city_key = result[component_type].lower()
                    if city_key in DatabaseConfig.PROVINCE_IDS:
                        result['city_id'] = DatabaseConfig.PROVINCE_IDS[city_key]
                
                working_text = re.sub(pattern, '', working_text).strip()
                break
    
    return result

def process_single_address(address_text, record_id):
    """
    Xử lý địa chỉ đơn lẻ
    """
    
    parsed = smart_address_parser(address_text)
    
    # Tạo full_address chuẩn hóa
    address_parts = []
    
    if parsed.get('street'):
        street = parsed['street']
        if not any(prefix in street.lower() for prefix in ['đường', 'phố', 'mt', 'mặt tiền', 'căn']):
            address_parts.append(f"Đường {street}")
        else:
            address_parts.append(street.title())
    
    if parsed.get('ward'):
        ward = parsed['ward']
        if not any(prefix in ward.lower() for prefix in ['phường', 'xã']):
            address_parts.append(f"Phường {ward}")
        else:
            address_parts.append(ward.title())
    
    if parsed.get('district'):
        address_parts.append(parsed['district'].title())
    
    if parsed.get('city'):
        city = parsed['city']
        if not any(prefix in city.lower() for prefix in ['tỉnh', 'thành phố']):
            address_parts.append(f"Thành phố {city}")
        else:
            address_parts.append(city.title())
    
    full_address = ', '.join(address_parts) if address_parts else str(address_text)
    
    # Tạo TSV
    tsv = create_tsv(address_text)
    
    return {
        'id': record_id + 1000000,
        'street_id': parsed.get('street_id'),
        'ward_id': parsed.get('ward_id'),
        'district_id': parsed.get('district_id'),
        'city_id': parsed.get('city_id'),
        'country_id': 1,
        'full_address': full_address,
        'created_at': pd.Timestamp.now(),
        'updated_at': pd.Timestamp.now(),
        'tsv': tsv
    }

def create_tsv(address_text):
    """
    Tạo TSV (Text Search Vector)
    """
    if pd.isna(address_text):
        return ""
    
    text = str(address_text).lower()
    text = re.sub(r'[^\w\sàáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ]', ' ', text)
    
    words = [w for w in text.split() if len(w) > 1][:15]
    
    tsv_parts = []
    for i, word in enumerate(words):
        tsv_parts.append(f"'{word}':{i+1}A")
    
    return ' '.join(tsv_parts)

def create_standardized_address_data(df_input, df_sample):
    """
    Tạo dữ liệu địa chỉ chuẩn hóa
    """
    
    from data_loader import find_address_column
    
    processed_data = []
    address_column = find_address_column(df_input)
    
    for idx, row in df_input.iterrows():
        address_text = str(row[address_column])
        processed_address = process_single_address(address_text, idx)
        processed_data.append(processed_address)
        
        if idx % 100 == 0 and idx > 0:
            print(f"Đã xử lý {idx} dòng...")
    
    return pd.DataFrame(processed_data) 