import pandas as pd
import numpy as np
import re
from pathlib import Path

def normalize_text(text):
    """
    Chuẩn hóa text để so sánh: lowercase và bỏ khoảng trắng thừa
    """
    if pd.isna(text) or text == '':
        return ''

    # Chuyển về string và lowercase
    text = str(text).lower().strip()

    # Bỏ khoảng trắng thừa
    text = re.sub(r'\s+', ' ', text)

    return text.strip()

def process_excel_file(file_path):
    """
    Xử lý file Excel Book2.xlsx
    """
    print(f"Đang đọc file: {file_path}")

    # Đọc 2 sheet
    try:
        data_sheet = pd.read_excel(file_path, sheet_name='Data')
        hoat_chat_sheet = pd.read_excel(file_path, sheet_name='Hoat_Chat')
        print(f"Đã đọc thành công 2 sheet:")
        print(f"- Sheet Data: {data_sheet.shape[0]} rows, {data_sheet.shape[1]} columns")
        print(f"- Sheet Hoat_Chat: {hoat_chat_sheet.shape[0]} rows, {hoat_chat_sheet.shape[1]} columns")
    except Exception as e:
        print(f"Lỗi khi đọc file Excel: {e}")
        return None, None

    # Hiển thị thông tin về các cột
    print("\nCác cột trong sheet Data:")
    print(data_sheet.columns.tolist())

    print("\nCác cột trong sheet Hoat_Chat:")
    print(hoat_chat_sheet.columns.tolist())

    return data_sheet, hoat_chat_sheet

def create_hoat_chat_mapping(hoat_chat_sheet):
    """
    Tạo mapping từ hoạt chất sang các nhóm
    """
    mapping = {}

    # Lấy tên các nhóm
    group_columns = hoat_chat_sheet.columns.tolist()
    print(f"\nCác nhóm hoạt chất: {group_columns}")

    # Duyệt qua từng cột (nhóm) trong sheet Hoat_Chat
    for group in group_columns:
        # Lấy tất cả hoạt chất trong nhóm này
        hoat_chat_list = []
        for value in hoat_chat_sheet[group].dropna():
            if pd.notna(value) and str(value).strip() != '':
                # Split nếu có nhiều hoạt chất trong một ô
                hoat_chats = [x.strip() for x in str(value).split(';') if x.strip()]
                hoat_chat_list.extend(hoat_chats)

        # Thêm vào mapping
        for hoat_chat in hoat_chat_list:
            normalized_name = normalize_text(hoat_chat)
            if normalized_name == '':
                continue

            if normalized_name not in mapping:
                mapping[normalized_name] = []
            mapping[normalized_name].append(group)

    print(f"Đã tạo mapping cho {len(mapping)} hoạt chất")
    return mapping, group_columns

def process_data_sheet(data_sheet, hoat_chat_mapping, group_columns):
    """
    Xử lý sheet Data và đánh dấu các nhóm hoạt chất
    """
    print(f"\nĐang xử lý {len(data_sheet)} records trong sheet Data...")

    # Tạo bản sao để không ảnh hưởng đến dữ liệu gốc
    result_df = data_sheet.copy()

    # Thêm các cột nhóm mới nếu chưa có
    for group in group_columns:
        if group not in result_df.columns:
            result_df[group] = 0

        # Duyệt qua từng record
    for idx, row in result_df.iterrows():
        hoat_chat_col = row['Hoạt chất'] if 'Hoạt chất' in row else None

        if pd.isna(hoat_chat_col) or hoat_chat_col == '':
            # Đánh dấu 0 cho tất cả nhóm nếu không có hoạt chất
            for group in group_columns:
                result_df.at[idx, group] = 0
            continue

        # Split hoạt chất theo dấu ;
        hoat_chat_list = [x.strip() for x in str(hoat_chat_col).split(';') if x.strip()]

                # Tìm các nhóm cho từng hoạt chất
        found_groups = set()
        hoat_chat_khac = []  # Lưu danh sách hoạt chất thuộc nhóm "khác"

        for hoat_chat in hoat_chat_list:
            normalized_hoat_chat = normalize_text(hoat_chat)
            if normalized_hoat_chat in hoat_chat_mapping:
                groups = hoat_chat_mapping[normalized_hoat_chat]
                found_groups.update(groups)

                # Nếu hoạt chất thuộc nhóm "khác", lưu lại tên
                if 'khác' in groups:
                    hoat_chat_khac.append(hoat_chat)

        # Đánh dấu 0 cho tất cả nhóm trước
        for group in group_columns:
            result_df.at[idx, group] = 0

        # Sau đó đánh dấu 1 cho các nhóm tìm thấy (trừ nhóm "khác")
        for group in found_groups:
            if group != 'khác':
                result_df.at[idx, group] = 1

        # Xử lý đặc biệt cho nhóm "khác": ghi tên hoạt chất thay vì số 1
        if hoat_chat_khac:
            result_df.at[idx, 'khác'] = '; '.join(hoat_chat_khac)

    print("Đã hoàn thành xử lý!")
    return result_df

def main():
    """
    Hàm chính để xử lý file Excel
    """
    # Đường dẫn file
    file_path = Path("data/Book2.xlsx")

    if not file_path.exists():
        print(f"Không tìm thấy file: {file_path}")
        return

    # Đọc file Excel
    data_sheet, hoat_chat_sheet = process_excel_file(file_path)

    if data_sheet is None or hoat_chat_sheet is None:
        return

    # Tạo mapping hoạt chất
    hoat_chat_mapping, group_columns = create_hoat_chat_mapping(hoat_chat_sheet)

    # Xử lý sheet Data
    result_df = process_data_sheet(data_sheet, hoat_chat_mapping, group_columns)

    # Lưu kết quả
    output_file = "Book2_processed_result_v3.xlsx"
    result_df.to_excel(output_file, index=False)
    print(f"\nĐã lưu kết quả vào file: {output_file}")

    # Hiển thị thống kê
    print("\nThống kê kết quả:")
    for group in group_columns:
        if group == 'khác':
            # Đếm số records có hoạt chất trong nhóm "khác"
            count = result_df[group].notna().sum() - (result_df[group] == 0).sum()
            print(f"- {group}: {count} records (ghi tên hoạt chất)")
        else:
            count = result_df[group].sum()
            print(f"- {group}: {count} records")

    # Hiển thị một vài ví dụ
    print("\nVí dụ kết quả (5 records đầu):")
    display_columns = ['Hoạt chất'] + group_columns
    available_columns = [col for col in display_columns if col in result_df.columns]
    print(result_df[available_columns].head())

if __name__ == "__main__":
    main()
