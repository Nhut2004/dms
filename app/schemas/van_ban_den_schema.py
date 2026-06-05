from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime

# Schema nhận dữ liệu tạo mới


class VanBanDenCreate(BaseModel):
    # Thông tin ban hành
    organ_id: str
    organ_name: Optional[str] = None
    type_name: Optional[str] = None
    code_number: Optional[str] = None
    code_notation: Optional[str] = None
    issued_date: Optional[date] = None

    # Nội dung
    subject: Optional[str] = None
    language: Optional[str] = "Tiếng Việt"
    page_amount: Optional[int] = None
    description: Optional[str] = None
    priority: Optional[int] = 1

    # Thông tin tiếp nhận (Văn bản đến)
    arrival_date: Optional[date] = None
    arrival_number: Optional[int] = None
    to_places: Optional[str] = None
    trace_header_list: Optional[str] = None
    due_date: Optional[date] = None

    # Người ký
    signer_position: Optional[str] = None
    signer_full_name: Optional[str] = None

    # Các khóa ngoại liên kết
    ho_so_id: Optional[int] = None
    loai_vb_id: int
    nguoi_nhap_id: int  # Người thực hiện nhập liệu vào hệ thống

# Schema trả kết quả về


class VanBanDenResponse(BaseModel):
    id: int
    organ_id: str
    code_notation: Optional[str]
    subject: Optional[str]
    arrival_date: Optional[date]
    status: str
    loai_vb_id: int
    nguoi_nhap_id: int
    ho_so_id: Optional[int]
    created_at: datetime

    class Config:
        from_attributes = True
