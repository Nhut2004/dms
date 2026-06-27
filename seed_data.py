from datetime import date, timedelta
from config.database import SessionLocal
# Đã import thêm ViTriLuuTru vào đây
from app.models.core import CoQuanToChuc, DanhMucLoaiVb, HoSo, ViTriLuuTru
from app.models.auth import CanBo
from app.models.document import VanBanDen, VanBanDi


def seed_data():
    db = SessionLocal()

    try:
        print("⏳ Đang kiểm tra và tạo dữ liệu nền tảng (Danh mục, Cơ quan, Cán bộ, Vị trí, Hồ sơ)...")

        # 1. Tạo Cơ quan (nếu chưa có)
        co_quan = db.query(CoQuanToChuc).first()
        if not co_quan:
            co_quan = CoQuanToChuc(
                ten_co_quan="UBND Thành phố Cần Thơ", organ_id="UBND-CT", dia_chi="Cần Thơ")
            db.add(co_quan)
            db.commit()
            db.refresh(co_quan)

        # 2. Tạo Loại văn bản (nếu chưa có)
        loai_vb = db.query(DanhMucLoaiVb).first()
        if not loai_vb:
            loai_vb = DanhMucLoaiVb(
                ten_loai_vb="Quyết định", mo_ta="Quyết định hành chính")
            db.add(loai_vb)
            db.commit()
            db.refresh(loai_vb)

        # 3. Tạo Cán bộ (nếu chưa có)
        can_bo = db.query(CanBo).first()
        if not can_bo:
            can_bo = CanBo(ho_ten="Trần Thị B",
                           chuc_vu="Giám đốc Sở", co_quan_id=co_quan.id)
            db.add(can_bo)
            db.commit()
            db.refresh(can_bo)

        # 4. TẠO VỊ TRÍ LƯU TRỮ (MỚI THÊM)
        vi_tri = db.query(ViTriLuuTru).first()
        if not vi_tri:
            vi_tri_1 = ViTriLuuTru(toa_nha="A", phong="101", ke_tu="01",
                                   ngan_tang="1", so_hop="H01", ghi_chu="Hồ sơ năm 2026")
            vi_tri_2 = ViTriLuuTru(toa_nha="B", phong="202", ke_tu="03",
                                   ngan_tang="2", so_hop="H15", ghi_chu="Hồ sơ mật")
            db.add_all([vi_tri_1, vi_tri_2])
            db.commit()
            db.refresh(vi_tri_1)
            vi_tri = vi_tri_1  # Gán vị trí 1 để dùng cho Hồ sơ mẫu

        # 5. Tạo Hồ sơ lưu trữ (Đã liên kết Vị trí lưu trữ)
        ho_so = db.query(HoSo).first()
        if not ho_so:
            ho_so = HoSo(
                ma_ho_so="HS-2026-001",
                tieu_de_ho_so="Hồ sơ dự án CNTT năm 2026",
                vi_tri_id=vi_tri.id  # Gắn vị trí lưu trữ vào đây
            )
            db.add(ho_so)
            db.commit()
            db.refresh(ho_so)

        print("⏳ Đang tạo 5 dữ liệu mẫu cho Văn bản đến...")
        if db.query(VanBanDen).count() == 0:
            for i in range(1, 6):
                vb_den = VanBanDen(
                    so_den=i,
                    ky_hieu=f"{i:03d}/QĐ-UBND",
                    ngay_den=date.today() - timedelta(days=i),
                    ngay_ban_hanh=date.today() - timedelta(days=i+2),
                    co_quan_ban_hanh_id=co_quan.id,
                    ma_loai_vb_id=loai_vb.id,
                    trich_yeu=f"Quyết định phê duyệt dự án nâng cấp hạ tầng số {i}",
                    ngon_ngu="Tiếng Việt",
                    so_trang=5 + i,
                    ho_ten_nguoi_ky="Nguyễn Văn A",
                    chuc_vu_nguoi_ky="Chủ tịch",
                    linh_vuc="Công nghệ thông tin",
                    do_khan=1 if i % 2 == 0 else 2,
                    don_vi_nhan="Phòng Hành chính, Phòng IT",
                    han_giai_quyet=date.today() + timedelta(days=10 - i),
                    ma_ho_so=ho_so.ma_ho_so
                )
                db.add(vb_den)

        print("⏳ Đang tạo 5 dữ liệu mẫu cho Văn bản đi...")
        if db.query(VanBanDi).count() == 0:
            for i in range(1, 6):
                vb_di = VanBanDi(
                    so_ky_hieu=f"VB/{date.today().year}/{i:03d}",
                    ngay_ban_hanh=date.today(),
                    trich_yeu=f"Thông báo triển khai kế hoạch bảo mật hệ thống giai đoạn {i}",
                    don_vi_soan_thao_id=co_quan.id,
                    ma_loai_vb_id=loai_vb.id,
                    ngon_ngu="Tiếng Việt",
                    so_trang=2 + i,
                    nguoi_ky_id=can_bo.id,
                    chuc_vu_nguoi_ky=can_bo.chuc_vu,
                    noi_nhan="Các phòng ban trực thuộc",
                    muc_do_khan=3 if i == 5 else 1,
                    han_tra_loi=date.today() + timedelta(days=15),
                    so_luong_ban_phat_hanh=10 * i,
                    ma_ho_so=ho_so.ma_ho_so
                )
                db.add(vb_di)

        db.commit()
        print("✅ THÀNH CÔNG! Đã bơm dữ liệu xong. Mở trình duyệt lên test thôi!")

    except Exception as e:
        db.rollback()
        print(f"❌ Xảy ra lỗi trong quá trình tạo dữ liệu: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    seed_data()
