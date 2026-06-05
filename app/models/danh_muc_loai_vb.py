from sqlalchemy import Column, Integer, String, Text
from config.database import Base

class DanhMucLoaiVb(Base):
    __tablename__ = "danh_muc_loai_vb"

    id = Column(Integer, primary_key=True, index=True)
    ten_loai_vb = Column(String(100), unique=True, nullable=False, comment="Ví dụ: Quyết định, Tờ trình, Công văn")
    mo_ta = Column(Text, nullable=True, comment="Mô tả chi tiết loại văn bản")