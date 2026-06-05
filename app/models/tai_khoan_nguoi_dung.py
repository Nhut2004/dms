from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from config.database import Base

class TaiKhoanNguoiDung(Base):
    __tablename__ = "tai_khoan_nguoi_dung"

    id = Column(Integer, primary_key=True, index=True)
    
    # Khóa ngoại liên kết với bảng Cơ quan
    co_quan_id = Column(Integer, ForeignKey("co_quan_to_chuc.id"), nullable=False, comment="Thuộc cơ quan nào")
    
    ho_ten = Column(String(100), nullable=False, comment="Họ và tên")
    chuc_vu = Column(String(100), nullable=True, comment="Chức vụ")
    email = Column(String(100), unique=True, nullable=True)
    ten_dang_nhap = Column(String(50), unique=True, nullable=False)
    mat_khau = Column(String(255), nullable=False, comment="Mật khẩu đã mã hóa")
    vai_tro = Column(String(50), default="chuyen_vien", comment="Vai trò: lanh_dao, van_thu, chuyen_vien, admin")
    trang_thai = Column(Integer, default=1, comment="1: Hoạt động, 0: Khóa")
    
    lan_dang_nhap_cuoi = Column(DateTime, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())