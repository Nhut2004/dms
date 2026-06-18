from datetime import date
from pathlib import Path
from typing import Annotated, List, Optional

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session
from config.database import get_db

from app.models.document import FileDinhKem, VanBanDi
from app.schemas.van_ban_di_schema import VanBanDiCreate, VanBanDiResponse
from app.dependencies import lay_nguoi_dung_hien_tai
from app.models.auth import TaiKhoan

router = APIRouter(
    prefix="/api/van-ban-di",
    tags=["Quản lý Văn bản đi"]
)


@router.post("/", response_model=VanBanDiResponse)
async def tao_van_ban_di(
    so_ky_hieu: Annotated[Optional[str], Form()] = None,
    ngay_ban_hanh: Annotated[Optional[date], Form()] = None,
    trich_yeu: Annotated[str, Form()] = None,
    don_vi_soan_thao_id: Annotated[int, Form()] = None,
    ma_loai_vb_id: Annotated[int, Form()] = None,
    ngon_ngu: Annotated[Optional[str], Form()] = None,
    so_trang: Annotated[Optional[int], Form()] = None,
    ghi_chu: Annotated[Optional[str], Form()] = None,
    nguoi_ky_id: Annotated[Optional[int], Form()] = None,
    chuc_vu_nguoi_ky: Annotated[Optional[str], Form()] = None,
    noi_nhan: Annotated[Optional[str], Form()] = None,
    muc_do_khan: Annotated[Optional[int], Form()] = None,
    han_tra_loi: Annotated[Optional[date], Form()] = None,
    stt_trong_ho_so: Annotated[Optional[int], Form()] = None,
    ma_ho_so: Annotated[Optional[str], Form()] = None,
    files: List[UploadFile] = File(default=[]),
    db: Session = Depends(get_db),
    nguoi_dung: TaiKhoan = Depends(lay_nguoi_dung_hien_tai)
):
    van_ban_data = VanBanDiCreate(
        so_ky_hieu=so_ky_hieu,
        ngay_ban_hanh=ngay_ban_hanh,
        trich_yeu=trich_yeu,
        don_vi_soan_thao_id=don_vi_soan_thao_id,
        ma_loai_vb_id=ma_loai_vb_id,
        ngon_ngu=ngon_ngu,
        so_trang=so_trang,
        ghi_chu=ghi_chu,
        nguoi_ky_id=nguoi_ky_id,
        chuc_vu_nguoi_ky=chuc_vu_nguoi_ky,
        noi_nhan=noi_nhan,
        muc_do_khan=muc_do_khan,
        han_tra_loi=han_tra_loi,
        stt_trong_ho_so=stt_trong_ho_so,
        ma_ho_so=ma_ho_so,
    )

    van_ban_moi = VanBanDi(**van_ban_data.model_dump())
    db.add(van_ban_moi)
    db.commit()
    db.refresh(van_ban_moi)

    if files:
        upload_dir = Path("uploads") / "van_ban_di" / str(van_ban_moi.id)
        upload_dir.mkdir(parents=True, exist_ok=True)

        for file in files:
            file_bytes = await file.read()
            file_path = upload_dir / file.filename
            with open(file_path, "wb") as f:
                f.write(file_bytes)

            ext = Path(file.filename).suffix.lower().lstrip('.')
            normalized_path = str(file_path).replace("\\", "/")
            file_record = FileDinhKem(
                loai_van_ban="VAN_BAN_DI",
                van_ban_id=van_ban_moi.id,
                ten_file=file.filename,
                duong_dan=normalized_path,
                dinh_dang=ext or None,
                dung_luong=float(len(file_bytes) / 1024),
            )
            db.add(file_record)

        db.commit()

    return van_ban_moi


@router.get("/{id}", response_model=VanBanDiResponse)
def lay_van_ban_di_theo_id(id: int, db: Session = Depends(get_db)):
    van_ban = db.query(VanBanDi).filter(VanBanDi.id == id).first()
    if not van_ban:
        raise HTTPException(
            status_code=404, detail="Không tìm thấy văn bản đi")
    return van_ban


@router.put("/{id}", response_model=VanBanDiResponse)
async def cap_nhat_van_ban_di(
    id: int,
    so_ky_hieu: Annotated[Optional[str], Form()] = None,
    ngay_ban_hanh: Annotated[Optional[date], Form()] = None,
    trich_yeu: Annotated[str, Form()] = None,
    don_vi_soan_thao_id: Annotated[int, Form()] = None,
    ma_loai_vb_id: Annotated[int, Form()] = None,
    ngon_ngu: Annotated[Optional[str], Form()] = None,
    so_trang: Annotated[Optional[int], Form()] = None,
    ghi_chu: Annotated[Optional[str], Form()] = None,
    nguoi_ky_id: Annotated[Optional[int], Form()] = None,
    chuc_vu_nguoi_ky: Annotated[Optional[str], Form()] = None,
    noi_nhan: Annotated[Optional[str], Form()] = None,
    muc_do_khan: Annotated[Optional[int], Form()] = None,
    han_tra_loi: Annotated[Optional[date], Form()] = None,
    stt_trong_ho_so: Annotated[Optional[int], Form()] = None,
    ma_ho_so: Annotated[Optional[str], Form()] = None,
    files: List[UploadFile] = File(default=[]),
    db: Session = Depends(get_db),
    nguoi_dung: TaiKhoan = Depends(lay_nguoi_dung_hien_tai)
):
    van_ban = db.query(VanBanDi).filter(VanBanDi.id == id).first()
    if not van_ban:
        raise HTTPException(
            status_code=404, detail="Không tìm thấy văn bản đi")

    van_ban.so_ky_hieu = so_ky_hieu
    van_ban.ngay_ban_hanh = ngay_ban_hanh
    van_ban.trich_yeu = trich_yeu
    van_ban.don_vi_soan_thao_id = don_vi_soan_thao_id
    van_ban.ma_loai_vb_id = ma_loai_vb_id
    van_ban.ngon_ngu = ngon_ngu
    van_ban.so_trang = so_trang
    van_ban.ghi_chu = ghi_chu
    van_ban.nguoi_ky_id = nguoi_ky_id
    van_ban.chuc_vu_nguoi_ky = chuc_vu_nguoi_ky
    van_ban.noi_nhan = noi_nhan
    van_ban.muc_do_khan = muc_do_khan
    van_ban.han_tra_loi = han_tra_loi
    van_ban.stt_trong_ho_so = stt_trong_ho_so
    van_ban.ma_ho_so = ma_ho_so

    db.commit()
    db.refresh(van_ban)

    if files:
        upload_dir = Path("uploads") / "van_ban_di" / str(van_ban.id)
        upload_dir.mkdir(parents=True, exist_ok=True)

        for file in files:
            file_bytes = await file.read()
            file_path = upload_dir / file.filename
            with open(file_path, "wb") as f:
                f.write(file_bytes)

            ext = Path(file.filename).suffix.lower().lstrip('.')
            normalized_path = str(file_path).replace("\\", "/")
            file_record = FileDinhKem(
                loai_van_ban="VAN_BAN_DI",
                van_ban_id=van_ban.id,
                ten_file=file.filename,
                duong_dan=normalized_path,
                dinh_dang=ext or None,
                dung_luong=float(len(file_bytes) / 1024),
            )
            db.add(file_record)

        db.commit()

    return van_ban


@router.delete("/{id}")
def xoa_van_ban_di(id: int, db: Session = Depends(get_db), nguoi_dung: TaiKhoan = Depends(lay_nguoi_dung_hien_tai)):
    van_ban = db.query(VanBanDi).filter(VanBanDi.id == id).first()
    if not van_ban:
        raise HTTPException(
            status_code=404, detail="Không tìm thấy văn bản đi")

    db.delete(van_ban)
    db.commit()
    return {"message": "Xóa văn bản đi thành công"}


@router.get("/", response_model=list[VanBanDiResponse])
def lay_danh_sach_van_ban_di(db: Session = Depends(get_db)):
    return db.query(VanBanDi).all()
