"""
Module cấu hình cho ứng dụng xử lý địa chỉ
"""
import os

class Config:
    """Class chứa các cấu hình chung"""
    
    # Đường dẫn file
    DATA_DIR = 'data'
    OUTPUT_DIR = 'output'
    BACKUP_DIR = 'backup'
    
    INPUT_FILE = 'address_full_0712.xlsx'
    SAMPLE_FILE = 'D_data_address - D_data_address.csv'
    
    # Tên file output mặc định
    DEFAULT_OUTPUT_CSV = 'processed_addresses.csv'
    DEFAULT_OUTPUT_EXCEL = 'processed_addresses.xlsx'
    DEFAULT_STATS_FILE = 'processing_stats.txt'
    
    # Cấu hình xử lý
    BATCH_SIZE = 100  # Kích thước batch để in tiến trình
    MAX_TSV_WORDS = 15  # Số từ tối đa trong TSV
    
    # ID offset
    ID_OFFSET = 1000000
    
    # Country ID mặc định (Việt Nam)
    DEFAULT_COUNTRY_ID = 1

class AddressPatterns:
    """Class chứa các pattern regex để nhận diện địa chỉ"""
    
    STREET_PATTERNS = [
        r'đường\s+([^,]+)',
        r'phố\s+([^,]+)',
        r'ngõ\s+([^,]+)',
        r'hẻm\s+([^,]+)',
        r'đ\.\s*([^,]+)',  # Viết tắt "Đ."
        r'đ\s+([^,]+)'     # Viết tắt "Đ "
    ]
    
    WARD_PATTERNS = [
        r'phường\s+([^,]+)',
        r'xã\s+([^,]+)',
        r'thị\s+trấn\s+([^,]+)',
        r'p\.\s*([^,]+)',   # Viết tắt "P."
        r'p\s+([^,]+)',     # Viết tắt "P "
        r'tt\.\s*([^,]+)',  # Viết tắt "TT."
        r'tt\s+([^,]+)'     # Viết tắt "TT "
    ]
    
    DISTRICT_PATTERNS = [
        r'quận\s+([^,\d]*\d*[^,]*)',
        r'huyện\s+([^,]+)',
        r'thị\s+xã\s+([^,]+)',
        r'thành\s+phố\s+([^,]+)',
        r'q\.\s*([^,]+)',   # Viết tắt "Q."
        r'q\s+([^,]+)',     # Viết tắt "Q "
        r'h\.\s*([^,]+)',   # Viết tắt "H."
        r'h\s+([^,]+)',     # Viết tắt "H "
        r'tx\.\s*([^,]+)',  # Viết tắt "TX."
        r'tx\s+([^,]+)',    # Viết tắt "TX "
        r'tp\.\s*([^,]+)',  # Viết tắt "TP."
        r'tp\s+([^,]+)'     # Viết tắt "TP "
    ]
    
    CITY_PATTERNS = [
        r'tỉnh\s+([^,]+)',
        r'thành\s+phố\s+([^,]+)',
        r'tp\.\s*([^,]+)',  # Viết tắt "TP."
        r'tp\s+([^,]+)'     # Viết tắt "TP "
    ]

class CleaningRules:
    """Class chứa các quy tắc làm sạch dữ liệu"""
    
    # Các từ cần loại bỏ
    REMOVE_WORDS = [
        'tại', 'ở', 'địa chỉ:', 'address:', 'add:', 'addr:',
        'dc:', 'dia chi:', 'diachi:', 'location:', 'loc:'
    ]
    
    # Các từ viết tắt cần chuẩn hóa
    ABBREVIATION_MAP = {
        'đ.': 'đường',
        'đ ': 'đường ',
        'p.': 'phường',
        'p ': 'phường ',
        'q.': 'quận',
        'q ': 'quận ',
        'h.': 'huyện',
        'h ': 'huyện ',
        'tx.': 'thị xã',
        'tx ': 'thị xã ',
        'tp.': 'thành phố',
        'tp ': 'thành phố ',
        'tt.': 'thị trấn',
        'tt ': 'thị trấn ',
        'xa.': 'xã',
        'xa ': 'xã '
    }
    
    # Ký tự đặc biệt cần loại bỏ (giữ lại dấu phẩy)
    SPECIAL_CHARS_PATTERN = r'[^\w\s,àáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ]'

class DatabaseConfig:
    """Class cấu hình database (nếu cần)"""
    
    # Mock IDs cho các tỉnh/thành phố
    PROVINCE_IDS = {
        'hồ chí minh': 1,
        'hà nội': 2,
        'bình dương': 3,
        'đà nẵng': 4,
        'an giang': 8,
        'cần thơ': 18,
        'vĩnh long': 58,
        'tiền giang': 58,
        'long an': 6
    }
    
    # Mock IDs cho các quận/huyện
    DISTRICT_IDS = {
        'quận 1': 1,
        'quận 2': 14,
        'quận 3': 15,
        'quận 4': 16,
        'quận 5': 20,
        'quận 6': 21,
        'quận 7': 22,
        'huyện củ chi': 5,
        'quận ba đình': 25,
        'quận hoàn kiếm': 37
    }

def get_file_paths():
    """
    Trả về các đường dẫn file được cấu hình
    
    Returns:
        dict: Dictionary chứa các đường dẫn file
    """
    return {
        'input_file': os.path.join(Config.DATA_DIR, Config.INPUT_FILE),
        'sample_file': os.path.join(Config.DATA_DIR, Config.SAMPLE_FILE),
        'output_csv': os.path.join(Config.OUTPUT_DIR, Config.DEFAULT_OUTPUT_CSV),
        'output_excel': os.path.join(Config.OUTPUT_DIR, Config.DEFAULT_OUTPUT_EXCEL),
        'stats_file': os.path.join(Config.OUTPUT_DIR, Config.DEFAULT_STATS_FILE)
    }

def validate_config():
    """
    Kiểm tra tính hợp lệ của cấu hình
    
    Returns:
        bool: True nếu cấu hình hợp lệ
    """
    paths = get_file_paths()
    
    # Kiểm tra file đầu vào có tồn tại không
    if not os.path.exists(paths['input_file']):
        print(f"Lỗi: Không tìm thấy file đầu vào: {paths['input_file']}")
        return False
    
    if not os.path.exists(paths['sample_file']):
        print(f"Lỗi: Không tìm thấy file mẫu: {paths['sample_file']}")
        return False
    
    # Tạo thư mục output nếu chưa có
    os.makedirs(Config.OUTPUT_DIR, exist_ok=True)
    os.makedirs(Config.BACKUP_DIR, exist_ok=True)
    
    return True 