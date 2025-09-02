import pandas as pd
from pathlib import Path

def view_final_results():
    """
    Hiển thị kết quả cuối cùng chi tiết
    """
    print("=== KẾT QUẢ CUỐI CÙNG ===\n")

    # Đọc file kết quả
    result_file = Path("Book2_processed_result.xlsx")

    if not result_file.exists():
        print("Không tìm thấy file kết quả!")
        return

    # Đọc dữ liệu
    df = pd.read_excel(result_file)

    # Các nhóm hoạt chất
    group_columns = ['NSAIDs', 'Giảm đau', 'Opioid', 'Corticoid', 'Acid Hyaluronic', 'Canxi', 'Loãng xương', 'Khác']

    print("1. THỐNG KÊ TỔNG QUAN:")
    print(f"- Tổng số records: {len(df)}")
    print(f"- Số records có hoạt chất: {df['Hoạt chất'].notna().sum()}")
    print()

    # Thống kê từng nhóm
    print("2. THỐNG KÊ THEO NHÓM HOẠT CHẤT:")
    total_records = len(df)
    for group in group_columns:
        if group in df.columns:
            count = df[group].sum()
            percentage = (count / total_records) * 100
            print(f"- {group}: {count} records ({percentage:.1f}%)")
    print()

    # Hiển thị mapping từ sheet Hoat_Chat
    print("3. MAPPING TỪ SHEET HOẠT CHẤT:")
    try:
        original_file = Path("data/Book2.xlsx")
        hoat_chat_sheet = pd.read_excel(original_file, sheet_name='Hoat_Chat')

        for group in group_columns:
            if group in hoat_chat_sheet.columns:
                print(f"\n{group}:")
                hoat_chat_list = []
                for value in hoat_chat_sheet[group].dropna():
                    if pd.notna(value) and str(value).strip() != '':
                        hoat_chats = [x.strip() for x in str(value).split(';') if x.strip()]
                        hoat_chat_list.extend(hoat_chats)

                # Hiển thị tối đa 10 hoạt chất đầu tiên
                for i, hoat_chat in enumerate(hoat_chat_list[:10]):
                    print(f"  {i+1}. {hoat_chat}")

                if len(hoat_chat_list) > 10:
                    print(f"  ... và {len(hoat_chat_list) - 10} hoạt chất khác")

    except Exception as e:
        print(f"Không thể đọc sheet Hoat_Chat: {e}")

    print()

    # Hiển thị một vài ví dụ kết quả
    print("4. VÍ DỤ KẾT QUẢ:")
    classified_records = df[df[group_columns].sum(axis=1) > 0]

    if len(classified_records) > 0:
        for idx, row in classified_records.head(3).iterrows():
            print(f"\nRecord {row.get('STT', idx+1)}:")
            hoat_chat = str(row['Hoạt chất'])[:100] + "..." if len(str(row['Hoạt chất'])) > 100 else str(row['Hoạt chất'])
            print(f"  Hoạt chất: {hoat_chat}")

            # Hiển thị các nhóm được đánh dấu
            marked_groups = []
            for group in group_columns:
                if group in row and row[group] == 1:
                    marked_groups.append(group)

            if marked_groups:
                print(f"  Thuộc nhóm: {', '.join(marked_groups)}")

    print("\n5. PHÂN TÍCH CHI TIẾT:")
    print("Các nhóm có tỷ lệ cao nhất:")
    group_stats = []
    for group in group_columns:
        if group in df.columns:
            count = df[group].sum()
            percentage = (count / total_records) * 100
            group_stats.append((group, count, percentage))

    # Sắp xếp theo tỷ lệ giảm dần
    group_stats.sort(key=lambda x: x[2], reverse=True)

    for group, count, percentage in group_stats:
        print(f"  {group}: {count} records ({percentage:.1f}%)")

if __name__ == "__main__":
    view_final_results()
