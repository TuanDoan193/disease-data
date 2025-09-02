
import pandas as pd
import os
from file_reader import read_excel_file
from dataclasses import dataclass
from typing import List, Dict, Any, Optional


@dataclass
class ThongTinCoBan:
    """Class chứa thông tin cơ bản của đơn thuốc"""
    ten_myt: str = ""
    ten_thuoc: List[str] = None
    chandoan: str = ""
    hoat_chat: List[str] = None
    atc: List[str] = None
    vi_tri_thk: List[str] = None
    benh_kem: bool = False

    def __post_init__(self):
        if self.ten_thuoc is None:
            self.ten_thuoc = []
        if self.hoat_chat is None:
            self.hoat_chat = []
        if self.atc is None:
            self.atc = []
        if self.vi_tri_thk is None:
            self.vi_tri_thk = []


@dataclass
class BenhLyNen:
    """Class chứa thông tin bệnh lý nền"""
    THA: bool = False  # Tăng huyết áp
    tim_mach_khac: bool = False  # Tim mạch khác (suy tim, BMV, ĐTN)
    DTĐ: bool = False  # Đái tháo đường
    tieu_hoa: bool = False  # Tiêu hóa
    ho_hap: bool = False  # Hô hấp
    CXK_khac: bool = False  # CXK khác
    benh_than_man: bool = False  # Bệnh thận mạn
    benh_khac: bool = False  # Bệnh khác

    def get_active_conditions(self) -> List[str]:
        """Lấy danh sách bệnh lý nền đang hoạt động"""
        conditions = []
        for field, value in self.__dict__.items():
            if value:
                conditions.append(field)
        return conditions


@dataclass
class NhomThuoc:
    """Class chứa thông tin nhóm thuốc"""
    NSAIDs: bool = False
    giam_dau: bool = False
    opioid: bool = False
    corticoid: bool = False
    acid_hyaluronic: bool = False
    canxi: bool = False
    loang_xuong: bool = False
    thuoc_khac: bool = False

    def get_active_groups(self) -> List[str]:
        """Lấy danh sách nhóm thuốc đang sử dụng"""
        groups = []
        for field, value in self.__dict__.items():
            if value:
                groups.append(field)
        return groups


@dataclass
class TuongTacThuoc:
    """Class chứa thông tin tương tác thuốc"""
    tong_so_cap_tuong_tac: int = 0
    so_cap_major: int = 0
    liet_ke_cap_major: List[str] = None
    hau_qua_cap_major: str = ""
    co_che_ttt: str = ""
    so_cap_moderate: int = 0
    so_cap_anh_huong_than: int = 0
    tong_so_cap_contraindicated_serious: int = 0
    liet_ke_cap_contraindicated_serious: List[str] = None
    hau_qua_cap_contraindicated_serious: str = ""
    tong_so_cap_contraindicated: int = 0
    liet_ke_cap_contraindicated: List[str] = None
    hau_qua_cap_contraindicated: str = ""
    tong_so_cap_serious: int = 0
    liet_ke_cap_serious: List[str] = None
    hau_qua_cap_serious: str = ""
    so_cap_anh_huong_than_chi_tiet: int = 0
    liet_ke_cap_anh_huong_than: List[str] = None
    hau_qua_cap_anh_huong_than: str = ""
    so_cap_CCĐ: int = 0
    liet_ke_cap_CCĐ: List[str] = None

    def __post_init__(self):
        if self.liet_ke_cap_major is None:
            self.liet_ke_cap_major = []
        if self.liet_ke_cap_contraindicated_serious is None:
            self.liet_ke_cap_contraindicated_serious = []
        if self.liet_ke_cap_contraindicated is None:
            self.liet_ke_cap_contraindicated = []
        if self.liet_ke_cap_serious is None:
            self.liet_ke_cap_serious = []
        if self.liet_ke_cap_anh_huong_than is None:
            self.liet_ke_cap_anh_huong_than = []
        if self.liet_ke_cap_CCĐ is None:
            self.liet_ke_cap_CCĐ = []

    def get_summary(self) -> Dict[str, Any]:
        """Lấy tóm tắt tương tác thuốc"""
        return {
            'tong_so_cap': self.tong_so_cap_tuong_tac,
            'major': self.so_cap_major,
            'moderate': self.so_cap_moderate,
            'contraindicated': self.tong_so_cap_contraindicated,
            'serious': self.tong_so_cap_serious,
            'anh_huong_than': self.so_cap_anh_huong_than
        }


class DonThuoc:
    def __init__(self, **kwargs):
        """
        Khởi tạo đơn thuốc với cấu trúc OOP

        Args:
            **kwargs: Các tham số động được chia thành các nhóm:
                - Thông tin cơ bản: ten_myt, ten_thuoc, chandoan, hoat_chat, atc, vi_tri_thk, benh_kem
                - Bệnh lý nền: THA, tim_mach_khac, DTĐ, tieu_hoa, ho_hap, CXK_khac, benh_than_man, benh_khac
                - Nhóm thuốc: NSAIDs, giam_dau, opioid, corticoid, acid_hyaluronic, canxi, loang_xuong, thuoc_khac
                - Tương tác thuốc: tất cả các tham số liên quan đến tương tác
        """
        # Khởi tạo các class con
        self.thong_tin_co_ban = ThongTinCoBan()
        self.benh_ly_nen = BenhLyNen()
        self.nhom_thuoc = NhomThuoc()
        self.tuong_tac_thuoc = TuongTacThuoc()

        # Lưu tất cả tham số gốc
        self.all_params = kwargs.copy()

        # Phân loại và gán tham số vào các class con
        self._process_basic_info(kwargs)
        self._process_medical_conditions(kwargs)
        self._process_drug_groups(kwargs)
        self._process_drug_interactions(kwargs)

    def _process_basic_info(self, kwargs: Dict[str, Any]):
        """Xử lý thông tin cơ bản"""
        basic_fields = ['ten_myt', 'chandoan', 'benh_kem']
        list_fields = ['ten_thuoc', 'hoat_chat', 'atc', 'vi_tri_thk']

        for field in basic_fields:
            if field in kwargs:
                setattr(self.thong_tin_co_ban, field, kwargs[field])

        for field in list_fields:
            if field in kwargs:
                value = kwargs[field]
                if isinstance(value, str):
                    setattr(self.thong_tin_co_ban, field, [value] if value else [])
                elif isinstance(value, list):
                    setattr(self.thong_tin_co_ban, field, value)

    def _process_medical_conditions(self, kwargs: Dict[str, Any]):
        """Xử lý bệnh lý nền"""
        condition_fields = ['THA', 'tim_mach_khac', 'DTĐ', 'tieu_hoa', 'ho_hap',
                           'CXK_khac', 'benh_than_man', 'benh_khac']

        for field in condition_fields:
            if field in kwargs:
                setattr(self.benh_ly_nen, field, bool(kwargs[field]))

    def _process_drug_groups(self, kwargs: Dict[str, Any]):
        """Xử lý nhóm thuốc"""
        drug_fields = ['NSAIDs', 'giam_dau', 'opioid', 'corticoid',
                      'acid_hyaluronic', 'canxi', 'loang_xuong', 'thuoc_khac']

        for field in drug_fields:
            if field in kwargs:
                setattr(self.nhom_thuoc, field, bool(kwargs[field]))

    def _process_drug_interactions(self, kwargs: Dict[str, Any]):
        """Xử lý tương tác thuốc"""
        interaction_fields = [
            'tong_so_cap_tuong_tac', 'so_cap_major', 'so_cap_moderate',
            'so_cap_anh_huong_than', 'tong_so_cap_contraindicated_serious',
            'tong_so_cap_contraindicated', 'tong_so_cap_serious',
            'so_cap_anh_huong_than_chi_tiet', 'so_cap_CCĐ'
        ]

        string_fields = [
            'hau_qua_cap_major', 'co_che_ttt', 'hau_qua_cap_contraindicated_serious',
            'hau_qua_cap_contraindicated', 'hau_qua_cap_serious', 'hau_qua_cap_anh_huong_than'
        ]

        list_fields = [
            'liet_ke_cap_major', 'liet_ke_cap_contraindicated_serious',
            'liet_ke_cap_contraindicated', 'liet_ke_cap_serious',
            'liet_ke_cap_anh_huong_than', 'liet_ke_cap_CCĐ'
        ]

        for field in interaction_fields:
            if field in kwargs:
                setattr(self.tuong_tac_thuoc, field, kwargs.get(field, 0))

        for field in string_fields:
            if field in kwargs:
                setattr(self.tuong_tac_thuoc, field, kwargs.get(field, ''))

        for field in list_fields:
            if field in kwargs:
                value = kwargs[field]
                if isinstance(value, str):
                    setattr(self.tuong_tac_thuoc, field, [value] if value else [])
                elif isinstance(value, list):
                    setattr(self.tuong_tac_thuoc, field, value)

    def __str__(self):
        """Hiển thị thông tin đơn thuốc"""
        thuoc_str = ", ".join(self.thong_tin_co_ban.ten_thuoc) if self.thong_tin_co_ban.ten_thuoc else "Không có"
        return f"🏥 {self.thong_tin_co_ban.ten_myt} | 💊 {thuoc_str} | 📋 {self.thong_tin_co_ban.chandoan}"

    def get_info(self) -> Dict[str, Any]:
        """Lấy thông tin chi tiết đơn thuốc"""
        return {
            'thong_tin_co_ban': self.thong_tin_co_ban.__dict__,
            'benh_ly_nen': self.benh_ly_nen.__dict__,
            'nhom_thuoc': self.nhom_thuoc.__dict__,
            'tuong_tac_thuoc': self.tuong_tac_thuoc.__dict__
        }

    def is_valid(self) -> bool:
        """Kiểm tra đơn thuốc có hợp lệ không"""
        return bool(
            self.thong_tin_co_ban.ten_myt and
            self.thong_tin_co_ban.ten_thuoc and
            self.thong_tin_co_ban.chandoan
        )

    def to_dict(self) -> Dict[str, Any]:
        """Chuyển đổi thành dictionary"""
        return self.get_info()

    def get_thuoc_count(self) -> int:
        """Lấy số lượng thuốc trong đơn"""
        return len(self.thong_tin_co_ban.ten_thuoc)

    def add_thuoc(self, ten_thuoc: str, **kwargs):
        """Thêm thuốc vào đơn với các thông tin bổ sung"""
        if ten_thuoc:
            self.thong_tin_co_ban.ten_thuoc.append(ten_thuoc)

            # Thêm các thông tin liên quan
            for field, value in kwargs.items():
                if hasattr(self.thong_tin_co_ban, field) and isinstance(getattr(self.thong_tin_co_ban, field), list):
                    getattr(self.thong_tin_co_ban, field).append(value)

    def remove_thuoc(self, ten_thuoc: str):
        """Xóa thuốc khỏi đơn"""
        if ten_thuoc in self.thong_tin_co_ban.ten_thuoc:
            index = self.thong_tin_co_ban.ten_thuoc.index(ten_thuoc)
            self.thong_tin_co_ban.ten_thuoc.pop(index)

            # Xóa các thông tin liên quan
            list_fields = ['hoat_chat', 'atc', 'vi_tri_thk']
            for field in list_fields:
                if hasattr(self.thong_tin_co_ban, field) and index < len(getattr(self.thong_tin_co_ban, field)):
                    getattr(self.thong_tin_co_ban, field).pop(index)

    def get_benh_ly_nen(self) -> List[str]:
        """Lấy danh sách bệnh lý nền"""
        return self.benh_ly_nen.get_active_conditions()

    def get_nhom_thuoc(self) -> List[str]:
        """Lấy danh sách nhóm thuốc"""
        return self.nhom_thuoc.get_active_groups()

    def get_tuong_tac_summary(self) -> Dict[str, Any]:
        """Lấy tóm tắt tương tác thuốc"""
        return self.tuong_tac_thuoc.get_summary()

    def get_param(self, param_name: str, default=None):
        """Lấy giá trị tham số theo tên"""
        return self.all_params.get(param_name, default)

    def set_param(self, param_name: str, value):
        """Đặt giá trị tham số"""
        self.all_params[param_name] = value
        # Có thể cần cập nhật lại các class con tương ứng

    def get_all_params(self) -> Dict[str, Any]:
        """Lấy tất cả tham số"""
        return self.all_params.copy()
