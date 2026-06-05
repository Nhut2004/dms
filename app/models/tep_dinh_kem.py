from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, func
from config.database import Base

class TepDinhKem(Base):
    __tablename__ = "tep_dinh_kem"

    id = Column(Integer, primary_key=True, index=True)
    ten_tep = Column(String(255), nullable=False, comment="Tên file gốc (VD: QĐ-123.pdf)")
    duong_dan = Column(String(500), nullable=False, comment="Đường dẫn lưu trên server/cloud")
    dinh_dang = Column(String(50), nullable=True, comment="Định dạng (pdf, docx, xlsx...)")
    kich_thuoc = Column(Float, nullable=True, comment="Dung lượng file (MB/KB)")
    tep_chinh = Column(Integer, default=1, comment="1: File nội dung chính, 0: Phụ lục")
    
    # Phân loại tệp thuộc về Văn bản đến hay Văn bản đi
    loai_van_ban = Column(String(50), nullable=False, comment="van_ban_den hoặc van_ban_di")
    van_ban_id = Column(Integer, nullable=False, comment="ID của văn bản tương ứng")
    
    nguoi_tai_len_id = Column(Integer, ForeignKey("tai_khoan_nguoi_dung.id"), nullable=True)
    thoi_gian_tai_len = Column(DateTime, server_default=func.now())