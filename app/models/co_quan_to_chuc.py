from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from config.database import Base

class CoQuanToChuc(Base):
    __tablename__ = "co_quan_to_chuc"

    id = Column(Integer, primary_key=True, index=True)
    organ_id = Column(String(13), unique=True, nullable=False, comment="Mã định danh cơ quan (13 ký tự)")
    ten_co_quan = Column(String(255), nullable=False, comment="Tên cơ quan, tổ chức")
    loai_co_quan = Column(String(100), nullable=True, comment="Loại hình cơ quan")
    dia_chi = Column(String(500), nullable=True, comment="Địa chỉ")
    trang_thai = Column(Integer, default=1, comment="1: Hoạt động, 0: Ngừng hoạt động")
    
    # Khóa ngoại trỏ đến chính bảng này (dành cho cơ quan cấp trên)
    parent_id = Column(Integer, ForeignKey("co_quan_to_chuc.id"), nullable=True, comment="Mã ID cơ quan cấp trên")

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())