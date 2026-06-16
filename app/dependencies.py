from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
import jwt
from config.database import get_db
from app.models.auth import TaiKhoan

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")

SECRET_KEY = "DMS_CHIA_KHOA_BI_MAT_CUA_NHUT_CUC_KY_AN_TOAN_2026"
ALGORITHM = "HS256"


def lay_nguoi_dung_hien_tai(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    loi_xac_thuc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Không thể xác thực thông tin (Token không hợp lệ hoặc đã hết hạn)",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        ten_dang_nhap: str = payload.get("sub")
        if ten_dang_nhap is None:
            raise loi_xac_thuc
    except jwt.PyJWTError:
        raise loi_xac_thuc

    # Truy vấn từ bảng TaiKhoan mới
    user = db.query(TaiKhoan).filter(
        TaiKhoan.ten_dang_nhap == ten_dang_nhap).first()

    # Kiểm tra thêm điều kiện tài khoản phải đang ACTIVE
    if user is None or user.trang_thai != 'ACTIVE':
        raise loi_xac_thuc

    return user
