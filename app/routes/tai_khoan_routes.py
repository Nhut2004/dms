from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from config.database import get_db
from app.models.tai_khoan_nguoi_dung import TaiKhoanNguoiDung
from app.schemas.tai_khoan_schema import TaiKhoanCreate, TaiKhoanResponse

# Cấu hình bộ mã hóa mật khẩu
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter(
    prefix="/api/tai-khoan",
    tags=["Quản lý Tài khoản Cán bộ"]
)

@router.post("/", response_model=TaiKhoanResponse)
def tao_tai_khoan(tai_khoan: TaiKhoanCreate, db: Session = Depends(get_db)):
    # 1. Kiểm tra xem tên đăng nhập đã có ai dùng chưa
    kiem_tra_user = db.query(TaiKhoanNguoiDung).filter(TaiKhoanNguoiDung.ten_dang_nhap == tai_khoan.ten_dang_nhap).first()
    if kiem_tra_user:
        raise HTTPException(status_code=400, detail="Tên đăng nhập đã tồn tại, vui lòng chọn tên khác!")
    
    # 2. Mã hóa mật khẩu trước khi lưu
    mat_khau_ma_hoa = pwd_context.hash(tai_khoan.mat_khau)
    
    # 3. Tạo bản ghi mới (Ghi đè mật khẩu gốc bằng mật khẩu đã mã hóa)
    tai_khoan_moi = TaiKhoanNguoiDung(
        co_quan_id=tai_khoan.co_quan_id,
        ho_ten=tai_khoan.ho_ten,
        chuc_vu=tai_khoan.chuc_vu,
        email=tai_khoan.email,
        ten_dang_nhap=tai_khoan.ten_dang_nhap,
        mat_khau=mat_khau_ma_hoa,
        vai_tro=tai_khoan.vai_tro
    )
    
    db.add(tai_khoan_moi)
    db.commit()
    db.refresh(tai_khoan_moi)
    
    return tai_khoan_moi

# API Lấy danh sách tất cả tài khoản
@router.get("/", response_model=list[TaiKhoanResponse])
def lay_danh_sach_tai_khoan(db: Session = Depends(get_db)):
    # Trả về toàn bộ danh sách tài khoản trong database
    return db.query(TaiKhoanNguoiDung).all()