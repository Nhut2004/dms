from pydantic import BaseModel
from typing import Optional
from datetime import date
from typing import Optional, List
from app.schemas.tep_dinh_kem_schema import TepDinhKemResponse


class VanBanDenBase(BaseModel):
    so_den: int
    ky_hieu: Optional[str] = None
    ngay_den: date
    ngay_ban_hanh: Optional[date] = None
    co_quan_ban_hanh_id: Optional[int] = None
    ma_loai_vb_id: Optional[int] = None
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
    trang_thai_xu_ly: Optional[str] = "CHO_XU_LY"
    stt_trong_ho_so: Optional[int] = None
    ma_ho_so: Optional[str] = None


class VanBanDenCreate(VanBanDenBase):
    pass


class VanBanDenUpdate(BaseModel):
    so_den: Optional[int] = None
    ky_hieu: Optional[str] = None
    ngay_den: Optional[date] = None
    ngay_ban_hanh: Optional[date] = None
    co_quan_ban_hanh_id: Optional[int] = None
    ma_loai_vb_id: Optional[int] = None
    trich_yeu: Optional[str] = None
    ngon_ngu: Optional[str] = None
    so_trang: Optional[int] = None
    ho_ten_nguoi_ky: Optional[str] = None
    chuc_vu_nguoi_ky: Optional[str] = None
    linh_vuc: Optional[str] = None
    do_khan: Optional[int] = None
    don_vi_nhan: Optional[str] = None
    han_giai_quyet: Optional[date] = None
    y_kien_chi_dao: Optional[str] = None
    trang_thai_xu_ly: Optional[str] = None
    stt_trong_ho_so: Optional[int] = None
    ma_ho_so: Optional[str] = None


class FileDinhKemResponse(BaseModel):
    id: int
    ten_file: str
    duong_dan: str

    class Config:
        from_attributes = True


class VanBanDenResponse(VanBanDenBase):
    id: int
    tep_dinh_kems: List[TepDinhKemResponse] = []

    class Config:
        from_attributes = True
