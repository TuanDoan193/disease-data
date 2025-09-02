#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Main application file for Disease Data Analysis
Tệp chính để chạy ứng dụng phân tích dữ liệu bệnh
"""

import sys
import os
from data_processor import DataProcessor

def main():
    """Hàm chính"""
    print("🚀 Khởi động ứng dụng phân tích dữ liệu bệnh viện...")

    # Khởi tạo processor
    processor = DataProcessor()

    if processor.df is None:
        print("❌ Không thể tải dữ liệu. Vui lòng kiểm tra file Excel!")
        return



if __name__ == "__main__":
    main()
