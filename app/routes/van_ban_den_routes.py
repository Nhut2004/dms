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

from fastapi import Query
from typing import Optional
from datetime import date

# API 3: Tìm kiếm và lọc Văn bản đến nâng cao
@router.get("/search", response_model=list[VanBanDenResponse])
def tim_kiem_van_ban_den(
    subject: Optional[str] = Query(None, description="Tìm theo trích yếu nội dung"),
    status: Optional[str] = Query(None, description="Lọc theo trạng thái xử lý"),
    priority: Optional[int] = Query(None, description="Lọc theo mức độ khẩn (1-5)"),
    db: Session = Depends(get_db)
):
    query = db.query(VanBanDen)
    
    # Tìm kiếm gần đúng (không phân biệt hoa thường với ilike) theo trích yếu
    if subject:
        query = query.filter(VanBanDen.subject.ilike(f"%{subject}%"))
        
    # Lọc theo trạng thái (Ví dụ: "Chờ xử lý", "Đang xử lý")
    if status:
        query = query.filter(VanBanDen.status == status)
        
    # Lọc theo độ khẩn của công văn
    if priority:
        query = query.filter(VanBanDen.priority == priority)
        
    return query.all()


# API 4: Cập nhật ý kiến chỉ đạo và Hạn giải quyết (Dành cho Lãnh đạo duyệt)
@router.patch("/{vb_id}/chi-dao", response_model=VanBanDenResponse)
def cap_nhat_y_kien_chi_dao(
    vb_id: int, 
    y_kien: str = Query(..., description="Ý kiến phân phối, chỉ đạo của lãnh đạo"),
    han_giai_quyet: Optional[date] = Query(None, description="Thời hạn giải quyết văn bản"),
    db: Session = Depends(get_db)
):
    # Tìm văn bản trong hệ thống theo ID
    vb = db.query(VanBanDen).filter(VanBanDen.id == vb_id).first()
    if not vb:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Không tìm thấy văn bản này cậu ơi!")
        
    # Tiến hành ghi nhận ý kiến và hạn chót xử lý vào các trường dữ liệu tương ứng
    vb.trace_header_list = y_kien
    if han_giai_quyet:
        vb.due_date = han_giai_quyet
        
    # Tự động chuyển trạng thái văn bản sang "Đang xử lý"
    vb.status = "Đang xử lý"
    
    db.commit()
    db.refresh(vb)
    return vb
