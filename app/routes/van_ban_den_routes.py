from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from config.database import get_db

from app.models.document import VanBanDen
from app.schemas.van_ban_den_schema import VanBanDenCreate, VanBanDenUpdate, VanBanDenResponse
from app.dependencies import lay_nguoi_dung_hien_tai
from app.models.auth import TaiKhoan
from app.models.document import VanBanDen, FileDinhKem

import os
import shutil
from fastapi import UploadFile, File
from typing import List

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


@router.put("/{van_ban_id}", response_model=VanBanDenResponse)
def cap_nhat_van_ban_den(
    van_ban_id: int,
    van_ban_update: VanBanDenUpdate,
    db: Session = Depends(get_db),
    nguoi_dung: TaiKhoan = Depends(lay_nguoi_dung_hien_tai)
):
    db_van_ban = db.query(VanBanDen).filter(VanBanDen.id == van_ban_id).first()
    if not db_van_ban:
        raise HTTPException(
            status_code=404, detail="Không tìm thấy văn bản đến này!")

    # Cập nhật các trường có dữ liệu gửi lên
    update_data = van_ban_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_van_ban, key, value)

    db.commit()
    db.refresh(db_van_ban)
    return db_van_ban


@router.delete("/{van_ban_id}")
def xoa_van_ban_den(
    van_ban_id: int,
    db: Session = Depends(get_db),
    nguoi_dung: TaiKhoan = Depends(lay_nguoi_dung_hien_tai)
):
    db_van_ban = db.query(VanBanDen).filter(VanBanDen.id == van_ban_id).first()
    if not db_van_ban:
        raise HTTPException(
            status_code=404, detail="Không tìm thấy văn bản đến này!")

    db.delete(db_van_ban)
    db.commit()
    return {"message": "Đã xóa văn bản đến thành công!"}


@router.get("/{van_ban_id}", response_model=VanBanDenResponse)
def lay_chi_tiet_van_ban_den(
    van_ban_id: int,
    db: Session = Depends(get_db),
    nguoi_dung: TaiKhoan = Depends(lay_nguoi_dung_hien_tai)
):
    db_van_ban = db.query(VanBanDen).filter(VanBanDen.id == van_ban_id).first()
    if not db_van_ban:
        raise HTTPException(
            status_code=404, detail="Không tìm thấy văn bản đến này!")

    return db_van_ban


# Tạo sẵn thư mục trên ổ cứng để chứa file văn bản đến
UPLOAD_DIR = "uploads/van_ban_den"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/{van_ban_id}/upload", summary="Tải file đính kèm cho Văn bản đến")
def upload_file_van_ban_den(
    van_ban_id: int,
    files: List[UploadFile] = File(...),
    db: Session = Depends(get_db),
    nguoi_dung: TaiKhoan = Depends(lay_nguoi_dung_hien_tai)
):
    db_van_ban = db.query(VanBanDen).filter(VanBanDen.id == van_ban_id).first()
    if not db_van_ban:
        raise HTTPException(
            status_code=404, detail="Không tìm thấy văn bản để đính kèm!")

    saved_files = []
    for file in files:
        # Tạo tên file an toàn: Thêm ID văn bản đằng trước để không bị trùng tên
        file_path = os.path.join(UPLOAD_DIR, f"{van_ban_id}_{file.filename}")

        # Lưu file vật lý vào ổ cứng
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        saved_files.append(file.filename)

        new_file = FileDinhKem(
            ten_file=file.filename,
            duong_dan=file_path,
            van_ban_id=van_ban_id,
            loai_van_ban="VAN_BAN_DEN"
        )
        db.add(new_file)

    db.commit()  # Mở comment dòng này nếu có lưu vào DB ở trên
    return {"message": f"Đã tải lên {len(saved_files)} file thành công!", "files": saved_files}
