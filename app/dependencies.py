from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
import jwt
from config.database import get_db
from app.models.tai_khoan_nguoi_dung import TaiKhoanNguoiDung

# Chỉ định đường dẫn đăng nhập để Swagger UI biết chỗ lấy Token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")

# Khóa bí mật (file auth_routes.py)
SECRET_KEY = "DMS_CHIA_KHOA_BI_MAT_CUA_NHUT_CUC_KY_AN_TOAN_2026"
ALGORITHM = "HS256"

# Hàm bảo vệ: Kiểm tra Token và trả về thông tin người dùng hiện tại


def lay_nguoi_dung_hien_tai(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    # Chuẩn bị sẵn thông báo lỗi đuổi ra ngoài (Lỗi 401)
    loi_xac_thuc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Không thể xác thực thông tin (Token không hợp lệ hoặc đã hết hạn)",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Giải mã thẻ Token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        ten_dang_nhap: str = payload.get("sub")
        if ten_dang_nhap is None:
            raise loi_xac_thuc
    except jwt.PyJWTError:
        # Nếu Token bị chỉnh sửa hoặc hết hạn
        raise loi_xac_thuc

    # Lấy thông tin user từ Database để chắc chắn người này chưa bị xóa
    user = db.query(TaiKhoanNguoiDung).filter(
        TaiKhoanNguoiDung.ten_dang_nhap == ten_dang_nhap).first()
    if user is None:
        raise loi_xac_thuc

    # Trả về toàn bộ thông tin người dùng đang gọi API (gồm cả ID và vai_tro)
    return user
