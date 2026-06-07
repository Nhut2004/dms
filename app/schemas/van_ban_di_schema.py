from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime

# Schema nhận dữ liệu tạo mới


class VanBanDiCreate(BaseModel):
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
    issued_amount: Optional[int] = 1
    due_date: Optional[date] = None

    # Nơi nhận và Người ký
    to_organ_id: Optional[str] = None
    to_organ_name: Optional[str] = None
    signer_position: Optional[str] = None
    signer_full_name: Optional[str] = None

    # Các khóa ngoại liên kết (Bắt buộc phải có để nối dữ liệu)
    ho_so_id: Optional[int] = None
    loai_vb_id: int

# Schema trả kết quả về (hiển thị một số thông tin quan trọng)


class VanBanDiResponse(BaseModel):
    id: int
    organ_id: str
    code_notation: Optional[str]
    subject: Optional[str]
    issued_date: Optional[date]
    status: str
    loai_vb_id: int
    nguoi_soan_id: int
    ho_so_id: Optional[int]
    created_at: datetime

    class Config:
        from_attributes = True
