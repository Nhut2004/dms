from pydantic import BaseModel
from typing import Optional
from datetime import date


class HoSoCreate(BaseModel):
    ma_ho_so: str  # Khóa chính giờ là String (chữ)
    tieu_de_ho_so: str
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


class HoSoResponse(BaseModel):
    ma_ho_so: str
    tieu_de_ho_so: str
    ngay_bat_dau: Optional[date]
    ngay_ket_thuc: Optional[date]
    vi_tri_id: Optional[int]

    class Config:
        from_attributes = True
