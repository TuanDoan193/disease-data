import pandas as pd

def read_excel_file(file_path, sheet_name=0):
    """
    Đọc file Excel và trả về DataFrame

    Args:
        file_path (str): Đường dẫn đến file Excel
        sheet_name (str/int): Tên sheet hoặc index sheet (mặc định là 0 - sheet đầu tiên)

    Returns:
        pandas.DataFrame: DataFrame chứa dữ liệu từ file Excel
        None: Nếu có lỗi khi đọc file
    """
    try:
        if sheet_name == 0:
            # Đọc sheet đầu tiên
            df = pd.read_excel(file_path)
        else:
            # Đọc sheet cụ thể
            df = pd.read_excel(file_path, sheet_name=sheet_name)

        # Kiểm tra nếu df là dictionary (có nhiều sheet)
        if isinstance(df, dict):
            # Lấy sheet đầu tiên nếu không chỉ định sheet cụ thể
            if sheet_name == 0:
                first_sheet = list(df.keys())[0]
                df = df[first_sheet]
                print(f"Đã tự động chọn sheet: {first_sheet}")
            else:
                print(f"Không tìm thấy sheet: {sheet_name}")
                print(f"Các sheet có sẵn: {list(df.keys())}")
                return None

        return df
    except Exception as e:
        print(f"Lỗi khi đọc file Excel: {e}")
        return None

def read_csv_file(file_path):
    """
    Đọc file CSV và trả về DataFrame

    Args:
        file_path (str): Đường dẫn đến file CSV

    Returns:
        pandas.DataFrame: DataFrame chứa dữ liệu từ file CSV
        None: Nếu có lỗi khi đọc file
    """
    try:
        df = pd.read_csv(file_path)
        return df
    except Exception as e:
        print(f"Lỗi khi đọc file CSV: {e}")
        return None

def get_file_extension(file_path):
    """
    Lấy phần mở rộng của file

    Args:
        file_path (str): Đường dẫn đến file

    Returns:
        str: Phần mở rộng của file (không bao gồm dấu chấm)
    """
    return file_path.lower().split('.')[-1]

def is_supported_file(file_path):
    """
    Kiểm tra xem file có được hỗ trợ không

    Args:
        file_path (str): Đường dẫn đến file

    Returns:
        bool: True nếu file được hỗ trợ, False nếu không
    """
    supported_extensions = ['xlsx', 'xls', 'csv']
    extension = get_file_extension(file_path)
    return extension in supported_extensions

def list_excel_sheets(file_path):
    """
    Liệt kê tất cả các sheet trong file Excel

    Args:
        file_path (str): Đường dẫn đến file Excel

    Returns:
        list: Danh sách tên các sheet
    """
    try:
        excel_file = pd.ExcelFile(file_path)
        return excel_file.sheet_names
    except Exception as e:
        print(f"Lỗi khi đọc danh sách sheet: {e}")
        return []
