import pandas as pd
from pathlib import Path

def check_results_v3():
    """
    Kiểm tra kết quả v3 với việc ghi tên hoạt chất cho nhóm "khác"
    """
    print("=== KIỂM TRA KẾT QUẢ V3 (NHÓM 'KHÁC' GHI TÊN HOẠT CHẤT) ===\n")

    # Đọc file kết quả mới
    result_file = Path("Book2_processed_result_v3.xlsx")

    if not result_file.exists():
        print("Không tìm thấy file kết quả!")
        return

    # Đọc dữ liệu
    df = pd.read_excel(result_file)

    # Các nhóm hoạt chất
    group_columns = ['NSAIDs', 'giảm đau', 'Opioid', 'Corticoid', 'Acid Hyaluronic ', 'Canxi', 'Loãng xương', 'khác']

    print("1. THỐNG KÊ TỔNG QUAN:")
    print(f"- Tổng số records: {len(df)}")
    print(f"- Số records có hoạt chất: {df['Hoạt chất'].notna().sum()}")
    print()

    # Thống kê từng nhóm
    print("2. THỐNG KÊ THEO NHÓM HOẠT CHẤT:")
    total_records = len(df)
    for group in group_columns:
        if group in df.columns:
            if group == 'khác':
                # Đếm số records có hoạt chất trong nhóm "khác"
                count_1 = df[group].notna().sum() - (df[group] == 0).sum()
                count_0 = (df[group] == 0).sum()
                percentage_1 = (count_1 / total_records) * 100
                percentage_0 = (count_0 / total_records) * 100
                print(f"- {group}:")
                print(f"  + Có hoạt chất: {count_1} records ({percentage_1:.1f}%) - ghi tên")
                print(f"  + Không có: {count_0} records ({percentage_0:.1f}%) - ghi 0")
            else:
                count_1 = df[group].sum()
                count_0 = (df[group] == 0).sum()
                percentage_1 = (count_1 / total_records) * 100
                percentage_0 = (count_0 / total_records) * 100
                print(f"- {group}:")
                print(f"  + Số 1: {count_1} records ({percentage_1:.1f}%)")
                print(f"  + Số 0: {count_0} records ({percentage_0:.1f}%)")
    print()

    # Kiểm tra tính nhất quán
    print("3. KIỂM TRA TÍNH NHẤT QUÁN:")
    for group in group_columns:
        if group in df.columns:
            if group == 'khác':
                # Kiểm tra nhóm "khác" có text hoặc 0
                total_marked = (df[group] == 0).sum() + df[group].notna().sum()
                if total_marked == total_records:
                    print(f"✅ {group}: Tất cả {total_records} records đều được đánh dấu 0 hoặc ghi tên hoạt chất")
                else:
                    print(f"❌ {group}: Chỉ {total_marked}/{total_records} records được đánh dấu")
            else:
                total_marked = df[group].sum() + (df[group] == 0).sum()
                if total_marked == total_records:
                    print(f"✅ {group}: Tất cả {total_records} records đều được đánh dấu 0 hoặc 1")
                else:
                    print(f"❌ {group}: Chỉ {total_marked}/{total_records} records được đánh dấu")
    print()

    # Hiển thị một vài ví dụ
    print("4. VÍ DỤ KẾT QUẢ:")
    for idx, row in df.head(3).iterrows():
        print(f"\nRecord {row.get('STT', idx+1)}:")
        hoat_chat = str(row['Hoạt chất'])[:80] + "..." if len(str(row['Hoạt chất'])) > 80 else str(row['Hoạt chất'])
        print(f"  Hoạt chất: {hoat_chat}")

        # Hiển thị tất cả các nhóm
        for group in group_columns:
            if group in row:
                value = row[group]
                if group == 'khác' and value != 0:
                    print(f"  {group}: '{value}' (ghi tên hoạt chất)")
                else:
                    print(f"  {group}: {value}")

    print("\n5. PHÂN TÍCH NHÓM 'KHÁC':")
    print("Các hoạt chất phổ biến trong nhóm 'khác':")
    khac_values = df['khác'].dropna()
    khac_values = khac_values[khac_values != 0]

    if len(khac_values) > 0:
        # Đếm tần suất xuất hiện của từng hoạt chất
        hoat_chat_count = {}
        for value in khac_values:
            hoat_chats = [x.strip() for x in str(value).split(';') if x.strip()]
            for hoat_chat in hoat_chats:
                if hoat_chat in hoat_chat_count:
                    hoat_chat_count[hoat_chat] += 1
                else:
                    hoat_chat_count[hoat_chat] = 1

        # Sắp xếp theo tần suất giảm dần
        sorted_hoat_chat = sorted(hoat_chat_count.items(), key=lambda x: x[1], reverse=True)

        print(f"Tìm thấy {len(hoat_chat_count)} hoạt chất khác nhau:")
        for hoat_chat, count in sorted_hoat_chat[:10]:  # Hiển thị top 10
            print(f"  {hoat_chat}: {count} lần")

        if len(sorted_hoat_chat) > 10:
            print(f"  ... và {len(sorted_hoat_chat) - 10} hoạt chất khác")
    else:
        print("Không có hoạt chất nào trong nhóm 'khác'")

if __name__ == "__main__":
    check_results_v3()
