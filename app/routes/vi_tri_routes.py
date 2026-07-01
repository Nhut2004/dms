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


from fastapi import HTTPException

# Schema Pydantic phục vụ cho việc tạo mới và cập nhật dữ liệu
class ViTriCreateInput(BaseModel):
    toa_nha: Optional[str] = None
    phong: Optional[str] = None
    ke_tu: Optional[str] = None
    ngan_tang: Optional[str] = None
    so_hop: Optional[str] = None
    ghi_chu: Optional[str] = None

# 1. API Thêm mới một vị trí lưu trữ vào kho
@router.post("/", response_model=ViTriDropdownResponse)
def tao_vi_tri_luu_tru(
    data: ViTriCreateInput,
    db: Session = Depends(get_db),
    nguoi_dung: TaiKhoan = Depends(lay_nguoi_dung_hien_tai)
):
    # Tạo bản ghi mới dựa trên cấu trúc bảng ViTriLuuTru
    vi_tri_moi = ViTriLuuTru(
        toa_nha=data.toa_nha,
        phong=data.phong,
        ke_tu=data.ke_tu,
        ngan_tang=data.ngan_tang,
        so_hop=data.so_hop,
        ghi_chu=data.ghi_chu
    )
    
    db.add(vi_tri_moi)
    db.commit()
    db.refresh(vi_tri_moi)
    
    # Format lại dữ liệu trả về giống cấu trúc Dropdown cho Frontend đồng nhất
    cac_thanh_phan = []
    if vi_tri_moi.toa_nha: cac_thanh_phan.append(f"Tòa {vi_tri_moi.toa_nha}")
    if vi_tri_moi.phong: cac_thanh_phan.append(f"Phòng {vi_tri_moi.phong}")
    if vi_tri_moi.ke_tu: cac_thanh_phan.append(f"Kệ {vi_tri_moi.ke_tu}")
    ten_hien_thi = " - ".join(cac_thanh_phan) if cac_thanh_phan else f"Vị trí ID: {vi_tri_moi.id}"
    
    return {"id": vi_tri_moi.id, "ten_vi_tri": ten_hien_thi}

# 2. API Cập nhật thông tin phòng/kệ/tủ của vị trí cũ
@router.put("/{id}", response_model=ViTriDropdownResponse)
def cap_nhat_vi_tri_luu_tru(
    id: int,
    data: ViTriCreateInput,
    db: Session = Depends(get_db),
    nguoi_dung: TaiKhoan = Depends(lay_nguoi_dung_hien_tai)
):
    vi_tri = db.query(ViTriLuuTru).filter(ViTriLuuTru.id == id).first()
    if not vi_tri:
        raise HTTPException(status_code=404, detail="Không tìm thấy vị trí lưu trữ này!")
        
    # Cập nhật các trường dữ liệu mới (Chỉ cập nhật nếu có gửi lên)
    if data.toa_nha is not None: vi_tri.toa_nha = data.toa_nha
    if data.phong is not None: vi_tri.phong = data.phong
    if data.ke_tu is not None: vi_tri.ke_tu = data.ke_tu
    if data.ngan_tang is not None: vi_tri.ngan_tang = data.ngan_tang
    if data.so_hop is not None: vi_tri.so_hop = data.so_hop
    if data.ghi_chu is not None: vi_tri.ghi_chu = data.ghi_chu
    
    db.commit()
    db.refresh(vi_tri)
    
    cac_thanh_phan = []
    if vi_tri.toa_nha: cac_thanh_phan.append(f"Tòa {vi_tri.toa_nha}")
    if vi_tri.phong: cac_thanh_phan.append(f"Phòng {vi_tri.phong}")
    if vi_tri.ke_tu: cac_thanh_phan.append(f"Kệ {vi_tri.ke_tu}")
    ten_hien_thi = " - ".join(cac_thanh_phan) if cac_thanh_phan else f"Vị trí ID: {vi_tri.id}"
    
    return {"id": vi_tri.id, "ten_vi_tri": ten_hien_thi}

# 3. API Xóa một vị trí lưu trữ ra khỏi hệ thống danh mục
@router.delete("/{id}")
def xoa_vi_tri_luu_tru(
    id: int,
    db: Session = Depends(get_db),
    nguoi_dung: TaiKhoan = Depends(lay_nguoi_dung_hien_tai)
):
    vi_tri = db.query(ViTriLuuTru).filter(ViTriLuuTru.id == id).first()
    if not vi_tri:
        raise HTTPException(status_code=404, detail="Không tìm thấy vị trí lưu trữ để xóa!")
        
    # Guard chặn xóa: Nếu có Hồ sơ lưu trữ nào đang nằm ở vị trí này thì KHÔNG ĐƯỢC XÓA (Tránh mồ côi dữ liệu)
    from app.models.core import HoSo
    ho_so_dang_dung = db.query(HoSo).filter(HoSo.vi_tri_luu_tru_id == id).first()
    if ho_so_dang_dung:
        raise HTTPException(
            status_code=400, 
            detail=f"Không được xóa! Vị trí này hiện đang được hồ sơ '{ho_so_dang_dung.tieu_de_ho_so}' đăng ký sử dụng!"
        )
        
    db.delete(vi_tri)
    db.commit()
    return {"message": "Đã xóa vị trí lưu trữ ra khỏi danh mục hệ thống thành công!"}