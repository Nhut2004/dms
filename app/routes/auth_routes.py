from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session, joinedload  # Bổ sung joinedload
from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta
from config.database import get_db
from app.models.auth import TaiKhoan
from app.schemas.auth_schema import TokenResponse
from app.dependencies import SECRET_KEY, ALGORITHM

router = APIRouter(
    prefix="/api/auth",
    tags=["Xác thực & Đăng nhập"]
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24


@router.post("/login", response_model=TokenResponse)
def dang_nhap(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # ĐÃ SỬA: Dùng joinedload để lôi bằng được danh sách quyền từ DB lên
    user = db.query(TaiKhoan).options(joinedload(TaiKhoan.vai_tros)).filter(
        TaiKhoan.ten_dang_nhap == form_data.username).first()

    if not user:
        raise HTTPException(status_code=401, detail="Tài khoản không tồn tại!")

    if user.trang_thai != 'ACTIVE':
        raise HTTPException(status_code=403, detail="Tài khoản đã bị khóa!")

    mat_khau_dung = pwd_context.verify(form_data.password, user.mat_khau_hash)
    if not mat_khau_dung:
        raise HTTPException(
            status_code=401, detail="Mật khẩu không chính xác!")

    thoi_gian_het_han = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    thong_tin_luu_trong_the = {
        "sub": user.ten_dang_nhap,
        "id": user.id,
        "exp": thoi_gian_het_han
    }
    access_token = jwt.encode(thong_tin_luu_trong_the,
                              SECRET_KEY, algorithm=ALGORITHM)

    # ĐÃ SỬA: Trích xuất các quyền (VD: ['ADMIN', 'VAN_THU'])
    danh_sach_vai_tro = [
        vt.ma_vai_tro for vt in user.vai_tros] if user.vai_tros else []

    # Bắn trả về cho Frontend kèm theo quyền
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "tai_khoan_id": user.id,
        "ten_dang_nhap": user.ten_dang_nhap,
        "vai_tros": danh_sach_vai_tro
    }
