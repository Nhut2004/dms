from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from config.database import get_db
from sqlalchemy import func, or_
from app.models.document import VanBanDen
from app.schemas.van_ban_den_schema import VanBanDenCreate, VanBanDenUpdate, VanBanDenResponse, PhanPhoiInput, TienDoInput
from app.dependencies import lay_nguoi_dung_hien_tai
from app.models.auth import TaiKhoan, CanBo
from app.models.document import VanBanDen, FileDinhKem
from app.models.core import HoSo
import os
import shutil
from fastapi import UploadFile, File
from typing import List
from pydantic import BaseModel
router = APIRouter(
    prefix="/api/van-ban-den",
    tags=["Quản lý Văn bản đến"]
)


@router.post("/", response_model=VanBanDenResponse)
def tao_van_ban_den(
    van_ban: VanBanDenCreate,
    db: Session = Depends(get_db),
    nguoi_dung: TaiKhoan = Depends(lay_nguoi_dung_hien_tai)
):
    # 1. Guard: Chặn hồ sơ đã đóng (Giữ nguyên)
    if van_ban.ma_ho_so:
        ho_so = db.query(HoSo).filter(
            HoSo.ma_ho_so == van_ban.ma_ho_so).first()
        if ho_so and ho_so.trang_thai == "DA_DONG":
            raise HTTPException(
                status_code=400,
                detail=f"Hồ sơ {van_ban.ma_ho_so} đã đóng, không thể thêm văn bản!"
            )

    # 2. XỬ LÝ SỐ ĐẾN THÔNG MINH (Thay thế đoạn raise HTTPException cũ)
    kiem_tra = db.query(VanBanDen).filter(
        VanBanDen.so_den == van_ban.so_den).first()
    if kiem_tra:
        # Nếu số người dùng nhập đã bị trùng, hệ thống tự động tìm số lớn nhất và cộng 1
        max_so_den = db.query(func.max(VanBanDen.so_den)).scalar() or 0
        van_ban.so_den = max_so_den + 1
        # (Không báo lỗi 400 cản trở người dùng nữa)

    # --- BLOCK VALIDATE NGHIỆP VỤ (Giữ nguyên phần Ngày tháng, Số trang...) ---
    if van_ban.han_giai_quyet and van_ban.ngay_den:
        if van_ban.han_giai_quyet < van_ban.ngay_den:
            raise HTTPException(
                status_code=400,
                detail="Lỗi nghiệp vụ: Hạn giải quyết KHÔNG ĐƯỢC trước Ngày đến!"
            )

    if van_ban.so_trang is not None and van_ban.so_trang < 0:
        raise HTTPException(
            status_code=400,
            detail="Lỗi dữ liệu: Số trang không được là số âm!"
        )
    # --------------------------------

    van_ban_moi = VanBanDen(**van_ban.model_dump())
    db.add(van_ban_moi)
    db.commit()
    db.refresh(van_ban_moi)
    return van_ban_moi


@router.get("/")
def lay_danh_sach_van_ban_den(
    page: int = 1,
    size: int = 10,
    keyword: str = None,  # Thêm tham số tìm kiếm
    db: Session = Depends(get_db),
    nguoi_dung: TaiKhoan = Depends(lay_nguoi_dung_hien_tai)
):
    query = db.query(VanBanDen)

    # Nếu có từ khóa, lọc dữ liệu
    if keyword:
        query = query.filter(
            VanBanDen.trich_yeu.contains(keyword) |
            VanBanDen.ky_hieu.contains(keyword)
        )

    total = query.count()
    danh_sach = query.offset((page - 1) * size).limit(size).all()
    return {"data": danh_sach, "total": total}


@router.put("/{van_ban_id}", response_model=VanBanDenResponse)
def cap_nhat_van_ban_den(
    van_ban_id: int,
    van_ban_update: VanBanDenUpdate,
    db: Session = Depends(get_db),
    nguoi_dung: TaiKhoan = Depends(lay_nguoi_dung_hien_tai)
):
    db_van_ban = db.query(VanBanDen).filter(VanBanDen.id == van_ban_id).first()
    if not db_van_ban:
        raise HTTPException(
            status_code=404, detail="Không tìm thấy văn bản đến này!")

    ma_ho_so_moi = van_ban_update.ma_ho_so if van_ban_update.ma_ho_so is not None else db_van_ban.ma_ho_so
    if ma_ho_so_moi:
        ho_so = db.query(HoSo).filter(HoSo.ma_ho_so == ma_ho_so_moi).first()
        if ho_so and ho_so.trang_thai == "DA_DONG":
            raise HTTPException(
                status_code=400,
                detail=f"Hồ sơ {ma_ho_so_moi} đã đóng, không thể đưa văn bản vào đây!"
            )

    # --- BLOCK VALIDATE NGHIỆP VỤ KHI CẬP NHẬT ---
    ngay_den_check = van_ban_update.ngay_den if van_ban_update.ngay_den else db_van_ban.ngay_den
    han_giai_quyet_check = van_ban_update.han_giai_quyet if van_ban_update.han_giai_quyet else db_van_ban.han_giai_quyet

    if han_giai_quyet_check and ngay_den_check:
        if han_giai_quyet_check < ngay_den_check:
            raise HTTPException(
                status_code=400,
                detail="Lỗi nghiệp vụ: Hạn giải quyết KHÔNG ĐƯỢC trước Ngày đến!"
            )

    so_trang_check = van_ban_update.so_trang if van_ban_update.so_trang is not None else db_van_ban.so_trang
    if so_trang_check is not None and so_trang_check < 0:
        raise HTTPException(
            status_code=400,
            detail="Lỗi dữ liệu: Số trang không được là số âm!"
        )
    # --------------------------------

    # Cập nhật các trường có dữ liệu gửi lên
    update_data = van_ban_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_van_ban, key, value)

    db.commit()
    db.refresh(db_van_ban)
    return db_van_ban


@router.delete("/{van_ban_id}")
def xoa_van_ban_den(
    van_ban_id: int,
    db: Session = Depends(get_db),
    nguoi_dung: TaiKhoan = Depends(lay_nguoi_dung_hien_tai)
):
    db_van_ban = db.query(VanBanDen).filter(VanBanDen.id == van_ban_id).first()
    if not db_van_ban:
        raise HTTPException(
            status_code=404, detail="Không tìm thấy văn bản đến này!")

    db.delete(db_van_ban)
    db.commit()
    return {"message": "Đã xóa văn bản đến thành công!"}


@router.get("/{van_ban_id}", response_model=VanBanDenResponse)
def lay_chi_tiet_van_ban_den(
    van_ban_id: int,
    db: Session = Depends(get_db),
    nguoi_dung: TaiKhoan = Depends(lay_nguoi_dung_hien_tai)
):
    db_van_ban = db.query(VanBanDen).filter(VanBanDen.id == van_ban_id).first()
    if not db_van_ban:
        raise HTTPException(
            status_code=404, detail="Không tìm thấy văn bản đến này!")

    return db_van_ban


# Tạo sẵn thư mục trên ổ cứng để chứa file văn bản đến
UPLOAD_DIR = "uploads/van_ban_den"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/{van_ban_id}/upload", summary="Tải file đính kèm cho Văn bản đến")
def upload_file_van_ban_den(
    van_ban_id: int,
    files: List[UploadFile] = File(...),
    db: Session = Depends(get_db),
    nguoi_dung: TaiKhoan = Depends(lay_nguoi_dung_hien_tai)
):
    db_van_ban = db.query(VanBanDen).filter(VanBanDen.id == van_ban_id).first()
    if not db_van_ban:
        raise HTTPException(
            status_code=404, detail="Không tìm thấy văn bản để đính kèm!")

    saved_files = []
    file_responses = []
    for file in files:
        # Tạo tên file an toàn: Thêm ID văn bản đằng trước để không bị trùng tên
        file_path = os.path.join(UPLOAD_DIR, f"{van_ban_id}_{file.filename}")

        # Lưu file vật lý vào ổ cứng
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Tính toán định dạng và dung lượng
        ext = file.filename.split(
            ".")[-1].lower() if "." in file.filename else None
        file_size = os.path.getsize(file_path)

        # Đổi dấu \\ thành / để đường dẫn đồng nhất và không bị lỗi hiển thị trên React
        normalized_path = file_path.replace("\\", "/")

        new_file = FileDinhKem(
            ten_file=file.filename,
            duong_dan=normalized_path,
            van_ban_id=van_ban_id,
            loai_van_ban="VAN_BAN_DEN",
            dinh_dang=ext,
            dung_luong=float(file_size / 1024),
        )
        db.add(new_file)
        file_responses.append({
            "id": None,  # sẽ được fill sau commit nếu cần
            "ten_file": file.filename,
            "duong_dan": normalized_path,
            "dinh_dang": ext,
            "dung_luong": float(file_size / 1024),
        })

    db.commit()
    # Refresh để lấy ID cho các file mới tạo
    db.refresh(db_van_ban)
    return {"message": f"Đã tải lên {len(file_responses)} file thành công!", "files": file_responses}

# --- BLOCK API PHÂN PHỐI VÀ XỬ LÝ VĂN BẢN ĐẾN ---


@router.patch("/{id}/phan-phoi")
def phan_phoi_van_ban_den(
    id: int,
    data: PhanPhoiInput,
    db: Session = Depends(get_db),
    nguoi_dung: TaiKhoan = Depends(lay_nguoi_dung_hien_tai)
):
    van_ban = db.query(VanBanDen).filter(VanBanDen.id == id).first()
    if not van_ban:
        raise HTTPException(
            status_code=404, detail="Không tìm thấy văn bản đến!")

    can_bo = db.query(CanBo).filter(CanBo.id == data.nguoi_xu_ly_id).first()
    if not can_bo:
        raise HTTPException(
            status_code=400, detail="Cán bộ xử lý không tồn tại!")

    van_ban.nguoi_xu_ly_id = data.nguoi_xu_ly_id
    van_ban.trang_thai_xu_ly = 'DANG_XU_LY'
    db.commit()
    db.refresh(van_ban)

    return {"message": f"Đã phân phối văn bản cho {can_bo.ho_ten} thành công!"}


@router.patch("/{id}/tien-do")
def cap_nhat_tien_do_van_ban(
    id: int,
    data: TienDoInput,
    db: Session = Depends(get_db),
    nguoi_dung: TaiKhoan = Depends(lay_nguoi_dung_hien_tai)
):
    van_ban = db.query(VanBanDen).filter(VanBanDen.id == id).first()
    if not van_ban:
        raise HTTPException(
            status_code=404, detail="Không tìm thấy văn bản đến!")

    van_ban.trang_thai_xu_ly = data.trang_thai_xu_ly
    db.commit()
    db.refresh(van_ban)

    return {"message": "Cập nhật tiến độ xử lý thành công!"}
