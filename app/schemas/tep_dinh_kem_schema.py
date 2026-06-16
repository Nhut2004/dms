from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class TepDinhKemCreate(BaseModel):
    loai_van_ban: str  # Chỉ được nhập: 'VAN_BAN_DEN' hoặc 'VAN_BAN_DI'
    van_ban_id: int
    ten_file: str
    duong_dan: str
    dinh_dang: Optional[str] = None
    dung_luong: Optional[float] = None


class TepDinhKemResponse(BaseModel):
    id: int
    loai_van_ban: str
    van_ban_id: int
    ten_file: str
    duong_dan: str
    dinh_dang: Optional[str]
    dung_luong: Optional[float]
    ngay_tao: datetime

    class Config:
        from_attributes = True
