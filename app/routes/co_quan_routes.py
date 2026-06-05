from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from config.database import get_db
from app.models.co_quan_to_chuc import CoQuanToChuc
from app.schemas.co_quan_schema import CoQuanCreate, CoQuanResponse

router = APIRouter(
    prefix="/api/co-quan",
    tags=["Quản lý Cơ quan / Tổ chức"]
)

# API 1: Thêm mới một cơ quan
@router.post("/", response_model=CoQuanResponse)
def tao_co_quan(co_quan: CoQuanCreate, db: Session = Depends(get_db)):
    # Kiểm tra xem mã cơ quan đã tồn tại chưa
    db_co_quan = db.query(CoQuanToChuc).filter(CoQuanToChuc.organ_id == co_quan.organ_id).first()
    if db_co_quan:
        raise HTTPException(status_code=400, detail="Mã định danh cơ quan (OrganId) đã tồn tại!")
    
    # Tạo bản ghi mới
    co_quan_moi = CoQuanToChuc(**co_quan.model_dump())
    db.add(co_quan_moi)
    db.commit()
    db.refresh(co_quan_moi)
    
    return co_quan_moi

# API 2: Lấy danh sách tất cả cơ quan
@router.get("/", response_model=list[CoQuanResponse])
def lay_danh_sach_co_quan(db: Session = Depends(get_db)):
    return db.query(CoQuanToChuc).all()