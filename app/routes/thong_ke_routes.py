# app/routes/thong_ke_routes.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from config.database import get_db
from app.dependencies import lay_nguoi_dung_hien_tai
from app.models.auth import TaiKhoan
from app.models.document import VanBanDi, VanBanDen
from app.models.core import HoSo

router = APIRouter(
    prefix="/api/thong-ke",
    tags=["Thống kê & Dashboard"]
)


@router.get("/tong-quan")
def thong_ke_tong_quan(
    db: Session = Depends(get_db),
    nguoi_dung: TaiKhoan = Depends(lay_nguoi_dung_hien_tai)
):
    # 1. Thống kê Văn bản đi
    tong_vb_di = db.query(VanBanDi).count()
    vb_di_theo_trang_thai = dict(db.query(VanBanDi.trang_thai, func.count(
        VanBanDi.id)).group_by(VanBanDi.trang_thai).all())

    # 2. Thống kê Văn bản đến
    tong_vb_den = db.query(VanBanDen).count()
    vb_den_theo_trang_thai = dict(db.query(VanBanDen.trang_thai_xu_ly, func.count(
        VanBanDen.id)).group_by(VanBanDen.trang_thai_xu_ly).all())

    # 3. Thống kê Hồ sơ
    tong_ho_so = db.query(HoSo).count()
    ho_so_theo_trang_thai = dict(
        db.query(HoSo.trang_thai, func.count(HoSo.ma_ho_so)).group_by(HoSo.trang_thai).all())
    return {
        "van_ban_di": {
            "tong": tong_vb_di,
            "trang_thai": {
                "DRAFT": vb_di_theo_trang_thai.get("DRAFT", 0),
                "PENDING_APPROVAL": vb_di_theo_trang_thai.get("PENDING_APPROVAL", 0),
                "PUBLISHED": vb_di_theo_trang_thai.get("PUBLISHED", 0),
                "REVOKED": vb_di_theo_trang_thai.get("REVOKED", 0)
            }
        },
        "van_ban_den": {
            "tong": tong_vb_den,
            "trang_thai": {
                "CHO_XU_LY": vb_den_theo_trang_thai.get("CHO_XU_LY", 0),
                "DANG_XU_LY": vb_den_theo_trang_thai.get("DANG_XU_LY", 0),
                "DA_XU_LY": vb_den_theo_trang_thai.get("DA_XU_LY", 0)
            }
        },
        "ho_so": {
            "tong": tong_ho_so,
            "trang_thai": {
                "DANG_MO": ho_so_theo_trang_thai.get("DANG_MO", 0),
                "DA_DONG": ho_so_theo_trang_thai.get("DA_DONG", 0)
            }
        }
    }
