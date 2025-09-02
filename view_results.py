import pandas as pd
from pathlib import Path

def view_detailed_results():
    """
    Hiển thị kết quả chi tiết từ file đã xử lý
    """
    # Đọc file kết quả
    result_file = Path("data/Book2_processed_result.xlsx")

    if not result_file.exists():
        print("Không tìm thấy file kết quả!")
        return

    # Đọc dữ liệu
    df = pd.read_excel(result_file)

    # Các nhóm hoạt chất
    group_columns = ['Giảm đau', 'Opioid', 'Corticoid', 'Acid Hyaluronic', 'Canxi', 'Loãng xương', 'Khác']

    print("=== KẾT QUẢ CHI TIẾT ===\n")

    # Thống kê tổng quan
    print("1. THỐNG KÊ TỔNG QUAN:")
    print(f"- Tổng số records: {len(df)}")
    print(f"- Số records có hoạt chất: {df['Hoạt chất'].notna().sum()}")
    print()

    # Thống kê từng nhóm
    print("2. THỐNG KÊ THEO NHÓM HOẠT CHẤT:")
    for group in group_columns:
        if group in df.columns:
            count = df[group].sum()
            percentage = (count / len(df)) * 100
            print(f"- {group}: {count} records ({percentage:.1f}%)")
    print()

    # Hiển thị các records có hoạt chất được phân loại
    print("3. CÁC RECORDS CÓ HOẠT CHẤT ĐƯỢC PHÂN LOẠI:")

    # Lọc các records có ít nhất 1 nhóm được đánh dấu
    classified_records = df[df[group_columns].sum(axis=1) > 0]

    if len(classified_records) > 0:
        print(f"Tìm thấy {len(classified_records)} records có hoạt chất được phân loại:")
        print()

        for idx, row in classified_records.head(5).iterrows():
            print(f"Record {row.get('STT', idx+1)}:")
            hoat_chat = str(row['Hoạt chất'])[:100] + "..." if len(str(row['Hoạt chất'])) > 100 else str(row['Hoạt chất'])
            print(f"  Hoạt chất: {hoat_chat}")

            # Hiển thị các nhóm được đánh dấu
            marked_groups = []
            for group in group_columns:
                if group in row and row[group] == 1:
                    marked_groups.append(group)

            if marked_groups:
                print(f"  Thuộc nhóm: {', '.join(marked_groups)}")
            print()
    else:
        print("Không tìm thấy records nào có hoạt chất được phân loại.")

    # Hiển thị mapping từ sheet Hoat_Chat
    print("4. MAPPING TỪ SHEET HOẠT CHẤT:")
    try:
        original_file = Path("data/Book2.xlsx")
        hoat_chat_sheet = pd.read_excel(original_file, sheet_name='Hoat_Chat')

        print("Các hoạt chất và nhóm tương ứng:")
        for idx, row in hoat_chat_sheet.iterrows():
            hoat_chat_name = str(row.iloc[0]).strip()
            if pd.isna(hoat_chat_name) or hoat_chat_name == '':
                continue

            groups = []
            for group in group_columns:
                if group in row and pd.notna(row[group]) and row[group] == 1:
                    groups.append(group)

            if groups:
                print(f"  {hoat_chat_name} -> {', '.join(groups)}")

    except Exception as e:
        print(f"Không thể đọc sheet Hoat_Chat: {e}")

if __name__ == "__main__":
    view_detailed_results()
