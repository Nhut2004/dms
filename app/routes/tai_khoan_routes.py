from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from config.database import get_db
from app.models.auth import TaiKhoan, VaiTro
from app.schemas.tai_khoan_schema import TaiKhoanCreate, TaiKhoanResponse, VaiTroResponse
from app.dependencies import require_roles
from passlib.context import CryptContext

router = APIRouter(prefix="/api/tai-khoan", tags=["Quản lý Tài khoản"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.get("/vai-tro", response_model=list[VaiTroResponse])
def lay_danh_sach_vai_tro(db: Session = Depends(get_db)):
    return db.query(VaiTro).all()


@router.get("/", response_model=list[TaiKhoanResponse])
def lay_danh_sach_tai_khoan(db: Session = Depends(get_db), current_user=Depends(require_roles(["ADMIN"]))):
    return db.query(TaiKhoan).options(joinedload(TaiKhoan.vai_tros)).order_by(TaiKhoan.id.desc()).all()


@router.post("/", response_model=TaiKhoanResponse)
def tao_tai_khoan(payload: TaiKhoanCreate, db: Session = Depends(get_db), current_user=Depends(require_roles(["ADMIN"]))):
    kiem_tra = db.query(TaiKhoan).filter(
        TaiKhoan.ten_dang_nhap == payload.ten_dang_nhap).first()
    if kiem_tra:
        raise HTTPException(
            status_code=400, detail="Tên đăng nhập đã tồn tại!")

    hashed_password = pwd_context.hash(payload.mat_khau)
    tk_moi = TaiKhoan(
        ten_dang_nhap=payload.ten_dang_nhap,
        mat_khau_hash=hashed_password,
        can_bo_id=payload.can_bo_id
    )

    if payload.vai_tro_ids:
        vai_tros = db.query(VaiTro).filter(
            VaiTro.id.in_(payload.vai_tro_ids)).all()
        tk_moi.vai_tros = vai_tros

    db.add(tk_moi)
    db.commit()

    # TRỌNG TÂM: Truy vấn lại có joinedload để đảm bảo response nạp đủ quan hệ vai_tros
    tk_moi = db.query(TaiKhoan).options(joinedload(
        TaiKhoan.vai_tros)).filter(TaiKhoan.id == tk_moi.id).first()
    return tk_moi


# API Cập nhật tài khoản (Sửa)
@router.put("/{id}", response_model=TaiKhoanResponse)
def cap_nhat_tai_khoan(id: int, payload: TaiKhoanCreate, db: Session = Depends(get_db), current_user=Depends(require_roles(["ADMIN"]))):
    tk_hien_tai = db.query(TaiKhoan).filter(TaiKhoan.id == id).first()
    if not tk_hien_tai:
        raise HTTPException(
            status_code=404, detail="Không tìm thấy tài khoản!")

    # Cập nhật thông tin cơ bản
    tk_hien_tai.ten_dang_nhap = payload.ten_dang_nhap
    tk_hien_tai.can_bo_id = payload.can_bo_id

    # Nếu người dùng có nhập mật khẩu mới thì mới cập nhật
    if payload.mat_khau:
        tk_hien_tai.mat_khau_hash = pwd_context.hash(payload.mat_khau)

    # Cập nhật vai trò
    if payload.vai_tro_ids is not None:
        vai_tros = db.query(VaiTro).filter(
            VaiTro.id.in_(payload.vai_tro_ids)).all()
        tk_hien_tai.vai_tros = vai_tros

    db.commit()
    tk_hien_tai = db.query(TaiKhoan).options(joinedload(
        TaiKhoan.vai_tros)).filter(TaiKhoan.id == id).first()
    return tk_hien_tai

# API Xóa tài khoản


@router.delete("/{id}")
def xoa_tai_khoan(id: int, db: Session = Depends(get_db), current_user=Depends(require_roles(["ADMIN"]))):
    tk_can_xoa = db.query(TaiKhoan).filter(TaiKhoan.id == id).first()
    if not tk_can_xoa:
        raise HTTPException(
            status_code=404, detail="Không tìm thấy tài khoản!")

    # Bảo mật: Không cho phép Admin tự xóa chính mình
    if tk_can_xoa.id == current_user.id:
        raise HTTPException(
            status_code=400, detail="Bạn không thể tự xóa tài khoản của chính mình!")

    db.delete(tk_can_xoa)
    db.commit()
    return {"message": "Xóa thành công"}
