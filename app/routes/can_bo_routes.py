from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import Response
from sqlalchemy.orm import Session
from typing import List
from config.database import get_db
from app.models.auth import CanBo
from app.schemas.can_bo_schema import CanBoCreate, CanBoResponse, CanBoUpdate
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
    return db.query(CanBo).order_by(CanBo.id.desc()).all()


@router.post("/", response_model=CanBoResponse, status_code=status.HTTP_201_CREATED)
def tao_can_bo(
    payload: CanBoCreate,
    db: Session = Depends(get_db),
    nguoi_dung: TaiKhoan = Depends(lay_nguoi_dung_hien_tai)
):
    can_bo = CanBo(**payload.model_dump())
    db.add(can_bo)
    db.commit()
    db.refresh(can_bo)
    return can_bo


@router.put("/{id}", response_model=CanBoResponse)
def cap_nhat_can_bo(
    id: int,
    payload: CanBoUpdate,
    db: Session = Depends(get_db),
    nguoi_dung: TaiKhoan = Depends(lay_nguoi_dung_hien_tai)
):
    can_bo = db.query(CanBo).filter(CanBo.id == id).first()
    if not can_bo:
        raise HTTPException(status_code=404, detail="Không tìm thấy cán bộ")

    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(can_bo, key, value)

    db.commit()
    db.refresh(can_bo)
    return can_bo


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def xoa_can_bo(
    id: int,
    db: Session = Depends(get_db),
    nguoi_dung: TaiKhoan = Depends(lay_nguoi_dung_hien_tai)
):
    can_bo = db.query(CanBo).filter(CanBo.id == id).first()
    if not can_bo:
        raise HTTPException(status_code=404, detail="Không tìm thấy cán bộ")

    db.delete(can_bo)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
