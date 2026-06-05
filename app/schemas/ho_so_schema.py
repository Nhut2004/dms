from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime

# Schema nhận dữ liệu tạo mới


class HoSoCreate(BaseModel):
    file_code: Optional[str] = None
    organ_id: str
    file_catalog: Optional[int] = None
    file_notation: Optional[str] = None
    title: str  # Tiêu đề hồ sơ (Bắt buộc)
    maintenance: Optional[str] = "Vĩnh viễn"
    rights: Optional[str] = "Bình thường"
    creator: Optional[str] = None
    language: Optional[str] = "Tiếng Việt"
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    description: Optional[str] = None

    # Khóa ngoại để biết hồ sơ này của cơ quan nào và ai tạo
    co_quan_id: int
    created_by_id: int

# Schema trả kết quả về


class HoSoResponse(BaseModel):
    id: int
    file_code: Optional[str]
    organ_id: str
    file_catalog: Optional[int]
    file_notation: Optional[str]
    title: str
    maintenance: Optional[str]
    rights: Optional[str]
    creator: Optional[str]
    language: Optional[str]
    start_date: Optional[date]
    end_date: Optional[date]
    doc_total: Optional[int]
    page_total: Optional[int]
    description: Optional[str]
    is_locked: int
    co_quan_id: Optional[int]
    created_by_id: Optional[int]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
