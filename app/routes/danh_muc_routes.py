from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from config.database import get_db

from app.models.core import DanhMucLoaiVb
from app.schemas.danh_muc_schema import DanhMucCreate, DanhMucResponse
from app.dependencies import lay_nguoi_dung_hien_tai
from app.models.auth import TaiKhoan

router = APIRouter(
    prefix="/api/danh-muc",
    tags=["Quản lý Danh mục"]
)


@router.post("/", response_model=DanhMucResponse)
def tao_danh_muc(
    danh_muc: DanhMucCreate,
    db: Session = Depends(get_db),
    nguoi_dung: TaiKhoan = Depends(lay_nguoi_dung_hien_tai)
):
    kiem_tra = db.query(DanhMucLoaiVb).filter(
        DanhMucLoaiVb.ten_loai_vb == danh_muc.ten_loai_vb).first()
    if kiem_tra:
        raise HTTPException(
            status_code=400, detail="Tên loại văn bản đã tồn tại!")

    danh_muc_moi = DanhMucLoaiVb(**danh_muc.model_dump())
    db.add(danh_muc_moi)
    db.commit()
    db.refresh(danh_muc_moi)
    return danh_muc_moi


@router.get("/", response_model=list[DanhMucResponse])
def lay_danh_sach_danh_muc(
    db: Session = Depends(get_db),
    nguoi_dung: TaiKhoan = Depends(lay_nguoi_dung_hien_tai)
):
    return db.query(DanhMucLoaiVb).all()
