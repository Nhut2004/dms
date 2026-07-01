from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# 1. Schema dùng để kiểm tra dữ liệu khi người dùng gửi lên (Create)


class CoQuanCreate(BaseModel):
    ten_co_quan: str
    organ_id: str
    dia_chi: Optional[str] = None

# 2. Schema dùng để định dạng dữ liệu khi trả về cho người dùng (Response)


class CoQuanResponse(BaseModel):
    id: int
    ten_co_quan: str
    organ_id: str
    dia_chi: Optional[str]

    class Config:
        from_attributes = True  # Cho phép Pydantic đọc dữ liệu trực tiếp từ SQLAlchemy Model
