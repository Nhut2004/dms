from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Schema nhận dữ liệu từ người dùng gửi lên
class TaiKhoanCreate(BaseModel):
    co_quan_id: int
    ho_ten: str
    chuc_vu: Optional[str] = None
    email: Optional[str] = None
    ten_dang_nhap: str
    mat_khau: str
    vai_tro: Optional[str] = "chuyen_vien" # lanh_dao, van_thu, chuyen_vien, admin

# Schema trả kết quả về (CHÚ Ý: Không bao giờ trả về mật khẩu)
class TaiKhoanResponse(BaseModel):
    id: int
    co_quan_id: int
    ho_ten: str
    chuc_vu: Optional[str]
    email: Optional[str]
    ten_dang_nhap: str
    vai_tro: str
    trang_thai: int
    created_at: datetime

    class Config:
        from_attributes = True