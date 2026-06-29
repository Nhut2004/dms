from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.core import HoSo
from app.models.auth import TaiKhoan
from app.schemas.ho_so_schema import HoSoCreate, HoSoUpdate, HoSoResponse
from app.dependencies import lay_nguoi_dung_hien_tai
from config.database import get_db
from sqlalchemy import or_
router = APIRouter(
    prefix="/api/ho-so",
    tags=["Quản lý Hồ sơ"]
)


@router.post("/", response_model=HoSoResponse)
def tao_ho_so(
    ho_so: HoSoCreate,
    db: Session = Depends(get_db),
    nguoi_dung: TaiKhoan = Depends(lay_nguoi_dung_hien_tai)
):
    kiem_tra = db.query(HoSo).filter(HoSo.ma_ho_so == ho_so.ma_ho_so).first()
    if kiem_tra:
        raise HTTPException(status_code=400, detail="Mã hồ sơ đã tồn tại!")

    ho_so_moi = HoSo(**ho_so.model_dump())
    db.add(ho_so_moi)
    db.commit()
    db.refresh(ho_so_moi)
    return ho_so_moi


@router.get("/")
def lay_danh_sach_ho_so(
    page: int = 1,
    size: int = 10,
    keyword: str = None,
    db: Session = Depends(get_db),
    nguoi_dung: TaiKhoan = Depends(lay_nguoi_dung_hien_tai)
):
    query = db.query(HoSo)

    # 1. Logic tìm kiếm theo keyword (Mã hồ sơ hoặc Tiêu đề)
    if keyword:
        query = query.filter(
            or_(
                HoSo.ma_ho_so.ilike(f"%{keyword}%"),
                HoSo.tieu_de_ho_so.ilike(f"%{keyword}%")
            )
        )

    # 2. Đếm tổng số bản ghi (phục vụ phân trang UI)
    total = query.count()

    # 3. Áp dụng phân trang
    danh_sach = query.offset((page - 1) * size).limit(size).all()

    # 4. Trả về đúng cấu trúc chuẩn của hệ thống
    return {
        "data": danh_sach,
        "total": total
    }


@router.get("/{ma_ho_so}", response_model=HoSoResponse)
def lay_chi_tiet_ho_so(
    ma_ho_so: str,
    db: Session = Depends(get_db),
    nguoi_dung: TaiKhoan = Depends(lay_nguoi_dung_hien_tai)
):
    ho_so = db.query(HoSo).filter(HoSo.ma_ho_so == ma_ho_so).first()
    if not ho_so:
        raise HTTPException(status_code=404, detail="Không tìm thấy hồ sơ!")
    return ho_so


@router.put("/{ma_ho_so}", response_model=HoSoResponse)
def cap_nhat_ho_so(
    ma_ho_so: str,
    ho_so_update: HoSoUpdate,
    db: Session = Depends(get_db),
    nguoi_dung: TaiKhoan = Depends(lay_nguoi_dung_hien_tai)
):
    ho_so = db.query(HoSo).filter(HoSo.ma_ho_so == ma_ho_so).first()
    if not ho_so:
        raise HTTPException(status_code=404, detail="Không tìm thấy hồ sơ!")

    # Chỉ cập nhật các trường được truyền lên, không ghi đè None
    update_data = ho_so_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(ho_so, key, value)

    db.commit()
    db.refresh(ho_so)
    return ho_so


@router.delete("/{ma_ho_so}")
def xoa_ho_so(
    ma_ho_so: str,
    db: Session = Depends(get_db),
    nguoi_dung: TaiKhoan = Depends(lay_nguoi_dung_hien_tai)
):
    ho_so = db.query(HoSo).filter(HoSo.ma_ho_so == ma_ho_so).first()
    if not ho_so:
        raise HTTPException(status_code=404, detail="Không tìm thấy hồ sơ!")

    db.delete(ho_so)
    db.commit()
    return {"detail": "Xóa hồ sơ thành công!"}


@router.patch("/{ma_ho_so}/dong")
def dong_ho_so(
    ma_ho_so: str,
    db: Session = Depends(get_db),
    nguoi_dung: TaiKhoan = Depends(lay_nguoi_dung_hien_tai)
):
    ho_so = db.query(HoSo).filter(HoSo.ma_ho_so == ma_ho_so).first()
    if not ho_so:
        raise HTTPException(status_code=404, detail="Không tìm thấy hồ sơ")

    ho_so.trang_thai = "DA_DONG"
    db.commit()
    return {"message": "Đã đóng hồ sơ thành công!"}
