from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from config.database import get_db
from app.models.van_ban_di import VanBanDi
from app.schemas.van_ban_di_schema import VanBanDiCreate, VanBanDiResponse

router = APIRouter(
    prefix="/api/van-ban-di",
    tags=["Quản lý Văn bản đi"]
)

# API 1: Tạo mới Văn bản đi


@router.post("/", response_model=VanBanDiResponse)
def tao_van_ban_di(van_ban: VanBanDiCreate, db: Session = Depends(get_db)):
    van_ban_moi = VanBanDi(**van_ban.model_dump())
    db.add(van_ban_moi)
    db.commit()
    db.refresh(van_ban_moi)
    return van_ban_moi

# API 2: Lấy danh sách Văn bản đi


@router.get("/", response_model=list[VanBanDiResponse])
def lay_danh_sach_van_ban_di(db: Session = Depends(get_db)):
    return db.query(VanBanDi).all()
