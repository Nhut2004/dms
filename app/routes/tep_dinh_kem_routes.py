from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from config.database import get_db

from app.models.document import FileDinhKem
from app.schemas.tep_dinh_kem_schema import TepDinhKemCreate, TepDinhKemResponse
from app.dependencies import lay_nguoi_dung_hien_tai
from app.models.auth import TaiKhoan

router = APIRouter(
    prefix="/api/tep-dinh-kem",
    tags=["Quản lý Tệp đính kèm"]
)


@router.post("/", response_model=TepDinhKemResponse)
def tao_tep_dinh_kem(
    tep: TepDinhKemCreate,
    db: Session = Depends(get_db),
    nguoi_dung: TaiKhoan = Depends(lay_nguoi_dung_hien_tai)
):
    # Kiểm tra ràng buộc cứng theo thiết kế DB
    if tep.loai_van_ban not in ['VAN_BAN_DEN', 'VAN_BAN_DI']:
        raise HTTPException(
            status_code=400, detail="loai_van_ban chỉ được là VAN_BAN_DEN hoặc VAN_BAN_DI")

    tep_moi = FileDinhKem(**tep.model_dump())
    db.add(tep_moi)
    db.commit()
    db.refresh(tep_moi)
    return tep_moi


@router.get("/", response_model=list[TepDinhKemResponse])
def lay_danh_sach(db: Session = Depends(get_db)):
    return db.query(FileDinhKem).all()
