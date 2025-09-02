import pandas as pd
from pathlib import Path

def check_mapping():
    """
    Kiểm tra mapping và kết quả
    """
    print("=== KIỂM TRA MAPPING VÀ KẾT QUẢ ===\n")

    # Đọc file gốc để xem sheet Hoat_Chat
    original_file = Path("data/Book2.xlsx")
    hoat_chat_sheet = pd.read_excel(original_file, sheet_name='Hoat_Chat')

    print("1. SHEET HOẠT CHẤT:")
    print(f"Số dòng: {len(hoat_chat_sheet)}")
    print(f"Các cột: {hoat_chat_sheet.columns.tolist()}")
    print()

    # Hiển thị các hoạt chất và nhóm tương ứng
    print("2. MAPPING HOẠT CHẤT -> NHÓM:")
    group_columns = ['Giảm đau', 'Opioid', 'Corticoid', 'Acid Hyaluronic', 'Canxi', 'Loãng xương', 'Khác']

    mapping_count = 0
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
            mapping_count += 1

    print(f"Tổng số mapping: {mapping_count}")

    print()

    # Đọc kết quả đã xử lý
    result_file = Path("data/Book2_processed_result.xlsx")
    if result_file.exists():
        df = pd.read_excel(result_file)

        print("3. KẾT QUẢ XỬ LÝ:")
        print(f"Tổng records: {len(df)}")

        # Thống kê từng nhóm
        for group in group_columns:
            if group in df.columns:
                count = df[group].sum()
                print(f"  {group}: {count} records")

        print()

        # Hiển thị một vài ví dụ
        print("4. VÍ DỤ KẾT QUẢ:")
        classified_records = df[df[group_columns].sum(axis=1) > 0]

        if len(classified_records) > 0:
            for idx, row in classified_records.head(3).iterrows():
                print(f"Record {idx+1}:")
                hoat_chat = str(row['Hoạt chất'])[:80] + "..." if len(str(row['Hoạt chất'])) > 80 else str(row['Hoạt chất'])
                print(f"  Hoạt chất: {hoat_chat}")

                marked_groups = []
                for group in group_columns:
                    if group in row and row[group] == 1:
                        marked_groups.append(group)

                if marked_groups:
                    print(f"  Nhóm: {', '.join(marked_groups)}")
                print()

if __name__ == "__main__":
    check_mapping()
