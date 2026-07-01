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

# 1. API Lấy danh sách tất cả tệp đính kèm của MỘT VĂN BẢN CỤ THỂ (Đến hoặc Đi)
@router.get("/van-ban/{van_ban_id}", response_model=list[TepDinhKemResponse])
def lay_tep_dinh_kem_cua_van_ban(
    van_ban_id: int, 
    loai_vb: str, # Nhận vào query parameter: 'VAN_BAN_DEN' hoặc 'VAN_BAN_DI'
    db: Session = Depends(get_db),
    nguoi_dung: TaiKhoan = Depends(lay_nguoi_dung_hien_tai)
):
    if loai_vb not in ['VAN_BAN_DEN', 'VAN_BAN_DI']:
        raise HTTPException(status_code=400, detail="loai_vb phải là VAN_BAN_DEN hoặc VAN_BAN_DI")
        
    # Lọc file đính kèm dựa theo van_ban_id và phân loại văn bản tương ứng
    taps_dinh_kem = db.query(FileDinhKem).filter(
        FileDinhKem.van_ban_id == van_ban_id,
        FileDinhKem.loai_van_ban == loai_vb
    ).all()
    
    return taps_dinh_kem

# 2. API Xóa tệp đính kèm (Dùng khi người dùng muốn gỡ file đã đăng tải lên)
@router.delete("/{id}")
def xoa_tep_dinh_kem(
    id: int,
    db: Session = Depends(get_db),
    nguoi_dung: TaiKhoan = Depends(lay_nguoi_dung_hien_tai)
):
    tep_dinh_kem = db.query(FileDinhKem).filter(FileDinhKem.id == id).first()
    if not tep_dinh_kem:
        raise HTTPException(status_code=404, detail="Không tìm thấy tệp đính kèm này để xóa!")
        
    db.delete(tep_dinh_kem)
    db.commit()
    return {"message": "Xóa tệp đính kèm thành công!"}