from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Schema nhận dữ liệu từ người dùng gửi lên


class TaiKhoanCreate(BaseModel):
    ten_dang_nhap: str
    mat_khau: str
    can_bo_id: Optional[int] = None
    trang_thai: Optional[str] = "ACTIVE"

# Schema trả kết quả về (CHÚ Ý: Không bao giờ trả về mật khẩu)


class TaiKhoanResponse(BaseModel):
    id: int
    ten_dang_nhap: str
    can_bo_id: Optional[int]
    trang_thai: str
    ngay_tao: datetime

    class Config:
        from_attributes = True
