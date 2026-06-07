from pydantic import BaseModel

# Dữ liệu người dùng gửi lên để đăng nhập


class LoginRequest(BaseModel):
    ten_dang_nhap: str
    mat_khau: str

# Dữ liệu hệ thống trả về (Thẻ Token)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    nguoi_dung_id: int
    ho_ten: str
    vai_tro: str
