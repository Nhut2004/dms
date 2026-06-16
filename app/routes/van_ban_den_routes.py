from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from config.database import get_db

from app.models.document import VanBanDen
from app.schemas.van_ban_den_schema import VanBanDenCreate, VanBanDenResponse
from app.dependencies import lay_nguoi_dung_hien_tai
from app.models.auth import TaiKhoan

router = APIRouter(
    prefix="/api/van-ban-den",
    tags=["Quản lý Văn bản đến"]
)


@router.post("/", response_model=VanBanDenResponse)
def tao_van_ban_den(
    van_ban: VanBanDenCreate,
    db: Session = Depends(get_db),
    nguoi_dung: TaiKhoan = Depends(lay_nguoi_dung_hien_tai)
):
    kiem_tra = db.query(VanBanDen).filter(
        VanBanDen.so_den == van_ban.so_den).first()
    if kiem_tra:
        raise HTTPException(
            status_code=400, detail="Số đến đã tồn tại trong hệ thống!")

    van_ban_moi = VanBanDen(**van_ban.model_dump())
    db.add(van_ban_moi)
    db.commit()
    db.refresh(van_ban_moi)
    return van_ban_moi


@router.get("/", response_model=list[VanBanDenResponse])
def lay_danh_sach_van_ban_den(db: Session = Depends(get_db)):
    return db.query(VanBanDen).all()
