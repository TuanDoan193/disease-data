import pandas as pd
from pathlib import Path

def debug_hoat_chat_sheet():
    """
    Debug cấu trúc sheet Hoat_Chat
    """
    print("=== DEBUG SHEET HOẠT CHẤT ===\n")

    # Đọc file gốc
    original_file = Path("data/Book2.xlsx")
    hoat_chat_sheet = pd.read_excel(original_file, sheet_name='Hoat_Chat')

    print("1. THÔNG TIN SHEET:")
    print(f"Shape: {hoat_chat_sheet.shape}")
    print(f"Columns: {hoat_chat_sheet.columns.tolist()}")
    print()

    print("2. 10 DÒNG ĐẦU TIÊN:")
    print(hoat_chat_sheet.head(10).to_string())
    print()

    print("3. KIỂM TRA TỪNG CỘT:")
    for col in hoat_chat_sheet.columns:
        col_data = hoat_chat_sheet[col]
        non_null = col_data.notna().sum()
        unique_vals = col_data.nunique()
        ones = (col_data == 1).sum()
        print(f"  {col}: {non_null} non-null, {unique_vals} unique, {ones} ones")

    print()

    print("4. TÌM CÁC HOẠT CHẤT CÓ GIÁ TRỊ 1:")
    group_columns = ['Giảm đau', 'Opioid', 'Corticoid', 'Acid Hyaluronic', 'Canxi', 'Loãng xương', 'Khác']

    for group in group_columns:
        if group in hoat_chat_sheet.columns:
            print(f"\n{group}:")
            # Tìm các dòng có giá trị 1 trong cột này
            mask = hoat_chat_sheet[group] == 1
            if mask.any():
                for idx, row in hoat_chat_sheet[mask].iterrows():
                    # Tìm tên hoạt chất (có thể ở cột đầu tiên hoặc index)
                    hoat_chat_name = row.iloc[0] if pd.notna(row.iloc[0]) else f"Row {idx}"
                    print(f"  {hoat_chat_name}")
            else:
                print("  Không có hoạt chất nào")

if __name__ == "__main__":
    debug_hoat_chat_sheet()
