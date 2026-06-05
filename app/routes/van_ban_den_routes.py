from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from config.database import get_db
from app.models.van_ban_den import VanBanDen
from app.schemas.van_ban_den_schema import VanBanDenCreate, VanBanDenResponse

router = APIRouter(
    prefix="/api/van-ban-den",
    tags=["Quản lý Văn bản đến"]
)

# API 1: Tạo mới Văn bản đến


@router.post("/", response_model=VanBanDenResponse)
def tao_van_ban_den(van_ban: VanBanDenCreate, db: Session = Depends(get_db)):
    van_ban_moi = VanBanDen(**van_ban.model_dump())
    db.add(van_ban_moi)
    db.commit()
    db.refresh(van_ban_moi)
    return van_ban_moi

# API 2: Lấy danh sách Văn bản đến


@router.get("/", response_model=list[VanBanDenResponse])
def lay_danh_sach_van_ban_den(db: Session = Depends(get_db)):
    return db.query(VanBanDen).all()
