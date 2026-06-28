from pydantic import BaseModel
from typing import Optional, List
from datetime import date


class FileDinhKemResponse(BaseModel):
    id: int
    loai_van_ban: str
    van_ban_id: int
    ten_file: str
    duong_dan: str
    dinh_dang: Optional[str] = None
    dung_luong: Optional[float] = None

    class Config:
        from_attributes = True


class VanBanDiCreate(BaseModel):
    so_ky_hieu: Optional[str] = None
    ngay_ban_hanh: Optional[date] = None
    trich_yeu: str
    don_vi_soan_thao_id: int
    ma_loai_vb_id: int
    ngon_ngu: Optional[str] = "Tiếng Việt"
    so_trang: Optional[int] = None
    ghi_chu: Optional[str] = None
    nguoi_ky_id: Optional[int] = None
    chuc_vu_nguoi_ky: Optional[str] = None
    noi_nhan: Optional[str] = None
    muc_do_khan: Optional[int] = None
    trang_thai: Optional[str] = "DRAFT"
    han_tra_loi: Optional[date] = None
    stt_trong_ho_so: Optional[int] = None
    ma_ho_so: Optional[str] = None
    so_luong_ban_phat_hanh: Optional[int] = None


class VanBanDiResponse(BaseModel):
    id: int
    so_ky_hieu: Optional[str] = None
    ngay_ban_hanh: Optional[date] = None
    trich_yeu: str
    don_vi_soan_thao_id: int
    ma_loai_vb_id: int
    ngon_ngu: Optional[str] = None
    so_trang: Optional[int] = None
    ghi_chu: Optional[str] = None
    nguoi_ky_id: Optional[int] = None
    chuc_vu_nguoi_ky: Optional[str] = None
    noi_nhan: Optional[str] = None
    muc_do_khan: Optional[int] = None
    han_tra_loi: Optional[date] = None
    stt_trong_ho_so: Optional[int] = None
    ma_ho_so: Optional[str] = None
    trang_thai: Optional[str] = None
    tep_dinh_kems: Optional[List[FileDinhKemResponse]] = None
    so_luong_ban_phat_hanh: Optional[int] = None


class TrangThaiUpdate(BaseModel):
    trang_thai: str

    class Config:
        from_attributes = True
