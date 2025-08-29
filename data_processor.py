import pandas as pd
import os
from file_reader import read_excel_file

class DataProcessor:
    def __init__(self, file_path="data/Book1.xlsx"):
        """
        Khởi tạo DataProcessor

        Args:
            file_path (str): Đường dẫn đến file Excel
        """
        self.file_path = file_path
        self.df = None
        self.load_data()

    def load_data(self):
        """Đọc dữ liệu từ file Excel"""
        if not os.path.exists(self.file_path):
            print(f"Không tìm thấy file: {self.file_path}")
            return False

        self.df = read_excel_file(self.file_path)
        if self.df is not None:
            print(f"Đã tải dữ liệu thành công: {self.df.shape[0]} hàng, {self.df.shape[1]} cột")
            return True
        else:
            print("Không thể đọc dữ liệu từ file Excel")
            return False

    # TODO: Thêm các chức năng xử lý dữ liệu của bạn ở đây
    # Ví dụ:
    # def your_custom_function(self):
    #     """Mô tả chức năng của bạn"""
    #     pass
