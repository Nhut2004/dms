from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import Response
from sqlalchemy.orm import Session
from config.database import get_db

# Import model từ file core mới
from app.models.core import CoQuanToChuc
from app.schemas.co_quan_schema import CoQuanCreate, CoQuanResponse

# Gắn thêm bảo vệ
from app.dependencies import lay_nguoi_dung_hien_tai, require_roles
from app.models.auth import TaiKhoan

router = APIRouter(
    prefix="/api/co-quan",
    tags=["Quản lý Cơ quan"]
)


@router.post("/", response_model=CoQuanResponse)
def tao_co_quan(
    co_quan: CoQuanCreate,
    db: Session = Depends(get_db),
    nguoi_dung: TaiKhoan = Depends(require_roles(["ADMIN", "VAN_THU"]))
):
    kiem_tra = db.query(CoQuanToChuc).filter(
        CoQuanToChuc.organ_id == co_quan.organ_id).first()
    if kiem_tra:
        raise HTTPException(
            status_code=400, detail="Mã định danh (organ_id) đã tồn tại!")

    co_quan_moi = CoQuanToChuc(**co_quan.model_dump())
    db.add(co_quan_moi)
    db.commit()
    db.refresh(co_quan_moi)
    return co_quan_moi


@router.get("/", response_model=list[CoQuanResponse])
def lay_danh_sach_co_quan(db: Session = Depends(get_db)):
    return db.query(CoQuanToChuc).order_by(CoQuanToChuc.id.desc()).all()


@router.put("/{id}", response_model=CoQuanResponse)
def cap_nhat_co_quan(
    id: int,
    co_quan: CoQuanCreate,
    db: Session = Depends(get_db),
    nguoi_dung: TaiKhoan = Depends(require_roles(["ADMIN", "VAN_THU"]))
):
    co_quan_hien_tai = db.query(CoQuanToChuc).filter(
        CoQuanToChuc.id == id).first()
    if not co_quan_hien_tai:
        raise HTTPException(status_code=404, detail="Không tìm thấy cơ quan")

    existing = db.query(CoQuanToChuc).filter(
        CoQuanToChuc.organ_id == co_quan.organ_id, CoQuanToChuc.id != id).first()
    if existing:
        raise HTTPException(
            status_code=400, detail="Mã định danh (organ_id) đã tồn tại!")

    co_quan_hien_tai.ten_co_quan = co_quan.ten_co_quan
    co_quan_hien_tai.organ_id = co_quan.organ_id
    co_quan_hien_tai.dia_chi = co_quan.dia_chi

    db.commit()
    db.refresh(co_quan_hien_tai)
    return co_quan_hien_tai


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def xoa_co_quan(
    id: int,
    db: Session = Depends(get_db),
    nguoi_dung: TaiKhoan = Depends(require_roles(["ADMIN", "VAN_THU"]))
):
    co_quan = db.query(CoQuanToChuc).filter(CoQuanToChuc.id == id).first()
    if not co_quan:
        raise HTTPException(status_code=404, detail="Không tìm thấy cơ quan")

    db.delete(co_quan)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
