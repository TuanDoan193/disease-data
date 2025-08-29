#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Main application file for Disease Data Analysis
Tệp chính để chạy ứng dụng phân tích dữ liệu bệnh
"""

import sys
import os
from data_processor import DataProcessor

def print_menu():
    """In menu chính"""
    print("\n" + "="*60)
    print("🏥 PHÂN TÍCH DỮ LIỆU BỆNH VIỆN")
    print("="*60)
    print("1. Chức năng 1")
    print("2. Chức năng 2")
    print("3. Chức năng 3")
    print("0. Thoát")
    print("="*60)

def main():
    """Hàm chính"""
    print("🚀 Khởi động ứng dụng phân tích dữ liệu bệnh viện...")

    # Khởi tạo processor
    processor = DataProcessor()

    if processor.df is None:
        print("❌ Không thể tải dữ liệu. Vui lòng kiểm tra file Excel!")
        return

    print("✅ Đã tải dữ liệu thành công!")

    # Vòng lặp chính
    while True:
        print_menu()

        try:
            choice = input("\nChọn chức năng (0-3): ").strip()

            if choice == '0':
                print("👋 Tạm biệt!")
                break
            elif choice == '1':
                print("Chức năng 1 - TODO: Thêm logic của bạn")
                # TODO: Thêm logic chức năng 1
            elif choice == '2':
                print("Chức năng 2 - TODO: Thêm logic của bạn")
                # TODO: Thêm logic chức năng 2
            elif choice == '3':
                print("Chức năng 3 - TODO: Thêm logic của bạn")
                # TODO: Thêm logic chức năng 3
            else:
                print("❌ Lựa chọn không hợp lệ! Vui lòng chọn từ 0-3.")

        except KeyboardInterrupt:
            print("\n👋 Tạm biệt!")
            break
        except Exception as e:
            print(f"❌ Có lỗi xảy ra: {e}")

        input("\nNhấn Enter để tiếp tục...")

if __name__ == "__main__":
    main()
