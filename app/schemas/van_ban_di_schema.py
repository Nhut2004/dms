from pydantic import BaseModel
from typing import Optional
from datetime import date


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
    han_tra_loi: Optional[date] = None
    stt_trong_ho_so: Optional[int] = None
    ma_ho_so: Optional[str] = None


class VanBanDiResponse(BaseModel):
    id: int
    so_ky_hieu: Optional[str]
    trich_yeu: str
    don_vi_soan_thao_id: int
    ma_loai_vb_id: int
    ma_ho_so: Optional[str]

    class Config:
        from_attributes = True
