from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from config.database import get_db
from app.models.ho_so import HoSoLuuTru
from app.schemas.ho_so_schema import HoSoCreate, HoSoResponse

router = APIRouter(
    prefix="/api/ho-so",
    tags=["Quản lý Hồ sơ lưu trữ"]
)

# API 1: Tạo hồ sơ mới


@router.post("/", response_model=HoSoResponse)
def tao_ho_so(ho_so: HoSoCreate, db: Session = Depends(get_db)):
    ho_so_moi = HoSoLuuTru(**ho_so.model_dump())
    db.add(ho_so_moi)
    db.commit()
    db.refresh(ho_so_moi)
    return ho_so_moi

# API 2: Lấy danh sách hồ sơ


@router.get("/", response_model=list[HoSoResponse])
def lay_danh_sach_ho_so(db: Session = Depends(get_db)):
    return db.query(HoSoLuuTru).all()
