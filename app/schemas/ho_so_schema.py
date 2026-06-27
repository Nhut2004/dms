from pydantic import BaseModel
from typing import Optional
from datetime import date


class HoSoCreate(BaseModel):
    ma_ho_so: str
    tieu_de_ho_so: str
    file_catalog: Optional[int] = None
    file_notation: Optional[str] = None
    thoi_han_bao_quan: Optional[str] = None
    che_do_su_dung: Optional[str] = None
    ngay_bat_dau: Optional[date] = None
    ngay_ket_thuc: Optional[date] = None
    so_luong_trang: Optional[int] = 0
    so_luong_van_ban: Optional[int] = 0
    nguoi_lap: Optional[str] = None
    ngon_ngu: Optional[str] = "Tiếng Việt"
    ghi_chu: Optional[str] = None
    vi_tri_id: Optional[int] = None


class HoSoUpdate(BaseModel):
    tieu_de_ho_so: Optional[str] = None
    file_catalog: Optional[int] = None
    file_notation: Optional[str] = None
    thoi_han_bao_quan: Optional[str] = None
    che_do_su_dung: Optional[str] = None
    ngay_bat_dau: Optional[date] = None
    ngay_ket_thuc: Optional[date] = None
    so_luong_trang: Optional[int] = None
    so_luong_van_ban: Optional[int] = None
    nguoi_lap: Optional[str] = None
    ngon_ngu: Optional[str] = None
    ghi_chu: Optional[str] = None
    vi_tri_id: Optional[int] = None


class HoSoResponse(BaseModel):
    ma_ho_so: str
    tieu_de_ho_so: str
    file_catalog: Optional[int] = None
    file_notation: Optional[str] = None
    thoi_han_bao_quan: Optional[str] = None
    che_do_su_dung: Optional[str] = None
    ngay_bat_dau: Optional[date] = None
    ngay_ket_thuc: Optional[date] = None
    so_luong_trang: Optional[int] = None
    so_luong_van_ban: Optional[int] = None
    nguoi_lap: Optional[str] = None
    ngon_ngu: Optional[str] = None
    ghi_chu: Optional[str] = None
    vi_tri_id: Optional[int] = None

    class Config:
        from_attributes = True
