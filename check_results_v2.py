import pandas as pd
from pathlib import Path

def check_results_v2():
    """
    Kiểm tra kết quả với việc đánh dấu 0/1 rõ ràng
    """
    print("=== KIỂM TRA KẾT QUẢ V2 (ĐÁNH DẤU 0/1 RÕ RÀNG) ===\n")

    # Đọc file kết quả mới
    result_file = Path("Book2_processed_result_v2.xlsx")

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
                print(f"  {group}: {value}")

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
    check_results_v2()
