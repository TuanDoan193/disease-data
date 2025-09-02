import pandas as pd

# Đọc file Excel gốc
df = pd.read_excel("data/dataa.xlsx")

# Hàm nối chuỗi, bỏ NaN và bỏ trùng lặp
def join_unique(series):
    return "; ".join(sorted(set(str(x) for x in series.dropna() if str(x).strip() != "")))

# Hàm nối chuỗi cho cột TenThuoc - chỉ lấy tên thuốc (phần đầu trước dấu phẩy)
def join_unique_ten_thuoc(series):
    unique_drugs = set()
    for x in series.dropna():
        if str(x).strip() != "":
            # Split theo dấu phẩy và lấy phần đầu tiên (tên thuốc)
            drug_name = str(x).split(',')[0].strip()
            unique_drugs.add(drug_name)
    return "; ".join(sorted(unique_drugs))

# Group theo STT và nối chuỗi cho tất cả cột khác
grouped_concat = df.groupby("STT", as_index=False).agg({
    'TenThuoc': join_unique_ten_thuoc,
    # Các cột khác giữ nguyên hàm join_unique
    **{col: join_unique for col in df.columns if col not in ['STT', 'TenThuoc']}
})

# Giữ đúng thứ tự cột như file gốc
grouped_concat = grouped_concat.reindex(columns=df.columns)

# Xuất ra file Excel mới
grouped_concat.to_excel("Book1_grouped_ten_thuoc.xlsx", index=False)

print("✅ Đã tạo file Book1_grouped_ten_thuoc.xlsx với dữ liệu đã group theo STT")
print("📝 Cột TenThuoc đã được xử lý để chỉ lấy tên thuốc (phần trước dấu phẩy)")
print("🔢 Thứ tự các cột đã được giữ nguyên như file gốc")
