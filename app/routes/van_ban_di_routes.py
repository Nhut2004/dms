from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from config.database import get_db

from app.models.document import VanBanDi
from app.schemas.van_ban_di_schema import VanBanDiCreate, VanBanDiResponse
from app.dependencies import lay_nguoi_dung_hien_tai
from app.models.auth import TaiKhoan

router = APIRouter(
    prefix="/api/van-ban-di",
    tags=["Quản lý Văn bản đi"]
)


@router.post("/", response_model=VanBanDiResponse)
def tao_van_ban_di(
    van_ban: VanBanDiCreate,
    db: Session = Depends(get_db),
    nguoi_dung: TaiKhoan = Depends(lay_nguoi_dung_hien_tai)
):
    van_ban_moi = VanBanDi(**van_ban.model_dump())
    db.add(van_ban_moi)
    db.commit()
    db.refresh(van_ban_moi)
    return van_ban_moi


@router.get("/", response_model=list[VanBanDiResponse])
def lay_danh_sach_van_ban_di(db: Session = Depends(get_db)):
    return db.query(VanBanDi).all()
