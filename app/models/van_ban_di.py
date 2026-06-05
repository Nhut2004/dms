from sqlalchemy import Column, Date, DateTime, Integer, String, Text, func, ForeignKey
from config.database import Base

class VanBanDi(Base):
    __tablename__ = "van_ban_di"

    # Thông tin định danh hệ thống
    id = Column(Integer, primary_key=True, index=True)
    file_code = Column(String(50), nullable=True, comment="Mã hồ sơ (FileCode)")
    file_catalog = Column(Integer, nullable=True, comment="Năm hình thành hồ sơ (FileCatalog)")
    file_notation = Column(String(20), nullable=True, comment="Số và ký hiệu hồ sơ (FileNotation)")
    doc_ordinal = Column(Integer, nullable=True, comment="Số thứ tự văn bản trong hồ sơ (DocOrdinal)")

    # Thông tin ban hành
    organ_id = Column(String(13), nullable=False, comment="Mã định danh của cơ quan ban hành (OrganId)")
    organ_name = Column(String(200), nullable=True, comment="Tên cơ quan ban hành (OrganName)")
    type_name = Column(String(100), nullable=True, comment="Tên loại văn bản (TypeName)")
    code_number = Column(String(11), nullable=True, comment="Số của văn bản (CodeNumber)")
    code_notation = Column(String(30), nullable=True, comment="Ký hiệu văn bản (CodeNotation)")
    issued_date = Column(Date, nullable=True, comment="Ngày ban hành (IssuedDate)")

    # Nội dung và phân loại
    subject = Column(String(500), nullable=True, comment="Trích yếu nội dung (Subject)")
    language = Column(String(30), nullable=True, comment="Ngôn ngữ (Language)")
    page_amount = Column(Integer, nullable=True, comment="Số trang (PageAmount)")
    description = Column(String(500), nullable=True, comment="Ghi chú (Description)")
    priority = Column(Integer, nullable=True, comment="Mức độ khẩn, độ mật (Priority)")
    issued_amount = Column(Integer, nullable=True, comment="Số lượng bản phát hành (IssuedAmount)")
    due_date = Column(Date, nullable=True, comment="Hạn trả lời văn bản (DueDate)")

    # Nơi nhận (To)
    to_organ_id = Column(String(13), nullable=True, comment="Mã định danh cơ quan nhận")
    to_organ_name = Column(String(200), nullable=True, comment="Tên cơ quan nhận")

    # Người ký (SignerInfo)
    signer_position = Column(String(100), nullable=True, comment="Chức vụ người ký (Position)")
    signer_full_name = Column(String(50), nullable=True, comment="Họ tên người ký (FullName)")

    # --- THÊM KHÓA NGOẠI TẠI ĐÂY ---
    ho_so_id = Column(Integer, ForeignKey("ho_so_luu_tru.id"), nullable=True, comment="Thuộc hồ sơ nào")
    loai_vb_id = Column(Integer, ForeignKey("danh_muc_loai_vb.id"), nullable=True, comment="ID Danh mục loại văn bản")
    nguoi_soan_id = Column(Integer, ForeignKey("tai_khoan_nguoi_dung.id"), nullable=True, comment="Cán bộ soạn thảo")

    # Quản lý hệ thống
    status = Column(String(50), default="Đã phát hành", comment="Trạng thái xử lý")
    is_recalled = Column(Integer, default=0, comment="Trạng thái thu hồi (0: Không, 1: Có)")
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)