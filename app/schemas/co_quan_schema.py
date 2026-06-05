from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# 1. Schema dùng để kiểm tra dữ liệu khi người dùng gửi lên (Create)
class CoQuanCreate(BaseModel):
    organ_id: str
    ten_co_quan: str
    loai_co_quan: Optional[str] = None
    dia_chi: Optional[str] = None
    trang_thai: Optional[int] = 1
    parent_id: Optional[int] = None

# 2. Schema dùng để định dạng dữ liệu khi trả về cho người dùng (Response)
class CoQuanResponse(BaseModel):
    id: int
    organ_id: str
    ten_co_quan: str
    loai_co_quan: Optional[str]
    dia_chi: Optional[str]
    trang_thai: int
    parent_id: Optional[int]
    created_at: datetime

    class Config:
        from_attributes = True # Cho phép Pydantic đọc dữ liệu trực tiếp từ SQLAlchemy Model