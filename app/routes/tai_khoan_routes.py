from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from config.database import get_db
from app.models.auth import TaiKhoan
from app.schemas.tai_khoan_schema import TaiKhoanCreate, TaiKhoanResponse

# Cấu hình bộ mã hóa mật khẩu
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter(
    prefix="/api/tai-khoan",
    tags=["Quản lý Tài khoản"]
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/", response_model=TaiKhoanResponse)
def tao_tai_khoan(tai_khoan: TaiKhoanCreate, db: Session = Depends(get_db)):
    # 1. Kiểm tra trùng lặp
    kiem_tra = db.query(TaiKhoan).filter(
        TaiKhoan.ten_dang_nhap == tai_khoan.ten_dang_nhap).first()
    if kiem_tra:
        raise HTTPException(
            status_code=400, detail="Tên đăng nhập đã tồn tại!")

    # 2. Băm mật khẩu
    mat_khau_bam = pwd_context.hash(tai_khoan.mat_khau)

    # 3. Lưu vào DB (Lưu ý cột mật khẩu giờ tên là mat_khau_hash)
    tai_khoan_moi = TaiKhoan(
        ten_dang_nhap=tai_khoan.ten_dang_nhap,
        mat_khau_hash=mat_khau_bam,
        can_bo_id=tai_khoan.can_bo_id,
        trang_thai=tai_khoan.trang_thai
    )

    db.add(tai_khoan_moi)
    db.commit()
    db.refresh(tai_khoan_moi)
    return tai_khoan_moi


@router.get("/", response_model=list[TaiKhoanResponse])
def lay_danh_sach_tai_khoan(db: Session = Depends(get_db)):
    return db.query(TaiKhoan).all()
