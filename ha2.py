import pandas as pd
import re
from pathlib import Path

def normalize_text(text):
    """Chuẩn hóa text để so sánh"""
    if pd.isna(text) or text == '':
        return ''
    text = str(text).lower().strip()
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def create_benh_mapping(benh_sheet):
    """Tạo mapping từ tên bệnh sang các nhóm bệnh"""
    mapping = {}
    group_columns = benh_sheet.columns.tolist()

    for group in group_columns:
        benh_list = []
        for value in benh_sheet[group].dropna():
            if pd.notna(value) and str(value).strip() != '':
                benh_names = re.split(r'[;,-]', str(value))
                for benh_name in benh_names:
                    benh_name = benh_name.strip()
                    if benh_name:
                        benh_list.append(benh_name)

        for benh_name in benh_list:
            normalized_name = normalize_text(benh_name)
            if normalized_name == '':
                continue
            if normalized_name not in mapping:
                mapping[normalized_name] = []
            if group not in mapping[normalized_name]:
                mapping[normalized_name].append(group)

    return mapping, group_columns

def find_benh_khac_names(chandoan_text, benh_mapping):
    """Tìm tên bệnh cụ thể thuộc nhóm 'Bệnh khác'"""
    if pd.isna(chandoan_text) or chandoan_text == '':
        return []

    chandoan_normalized = normalize_text(str(chandoan_text))
    benh_khac_names = []

    # Tìm tất cả bệnh thuộc nhóm "Bệnh khác"
    for benh_name, groups in benh_mapping.items():
        if 'Bệnh khác' in groups:
            if len(benh_name) >= 3:
                pattern = r'\b' + re.escape(benh_name) + r'\b'
                if re.search(pattern, chandoan_normalized):
                    benh_khac_names.append(benh_name)
                elif benh_name in chandoan_normalized and len(benh_name) >= 5:
                    benh_khac_names.append(benh_name)

    return benh_khac_names

def find_matching_diseases(chandoan_text, benh_mapping):
    """Tìm các bệnh trong chuỗi chẩn đoán"""
    if pd.isna(chandoan_text) or chandoan_text == '':
        return set()

    chandoan_normalized = normalize_text(str(chandoan_text))
    found_groups = set()

    sorted_diseases = sorted(benh_mapping.items(), key=lambda x: len(x[0]), reverse=True)

    for benh_name, groups in sorted_diseases:
        if len(benh_name) >= 3:
            pattern = r'\b' + re.escape(benh_name) + r'\b'
            if re.search(pattern, chandoan_normalized):
                found_groups.update(groups)
            elif benh_name in chandoan_normalized and len(benh_name) >= 5:
                found_groups.update(groups)

    return found_groups

def main():
    # Đọc file Excel
    file_path = Path("data/Book2.xlsx")
    if not file_path.exists():
        print(f"Không tìm thấy file: {file_path}")
        return

    print("Đang đọc file Excel...")
    data_sheet = pd.read_excel(file_path, sheet_name='Data')
    benh_sheet = pd.read_excel(file_path, sheet_name='Benh')

    print(f"Đã đọc: {len(data_sheet)} records từ sheet Data, {len(benh_sheet)} records từ sheet Benh")

    # Tạo mapping bệnh
    print("Đang tạo mapping bệnh...")
    benh_mapping, group_columns = create_benh_mapping(benh_sheet)

    # Xử lý sheet Data
    print("Đang xử lý phân loại bệnh...")
    result_df = data_sheet.copy()

    # Thêm các cột nhóm mới
    for group in group_columns:
        if group not in result_df.columns:
            result_df[group] = 0

    # Chuyển đổi cột "Bệnh khác" thành string để có thể ghi text
    if 'Bệnh khác' in result_df.columns:
        result_df['Bệnh khác'] = result_df['Bệnh khác'].astype(str)

    # Duyệt qua từng record
    for idx, row in result_df.iterrows():
        if(row['STT'] == 250):
            print(row)
        chandoan_col = row['ChanDoan'] if 'ChanDoan' in row else None

        if pd.isna(chandoan_col) or chandoan_col == '':
            for group in group_columns:
                result_df.at[idx, group] = 0
            continue

                        # Tìm các nhóm bệnh
        found_groups = find_matching_diseases(chandoan_col, benh_mapping)

        # Đánh dấu 0 cho tất cả nhóm trước
        for group in group_columns:
            result_df.at[idx, group] = 0

        # Sau đó đánh dấu 1 cho các nhóm tìm thấy (trừ nhóm "Bệnh khác")
        benh_khac_list = []
        for group in found_groups:
            if group == 'Bệnh khác':
                # Tìm tên bệnh cụ thể thuộc nhóm "Bệnh khác"
                benh_khac_names = find_benh_khac_names(chandoan_col, benh_mapping)
                if benh_khac_names:
                    benh_khac_list.extend(benh_khac_names)
            else:
                result_df.at[idx, group] = 1

        # Ghi tên bệnh vào cột "Bệnh khác" nếu có
        if benh_khac_list:
            result_df.at[idx, 'Bệnh khác'] = '; '.join(benh_khac_list)

        # Cập nhật cột "Bệnh kèm" dựa trên số lượng nhóm bệnh tìm thấy
        if len(found_groups) > 1:
            result_df.at[idx, 'Bệnh kèm'] = 1
        else:
            result_df.at[idx, 'Bệnh kèm'] = 0

    # Lưu kết quả
    output_file = "Book2_processed_benh_result_v4.xlsx"
    result_df.to_excel(output_file, index=False)
    print(f"Đã lưu kết quả vào file: {output_file}")

    # Thống kê đơn giản
    print("\nThống kê:")
    for group in group_columns:
        if group == 'Bệnh khác':
            # Đếm số records có nội dung trong cột "Bệnh khác"
            count = result_df[group].notna().sum() - (result_df[group] == 'nan').sum()
            print(f"- {group}: {count:.0f} records (ghi tên bệnh)")
        else:
            count = result_df[group].sum()
            print(f"- {group}: {count:.0f} records")

if __name__ == "__main__":
    main()
