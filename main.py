from app.routes import ho_so_routes, tep_dinh_kem_routes, van_ban_den_routes, van_ban_di_routes
from app.routes import danh_muc_routes
from app.routes import tai_khoan_routes
from app.routes import co_quan_routes
from fastapi import FastAPI
from config.database import Base, engine

# 1. Import các models để SQLAlchemy nhận diện được
from app.models.van_ban_den import VanBanDen
from app.models.van_ban_di import VanBanDi
from app.models.ho_so import HoSoLuuTru
from app.models.co_quan_to_chuc import CoQuanToChuc
from app.models.tai_khoan_nguoi_dung import TaiKhoanNguoiDung
from app.models.danh_muc_loai_vb import DanhMucLoaiVb
from app.models.tep_dinh_kem import TepDinhKem
from app.models.nhat_ky_truy_cap import NhatKyTruyCap
from app.models.van_ban_di import VanBanDi
from app.models.van_ban_den import VanBanDen
from app.models.tep_dinh_kem import TepDinhKem
# 2. Lệnh tự động tạo tất cả các bảng trong database (nếu chưa có)
Base.metadata.create_all(bind=engine)

# 3. Khởi tạo ứng dụng FastAPI
app = FastAPI(title="Document Management System (DMS)")

app.include_router(co_quan_routes.router)
app.include_router(tai_khoan_routes.router)
app.include_router(danh_muc_routes.router)
app.include_router(ho_so_routes.router)
app.include_router(van_ban_di_routes.router)
app.include_router(van_ban_den_routes.router)
app.include_router(tep_dinh_kem_routes.router)


@app.get("/")
def read_root():
    return {"message": "Hệ thống DMS đã khởi động. Database đã được tạo thành công!"}
