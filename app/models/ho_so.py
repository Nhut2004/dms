from sqlalchemy import Column, Date, DateTime, Integer, String, func, ForeignKey
from config.database import Base

class HoSoLuuTru(Base):
    __tablename__ = "ho_so_luu_tru"

    # Thông tin định danh hệ thống
    id = Column(Integer, primary_key=True, index=True)

    # 1. Mã hồ sơ
    file_code = Column(String(50), nullable=True, comment="Mã hồ sơ (FileCode)")
    organ_id = Column(String(13), nullable=False, comment="Mã định danh cơ quan lập danh mục (OrganId)")
    file_catalog = Column(Integer, nullable=True, comment="Năm hình thành hồ sơ (FileCatalog)")
    file_notation = Column(String(20), nullable=True, comment="Số và ký hiệu hồ sơ (FileNotation)")

    # Các thông tin hồ sơ khác theo chuẩn
    title = Column(String(500), nullable=False, comment="Tiêu đề hồ sơ (Title)")
    maintenance = Column(String(30), nullable=True, comment="Thời hạn bảo quản (Maintenance)")
    rights = Column(String(30), nullable=True, comment="Chế độ sử dụng (Rights)")
    creator = Column(String(30), nullable=True, comment="Người lập hồ sơ (Creator)")
    language = Column(String(50), nullable=True, comment="Ngôn ngữ (Language)")
    start_date = Column(Date, nullable=True, comment="Thời gian bắt đầu (StartDate)")
    end_date = Column(Date, nullable=True, comment="Thời gian kết thúc (EndDate)")
    doc_total = Column(Integer, nullable=True, comment="Tổng số văn bản trong hồ sơ (DocTotal)")
    page_total = Column(Integer, nullable=True, comment="Tổng số trang của hồ sơ (PageTotal)")
    description = Column(String(500), nullable=True, comment="Ghi chú (Description)")

    # Quản lý hệ thống (Theo thiết kế luận lý)
    is_locked = Column(Integer, default=0, comment="Trạng thái khóa (0: Mở, 1: Khóa)")

    # --- THÊM KHÓA NGOẠI TẠI ĐÂY ---
    co_quan_id = Column(Integer, ForeignKey("co_quan_to_chuc.id"), nullable=True, comment="ID Cơ quan quản lý hồ sơ")
    created_by_id = Column(Integer, ForeignKey("tai_khoan_nguoi_dung.id"), nullable=True, comment="ID Người tạo hệ thống")
    # ------------------------------

    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)