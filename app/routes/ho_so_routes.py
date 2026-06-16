from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from config.database import get_db

from app.models.core import HoSo
from app.schemas.ho_so_schema import HoSoCreate, HoSoResponse
from app.dependencies import lay_nguoi_dung_hien_tai
from app.models.auth import TaiKhoan

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


@router.get("/", response_model=list[HoSoResponse])
def lay_danh_sach_ho_so(db: Session = Depends(get_db)):
    return db.query(HoSo).all()
