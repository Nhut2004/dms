import os
import shutil
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from config.database import get_db
from app.models.tep_dinh_kem import TepDinhKem
from app.schemas.tep_dinh_kem_schema import TepDinhKemResponse

router = APIRouter(
    prefix="/api/tep-dinh-kem",
    tags=["Quản lý Tệp đính kèm (Upload File)"]
)

# Tạo thư mục chứa file nếu chưa có
UPLOAD_DIR = "uploads"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

# API: Tải file lên hệ thống


@router.post("/", response_model=TepDinhKemResponse)
def tai_len_tep(
    file: UploadFile = File(...),
    tep_chinh: int = Form(1, description="1: File chính, 0: Phụ lục"),
    loai_van_ban: str = Form(...,
                             description="Nhập 'van_ban_den' hoặc 'van_ban_di'"),
    van_ban_id: int = Form(..., description="ID của văn bản tương ứng"),
    nguoi_tai_len_id: int = Form(...,
                                 description="ID của tài khoản người dùng"),
    db: Session = Depends(get_db)
):
    try:
        # 1. Xử lý lưu file vật lý vào thư mục 'uploads'
        file_location = f"{UPLOAD_DIR}/{file.filename}"
        with open(file_location, "wb+") as file_object:
            shutil.copyfileobj(file.file, file_object)

        # 2. Lấy thông tin tệp (Dung lượng MB và định dạng)
        file_size_mb = os.path.getsize(file_location) / (1024 * 1024)
        file_extension = file.filename.split(
            ".")[-1] if "." in file.filename else "unknown"

        # 3. Lưu thông tin vào Database
        tep_moi = TepDinhKem(
            ten_tep=file.filename,
            duong_dan=file_location,
            dinh_dang=file_extension,
            kich_thuoc=round(file_size_mb, 2),  # Làm tròn 2 chữ số thập phân
            tep_chinh=tep_chinh,
            loai_van_ban=loai_van_ban,
            van_ban_id=van_ban_id,
            nguoi_tai_len_id=nguoi_tai_len_id
        )

        db.add(tep_moi)
        db.commit()
        db.refresh(tep_moi)

        return tep_moi

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Lỗi khi tải file: {str(e)}")
