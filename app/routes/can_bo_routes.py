from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from config.database import get_db
from app.models.auth import CanBo
from app.schemas.can_bo_schema import CanBoResponse
from app.dependencies import lay_nguoi_dung_hien_tai
from app.models.auth import TaiKhoan

router = APIRouter(
    prefix="/api/can-bo",
    tags=["Quản lý Cán bộ"]
)


@router.get("/", response_model=List[CanBoResponse])
def lay_danh_sach_can_bo(
    db: Session = Depends(get_db),
    nguoi_dung: TaiKhoan = Depends(lay_nguoi_dung_hien_tai)
):
    return db.query(CanBo).all()
