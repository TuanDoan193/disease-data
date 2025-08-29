# Script Phân tích Dữ liệu Bệnh nhân

## Cài đặt

```bash
pip install -r requirements.txt
```

## Cách sử dụng

### 1. Script đọc dữ liệu cơ bản (`simple_reader.py`)

Hiển thị thông tin cơ bản về dữ liệu:

```bash
python simple_reader.py <đường_dẫn_file>
```

**Ví dụ:**
```bash
python simple_reader.py Book1.xlsx
python simple_reader.py data.csv
```

### 2. Script phân tích chi tiết (`disease_analyzer.py`)

Phân tích chi tiết dữ liệu bệnh nhân và tạo báo cáo:

```bash
python disease_analyzer.py <đường_dẫn_file>
```

**Ví dụ:**
```bash
python disease_analyzer.py Book1.xlsx
```

## Kết quả phân tích

Script `disease_analyzer.py` sẽ hiển thị:

1. **Thống kê cơ bản**: Số lượng bệnh nhân, số cột dữ liệu
2. **Phân tích tuổi**: Tuổi trung bình, phân bố theo nhóm tuổi
3. **Phân tích giới tính**: Tỷ lệ nam/nữ
4. **Phân tích theo khoa**: Top 10 khoa có nhiều bệnh nhân nhất
5. **Top 10 chẩn đoán**: Các chẩn đoán phổ biến nhất
6. **Top 10 thuốc**: Thuốc được kê nhiều nhất
7. **Phân tích chi phí**: Chi phí trung bình, tổng chi phí
8. **Phân tích tương tác thuốc**: Số lượng tương tác thuốc
9. **Phân tích bệnh kèm**: Tỷ lệ các bệnh kèm theo
10. **Phân tích dữ liệu thiếu**: Các cột có dữ liệu thiếu

## File đầu ra

- Script sẽ tự động tạo file báo cáo: `bao_cao_phan_tich_<tên_file>.txt`
- Báo cáo chứa toàn bộ kết quả phân tích để lưu trữ

## Định dạng file hỗ trợ

- Excel: `.xlsx`, `.xls`
- CSV: `.csv`
