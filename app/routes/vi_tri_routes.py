from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel  # Thêm import này
from config.database import get_db
from app.models.core import ViTriLuuTru
from app.dependencies import lay_nguoi_dung_hien_tai
from app.models.auth import TaiKhoan

router = APIRouter(
    prefix="/api/danh-muc-vi-tri",
    tags=["Danh mục Vị trí lưu trữ"]
)

# 1. Tạo Schema chuẩn cho dữ liệu trả về (Phục vụ Swagger & Frontend)


class ViTriDropdownResponse(BaseModel):
    id: int
    ten_vi_tri: str

    class Config:
        from_attributes = True

# 2. Gắn response_model vào API


@router.get("/", response_model=list[ViTriDropdownResponse])
def lay_danh_sach_vi_tri(
    db: Session = Depends(get_db),
    nguoi_dung: TaiKhoan = Depends(lay_nguoi_dung_hien_tai)
):
    """API trả về danh sách toàn bộ vị trí lưu trữ để đổ vào Dropdown"""
    danh_sach = db.query(ViTriLuuTru).all()

    # Format lại dữ liệu để trả về đúng trường "ten_vi_tri" mà Frontend cần
    ket_qua = []
    for vi_tri in danh_sach:
        cac_thanh_phan = []
        if vi_tri.toa_nha:
            cac_thanh_phan.append(f"Tòa {vi_tri.toa_nha}")
        if vi_tri.phong:
            cac_thanh_phan.append(f"Phòng {vi_tri.phong}")
        if vi_tri.ke_tu:
            cac_thanh_phan.append(f"Kệ {vi_tri.ke_tu}")

        ten_hien_thi = " - ".join(
            cac_thanh_phan) if cac_thanh_phan else f"Vị trí ID: {vi_tri.id}"

        ket_qua.append({
            "id": vi_tri.id,
            "ten_vi_tri": ten_hien_thi
        })

    return ket_qua
