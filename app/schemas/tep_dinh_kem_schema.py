from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Schema trả kết quả về sau khi upload thành công


class TepDinhKemResponse(BaseModel):
    id: int
    ten_tep: str
    duong_dan: str
    dinh_dang: Optional[str]
    kich_thuoc: Optional[float]
    tep_chinh: int
    loai_van_ban: str
    van_ban_id: int
    nguoi_tai_len_id: Optional[int]
    thoi_gian_tai_len: datetime

    class Config:
        from_attributes = True
