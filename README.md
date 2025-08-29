# Chương trình Đọc và Phân tích Dữ liệu

Chương trình Python để đọc và hiển thị thông tin dữ liệu từ các file Excel (.xlsx, .xls) và CSV.

## Cấu trúc dự án

```
disease-data/
├── main.py              # File chính chạy chương trình
├── file_reader.py       # Các hàm đọc file Excel và CSV
├── data_display.py      # Các hàm hiển thị và phân tích dữ liệu
├── requirements.txt     # Danh sách thư viện cần thiết
└── README.md           # Hướng dẫn sử dụng
```

## Cài đặt

1. Cài đặt các thư viện cần thiết:
```bash
pip install -r requirements.txt
```

## Sử dụng

1. Chạy chương trình:
```bash
python main.py
```

2. Nhập đường dẫn đến file dữ liệu khi được yêu cầu
3. Chọn các tùy chọn hiển thị từ menu

## Tính năng

### Đọc dữ liệu
- Hỗ trợ file Excel (.xlsx, .xls)
- Hỗ trợ file CSV
- Đọc sheet cụ thể hoặc sheet đầu tiên (cho Excel)

### Hiển thị thông tin
1. **Thông tin cơ bản**: Kích thước, info(), head(), tail(), describe(), null values
2. **Thông tin chi tiết các cột**: Kiểu dữ liệu, số lượng, null, unique values
3. **Tóm tắt dữ liệu**: Tổng quan về dữ liệu và phân loại cột
4. **Mẫu dữ liệu**: Hiển thị số hàng tùy chọn
5. **Tất cả thông tin**: Hiển thị tất cả các thông tin trên

## Ví dụ sử dụng

```
Chương trình đọc và hiển thị dữ liệu
==================================================
Nhập đường dẫn đến file dữ liệu (Excel hoặc CSV): data.xlsx
Nhập tên sheet (hoặc Enter để đọc sheet đầu tiên):

Đang đọc dữ liệu từ file: data.xlsx
Đã đọc thành công 1000 hàng dữ liệu!

==================================================
MENU LỰA CHỌN
==================================================
1. Hiển thị thông tin cơ bản
2. Hiển thị thông tin chi tiết các cột
3. Hiển thị tóm tắt dữ liệu
4. Hiển thị mẫu dữ liệu
5. Hiển thị tất cả thông tin
0. Thoát
==================================================
Nhập lựa chọn của bạn: 1
```

## Thư viện sử dụng

- `pandas`: Xử lý và phân tích dữ liệu
- `openpyxl`: Đọc file Excel (.xlsx)
- `xlrd`: Đọc file Excel (.xls)
- `matplotlib`: Vẽ biểu đồ (cho các tính năng mở rộng)
- `seaborn`: Vẽ biểu đồ thống kê (cho các tính năng mở rộng)
- `numpy`: Tính toán số học
- `jupyter`: Môi trường notebook (tùy chọn)
