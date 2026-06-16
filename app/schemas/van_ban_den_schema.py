from pydantic import BaseModel
from typing import Optional
from datetime import date


class VanBanDenCreate(BaseModel):
    so_den: int
    ky_hieu: Optional[str] = None
    ngay_den: date
    ngay_ban_hanh: Optional[date] = None
    co_quan_ban_hanh_id: Optional[int] = None
    ma_loai_vb_id: int
    trich_yeu: str
    ngon_ngu: Optional[str] = "Tiếng Việt"
    so_trang: Optional[int] = None
    ho_ten_nguoi_ky: Optional[str] = None
    chuc_vu_nguoi_ky: Optional[str] = None
    linh_vuc: Optional[str] = None
    do_khan: Optional[int] = None
    don_vi_nhan: Optional[str] = None
    han_giai_quyet: Optional[date] = None
    y_kien_chi_dao: Optional[str] = None
    stt_trong_ho_so: Optional[int] = None
    ma_ho_so: Optional[str] = None


class VanBanDenResponse(BaseModel):
    id: int
    so_den: int
    ky_hieu: Optional[str]
    ngay_den: date
    trich_yeu: str
    ma_loai_vb_id: int
    ma_ho_so: Optional[str]

    class Config:
        from_attributes = True
