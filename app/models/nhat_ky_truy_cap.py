from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from config.database import Base

class NhatKyTruyCap(Base):
    __tablename__ = "nhat_ky_truy_cap"

    id = Column(Integer, primary_key=True, index=True)
    ma_tai_nguyen = Column(Integer, nullable=False, comment="ID của văn bản hoặc hồ sơ")
    loai_tai_nguyen = Column(String(50), nullable=False, comment="van_ban_den, van_ban_di, ho_so")
    hanh_dong = Column(String(100), nullable=False, comment="XEM, TAO_MOI, CAP_NHAT, XOA, TAI_XUONG")
    dia_chi_ip = Column(String(50), nullable=True, comment="IP của người dùng")
    thiet_bi = Column(String(255), nullable=True, comment="Trình duyệt hoặc thiết bị")
    
    nguoi_dung_id = Column(Integer, ForeignKey("tai_khoan_nguoi_dung.id"), nullable=False)
    thoi_gian_truy_cap = Column(DateTime, server_default=func.now())