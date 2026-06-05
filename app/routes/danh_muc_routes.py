from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from config.database import get_db
from app.models.danh_muc_loai_vb import DanhMucLoaiVb
from app.schemas.danh_muc_schema import DanhMucCreate, DanhMucResponse

router = APIRouter(
    prefix="/api/danh-muc",
    tags=["Quản lý Danh mục loại văn bản"]
)

# API Thêm loại văn bản mới
@router.post("/", response_model=DanhMucResponse)
def tao_danh_muc(danh_muc: DanhMucCreate, db: Session = Depends(get_db)):
    kiem_tra = db.query(DanhMucLoaiVb).filter(DanhMucLoaiVb.ten_loai_vb == danh_muc.ten_loai_vb).first()
    if kiem_tra:
        raise HTTPException(status_code=400, detail="Loại văn bản này đã tồn tại!")
    
    danh_muc_moi = DanhMucLoaiVb(**danh_muc.model_dump())
    db.add(danh_muc_moi)
    db.commit()
    db.refresh(danh_muc_moi)
    return danh_muc_moi

# API Lấy danh sách loại văn bản
@router.get("/", response_model=list[DanhMucResponse])
def lay_danh_sach_danh_muc(db: Session = Depends(get_db)):
    return db.query(DanhMucLoaiVb).all()