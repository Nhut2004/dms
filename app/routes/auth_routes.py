from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta
from config.database import get_db
from app.models.tai_khoan_nguoi_dung import TaiKhoanNguoiDung
from app.schemas.auth_schema import LoginRequest, TokenResponse

router = APIRouter(
    prefix="/api/auth",
    tags=["Xác thực & Đăng nhập"]
)

# Cấu hình bộ giải mã mật khẩu (Giống hệt bên tạo tài khoản)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Cấu hình "Con dấu" của hệ thống để ký lên thẻ Token (Tuyệt đối bảo mật)
SECRET_KEY = "DMS_CHIA_KHOA_BI_MAT_CUA_NHUT_CUC_KY_AN_TOAN_2026"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # Thẻ có hạn 1 ngày (24 tiếng)


@router.post("/login", response_model=TokenResponse)
def dang_nhap(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # 1. Tìm tài khoản (Swagger tự map chữ username vào form_data.username)
    user = db.query(TaiKhoanNguoiDung).filter(
        TaiKhoanNguoiDung.ten_dang_nhap == form_data.username).first()

    if not user:
        raise HTTPException(status_code=401, detail="Tài khoản không tồn tại!")

    # 2. Đối chiếu mật khẩu (Swagger tự map password vào form_data.password)
    mat_khau_dung = pwd_context.verify(form_data.password, user.mat_khau)
    if not mat_khau_dung:
        raise HTTPException(
            status_code=401, detail="Mật khẩu không chính xác!")

    # 3. Mật khẩu đúng -> Tạo thẻ Token
    thoi_gian_het_han = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    thong_tin_luu_trong_the = {
        "sub": user.ten_dang_nhap,
        "id": user.id,
        "vai_tro": user.vai_tro,
        "exp": thoi_gian_het_han
    }

    # Ký đóng dấu hệ thống lên thẻ
    chuoi_token = jwt.encode(thong_tin_luu_trong_the,
                             SECRET_KEY, algorithm=ALGORITHM)

    # 4. Trả thẻ về cho người dùng
    return {
        "access_token": chuoi_token,
        "token_type": "bearer",
        "nguoi_dung_id": user.id,
        "ho_ten": user.ho_ten,
        "vai_tro": user.vai_tro
    }
