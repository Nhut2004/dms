from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from config.database import get_db

# Import model từ file core mới
from app.models.core import CoQuanToChuc
from app.schemas.co_quan_schema import CoQuanCreate, CoQuanResponse

# Gắn thêm bảo vệ
from app.dependencies import lay_nguoi_dung_hien_tai
from app.models.auth import TaiKhoan

router = APIRouter(
    prefix="/api/co-quan",
    tags=["Quản lý Cơ quan"]
)


@router.post("/", response_model=CoQuanResponse)
def tao_co_quan(
    co_quan: CoQuanCreate,
    db: Session = Depends(get_db),
    nguoi_dung: TaiKhoan = Depends(lay_nguoi_dung_hien_tai)  # Khóa API này lại
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
    return db.query(CoQuanToChuc).all()
