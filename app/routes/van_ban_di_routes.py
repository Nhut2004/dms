from datetime import date
from pathlib import Path
from typing import Annotated, List, Optional
from sqlalchemy import func
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session
from config.database import get_db
from app.models.core import HoSo
from app.models.document import FileDinhKem, VanBanDi, VanBanDen
from app.schemas.van_ban_di_schema import VanBanDiCreate, VanBanDiResponse
from app.dependencies import lay_nguoi_dung_hien_tai
from app.models.auth import TaiKhoan, CanBo
from app.schemas.van_ban_di_schema import TrangThaiUpdate
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
    so_luong_ban_phat_hanh: Annotated[Optional[int], Form()] = None,
    db: Session = Depends(get_db),
    nguoi_dung: TaiKhoan = Depends(lay_nguoi_dung_hien_tai)
):

    if ma_ho_so:
        ho_so = db.query(HoSo).filter(HoSo.ma_ho_so == ma_ho_so).first()
        if ho_so and ho_so.trang_thai == "DA_DONG":
            raise HTTPException(
                status_code=400,
                detail=f"Hồ sơ {ma_ho_so} đã đóng, không thể thêm văn bản mới vào hồ sơ này!"
            )

    # --- BLOCK VALIDATE NGHIỆP VỤ ---
    if han_tra_loi and ngay_ban_hanh:
        if han_tra_loi < ngay_ban_hanh:
            raise HTTPException(
                status_code=400,
                detail="Lỗi nghiệp vụ: Hạn trả lời KHÔNG ĐƯỢC trước Ngày ban hành!"
            )

    if so_trang is not None and so_trang < 0:
        raise HTTPException(
            status_code=400,
            detail="Lỗi dữ liệu: Số trang không được là số âm!"
        )

    if so_luong_ban_phat_hanh is not None and so_luong_ban_phat_hanh < 0:
        raise HTTPException(
            status_code=400,
            detail="Lỗi dữ liệu: Số lượng bản phát hành không được là số âm!"
        )
    # --------------------------------

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
        so_luong_ban_phat_hanh=so_luong_ban_phat_hanh
    )

    van_ban_moi = VanBanDi(**van_ban_data.model_dump())
    db.add(van_ban_moi)
    db.commit()
    db.refresh(van_ban_moi)

    # Nếu có file đính kèm, lưu chúng và cập nhật lại đối tượng để trả về thông tin file
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
        # Làm mới đối tượng để trường relationship `tep_dinh_kems` chứa danh sách file mới
        db.refresh(van_ban_moi)

    return van_ban_moi


@router.get("/{id}", response_model=VanBanDiResponse)
def lay_van_ban_di_theo_id(
    id: int,
    db: Session = Depends(get_db),
    nguoi_dung: TaiKhoan = Depends(lay_nguoi_dung_hien_tai)  # Đã thêm bảo mật
):
    """Lấy chi tiết một văn bản đi (bảo vệ bằng JWT)."""
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
    so_luong_ban_phat_hanh: Annotated[Optional[int], Form()] = None,
    db: Session = Depends(get_db),
    nguoi_dung: TaiKhoan = Depends(lay_nguoi_dung_hien_tai)
):
    van_ban = db.query(VanBanDi).filter(VanBanDi.id == id).first()
    if not van_ban:
        raise HTTPException(
            status_code=404, detail="Không tìm thấy văn bản đi")

    ma_ho_so_moi = van_ban.ma_ho_so if van_ban.ma_ho_so is not None else db.ma_ho_so
    if ma_ho_so_moi:
        ho_so = db.query(HoSo).filter(HoSo.ma_ho_so == ma_ho_so_moi).first()
        if ho_so and ho_so.trang_thai == "DA_DONG":
            raise HTTPException(
                status_code=400,
                detail=f"Hồ sơ {ma_ho_so_moi} đã đóng, không thể đưa văn bản vào đây!"
            )

    # --- BLOCK VALIDATE NGHIỆP VỤ KHI CẬP NHẬT ---
    ngay_ban_hanh_check = ngay_ban_hanh if ngay_ban_hanh else van_ban.ngay_ban_hanh
    han_tra_loi_check = han_tra_loi if han_tra_loi else van_ban.han_tra_loi

    if han_tra_loi_check and ngay_ban_hanh_check:
        if han_tra_loi_check < ngay_ban_hanh_check:
            raise HTTPException(
                status_code=400,
                detail="Lỗi nghiệp vụ: Hạn trả lời KHÔNG ĐƯỢC trước Ngày ban hành!"
            )

    so_trang_check = so_trang if so_trang is not None else van_ban.so_trang
    if so_trang_check is not None and so_trang_check < 0:
        raise HTTPException(
            status_code=400,
            detail="Lỗi dữ liệu: Số trang không được là số âm!"
        )

    so_luong_check = so_luong_ban_phat_hanh if so_luong_ban_phat_hanh is not None else van_ban.so_luong_ban_phat_hanh
    if so_luong_check is not None and so_luong_check < 0:
        raise HTTPException(
            status_code=400,
            detail="Lỗi dữ liệu: Số lượng bản phát hành không được là số âm!"
        )
    # --------------------------------

    # --- CẬP NHẬT AN TOÀN (Không ghi đè dữ liệu thành None) ---
    if so_ky_hieu is not None:
        van_ban.so_ky_hieu = so_ky_hieu
    if ngay_ban_hanh is not None:
        van_ban.ngay_ban_hanh = ngay_ban_hanh
    if trich_yeu is not None:
        van_ban.trich_yeu = trich_yeu
    if don_vi_soan_thao_id is not None:
        van_ban.don_vi_soan_thao_id = don_vi_soan_thao_id
    if ma_loai_vb_id is not None:
        van_ban.ma_loai_vb_id = ma_loai_vb_id
    if ngon_ngu is not None:
        van_ban.ngon_ngu = ngon_ngu
    if so_trang is not None:
        van_ban.so_trang = so_trang
    if ghi_chu is not None:
        van_ban.ghi_chu = ghi_chu
    if nguoi_ky_id is not None:
        van_ban.nguoi_ky_id = nguoi_ky_id
    if chuc_vu_nguoi_ky is not None:
        van_ban.chuc_vu_nguoi_ky = chuc_vu_nguoi_ky
    if noi_nhan is not None:
        van_ban.noi_nhan = noi_nhan
    if muc_do_khan is not None:
        van_ban.muc_do_khan = muc_do_khan
    if han_tra_loi is not None:
        van_ban.han_tra_loi = han_tra_loi
    if so_luong_ban_phat_hanh is not None:
        van_ban.so_luong_ban_phat_hanh = so_luong_ban_phat_hanh
    if stt_trong_ho_so is not None:
        van_ban.stt_trong_ho_so = stt_trong_ho_so
    if ma_ho_so is not None:
        van_ban.ma_ho_so = ma_ho_so
    # ------------------------------------------------------------

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

    db.refresh(van_ban)  # Cập nhật danh sách file mới nhất trả về cho UI
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


# Bỏ response_model=list[VanBanDiResponse] để trả về cấu trúc mới
@router.get("/")
def lay_danh_sach_van_ban_di(
    page: int = 1,
    size: int = 10,
    keyword: str = None,  # Hỗ trợ tìm kiếm từ khóa
    db: Session = Depends(get_db),
    nguoi_dung: TaiKhoan = Depends(lay_nguoi_dung_hien_tai)
):
    query = db.query(VanBanDi)

    # Lọc theo từ khóa nếu có
    if keyword:
        query = query.filter(
            VanBanDi.trich_yeu.contains(keyword) |
            VanBanDi.so_ky_hieu.contains(keyword)
        )

    total = query.count()
    danh_sach = query.offset((page - 1) * size).limit(size).all()

    return {"data": danh_sach, "total": total}


@router.put("/{id}/trang-thai")
def cap_nhat_trang_thai(
    id: int,
    data: TrangThaiUpdate,
    db: Session = Depends(get_db),
    nguoi_dung: TaiKhoan = Depends(lay_nguoi_dung_hien_tai)
):
    # 1. Tìm văn bản đi hiện tại
    van_ban_di = db.query(VanBanDi).filter(VanBanDi.id == id).first()
    if not van_ban_di:
        raise HTTPException(
            status_code=404, detail="Không tìm thấy văn bản đi!")

    # Lưu lại trạng thái cũ trước khi cập nhật
    trang_thai_cu = van_ban_di.trang_thai
    van_ban_di.trang_thai = data.trang_thai  # Cập nhật sang trạng thái mới

    # 2. LOGIC LIÊN THÔNG: Chỉ kích hoạt khi chuyển sang PUBLISHED
    if trang_thai_cu != 'PUBLISHED' and data.trang_thai == 'PUBLISHED':
        try:
            # Tự động tính "Số đến" tiếp theo
            max_so_den = db.query(func.max(VanBanDen.so_den)).scalar() or 0

            # Tìm tên người ký từ bảng Cán Bộ
            ten_nguoi_ky = ""
            if van_ban_di.nguoi_ky_id:
                nguoi_ky = db.query(CanBo).filter(
                    CanBo.id == van_ban_di.nguoi_ky_id).first()
                ten_nguoi_ky = nguoi_ky.ho_ten if nguoi_ky else ""

            # TẠO VĂN BẢN ĐẾN MỚI TỪ DỮ LIỆU CỦA VĂN BẢN ĐI
            van_ban_den_moi = VanBanDen(
                so_den=max_so_den + 1,
                ky_hieu=van_ban_di.so_ky_hieu,
                ngay_den=date.today(),
                ngay_ban_hanh=van_ban_di.ngay_ban_hanh,
                co_quan_ban_hanh_id=van_ban_di.don_vi_soan_thao_id,
                ma_loai_vb_id=van_ban_di.ma_loai_vb_id,
                trich_yeu=van_ban_di.trich_yeu,
                so_trang=van_ban_di.so_trang,
                ho_ten_nguoi_ky=ten_nguoi_ky,
                chuc_vu_nguoi_ky=van_ban_di.chuc_vu_nguoi_ky,
                do_khan=van_ban_di.muc_do_khan,
                don_vi_nhan=van_ban_di.noi_nhan,
                trang_thai_xu_ly='CHO_XU_LY'  # Gắn trạng thái chờ xử lý cho bên nhận
            )
            db.add(van_ban_den_moi)
            db.flush()  # Cấp ID cho văn bản đến mới nhưng chưa commit DB

            # COPY LUÔN CÁC FILE ĐÍNH KÈM
            tep_dinh_kems = db.query(FileDinhKem).filter(
                FileDinhKem.van_ban_id == van_ban_di.id,
                FileDinhKem.loai_van_ban == 'VAN_BAN_DI'
            ).all()

            for tep in tep_dinh_kems:
                tep_moi = FileDinhKem(
                    loai_van_ban='VAN_BAN_DEN',
                    van_ban_id=van_ban_den_moi.id,  # Gắn vào ID văn bản đến mới
                    ten_file=tep.ten_file,
                    duong_dan=tep.duong_dan,
                    dinh_dang=tep.dinh_dang,
                    dung_luong=tep.dung_luong
                )
                db.add(tep_moi)

        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=500, detail=f"Lỗi hệ thống khi liên thông văn bản: {str(e)}")

    elif trang_thai_cu == 'PUBLISHED' and data.trang_thai == 'REVOKED':
        try:
            # Tìm Văn bản đến đã được tự động sinh ra trước đó
            van_ban_den_can_huy = db.query(VanBanDen).filter(
                VanBanDen.ky_hieu == van_ban_di.so_ky_hieu,
                VanBanDen.co_quan_ban_hanh_id == van_ban_di.don_vi_soan_thao_id
            ).first()

            if van_ban_den_can_huy:
                # 3.1. Xóa các File đính kèm của Văn bản đến này
                db.query(FileDinhKem).filter(
                    FileDinhKem.van_ban_id == van_ban_den_can_huy.id,
                    FileDinhKem.loai_van_ban == 'VAN_BAN_DEN'
                ).delete()

                # 3.2. Xóa Văn bản đến (Hủy theo đúng NĐ 30)
                db.delete(van_ban_den_can_huy)

        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=500, detail=f"Lỗi hệ thống khi thu hồi văn bản liên thông: {str(e)}")

    # 3. Lưu toàn bộ thay đổi (cả trạng thái VB đi và VB đến mới tạo)
    db.commit()
    db.refresh(van_ban_di)

    return {
        "message": "Cập nhật trạng thái thành công!",
        "trang_thai_moi": van_ban_di.trang_thai,
        "lien_thong_thanh_cong": data.trang_thai == 'PUBLISHED' and trang_thai_cu != 'PUBLISHED'
    }
