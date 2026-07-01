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

from app.models.auth import VaiTro  # Đảm bảo đã import VaiTro để check quyền
from pydantic import BaseModel
from typing import List

# Khai báo cấu trúc dữ liệu truyền lên khi gán vai trò
class GanVaiTroRequest(BaseModel):
    ma_vai_tro_list: List[str]  # Ví dụ truyền lên danh sách mã: ["VAN_THU", "LANH_DAO"]

# 1. API Khóa hoặc Mở khóa tài khoản (Cập nhật trạng thái ACTIVE / LOCKED)
@router.put("/{id}/trang-thai")
def cap_nhat_trang_thai_tai_khoan(id: int, trang_thai: str, db: Session = Depends(get_db)):
    if trang_thai not in ["ACTIVE", "LOCKED"]:
        raise HTTPException(status_code=400, detail="Trạng thái không hợp lệ! Chỉ chấp nhận ACTIVE hoặc LOCKED")
        
    tai_khoan = db.query(TaiKhoan).filter(TaiKhoan.id == id).first()
    if not tai_khoan:
        raise HTTPException(status_code=404, detail="Không tìm thấy tài khoản!")
        
    tai_khoan.trang_thai = trang_thai
    db.commit()
    return {"message": f"Đã cập nhật trạng thái tài khoản thành: {trang_thai}!"}

# 2. API Phân quyền - Gán danh sách vai trò cho tài khoản (Xử lý bảng quan hệ nhiều-nhiều vai_tros)
@router.put("/{id}/gan-vai-tro")
def gan_vai_tro_cho_tai_khoan(id: int, data: GanVaiTroRequest, db: Session = Depends(get_db)):
    # Tìm tài khoản cần phân quyền
    tai_khoan = db.query(TaiKhoan).filter(TaiKhoan.id == id).first()
    if not tai_khoan:
        raise HTTPException(status_code=404, detail="Không tìm thấy tài khoản này!")

    # Tìm các vai trò tương ứng trong DB dựa trên danh sách mã truyền lên
    vai_tro_tim_duoc = db.query(VaiTro).filter(VaiTro.ma_vai_tro.in_(data.ma_vai_tro_list)).all()
    if len(vai_tro_tim_duoc) != len(data.ma_vai_tro_list):
        raise HTTPException(status_code=400, detail="Có mã vai trò không tồn tại trong hệ thống!")

    # Cập nhật mối quan hệ nhiều-nhiều (SQLAlchemy tự động xử lý chèn vào bảng trung gian tai_khoan_vai_tro)
    tai_khoan.vai_tros = vai_tro_tim_duoc
    db.commit()

    return {
        "message": "Phân quyền vai trò cho tài khoản thành công!",
        "ten_dang_nhap": tai_khoan.ten_dang_nhap,
        "vai_tro_hien_tai": [vt.ma_vai_tro for vt in tai_khoan.vai_tros]
    }