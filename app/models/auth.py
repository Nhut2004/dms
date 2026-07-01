from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Table
from sqlalchemy.orm import relationship
from config.database import Base
from datetime import datetime

# Các bảng trung gian cho quan hệ nhiều-nhiều
tai_khoan_vai_tro = Table(
    'tai_khoan_vai_tro', Base.metadata,
    Column('tai_khoan_id', Integer, ForeignKey(
        'tai_khoan.id', ondelete="CASCADE"), primary_key=True),
    Column('vai_tro_id', Integer, ForeignKey(
        'vai_tro.id', ondelete="CASCADE"), primary_key=True)
)

vai_tro_quyen = Table(
    'vai_tro_quyen', Base.metadata,
    Column('vai_tro_id', Integer, ForeignKey(
        'vai_tro.id', ondelete="CASCADE"), primary_key=True),
    Column('quyen_id', Integer, ForeignKey(
        'quyen.id', ondelete="CASCADE"), primary_key=True)
)


class CanBo(Base):
    __tablename__ = "can_bo"
    id = Column(Integer, primary_key=True, index=True)
    ho_ten = Column(String(100), nullable=False)
    chuc_vu = Column(String(100))
    co_quan_id = Column(Integer, ForeignKey(
        "co_quan_to_chuc.id", ondelete="RESTRICT"), nullable=False)


class TaiKhoan(Base):
    __tablename__ = "tai_khoan"
    id = Column(Integer, primary_key=True, index=True)
    can_bo_id = Column(Integer, ForeignKey(
        "can_bo.id", ondelete="SET NULL"), unique=True)
    ten_dang_nhap = Column(String(100), unique=True, nullable=False)
    # Đã đổi tên khớp với SQL
    mat_khau_hash = Column(String(255), nullable=False)
    trang_thai = Column(String(20), default="ACTIVE", nullable=False)
    ngay_tao = Column(DateTime, default=datetime.utcnow, nullable=False)
    ngay_cap_nhat = Column(DateTime, default=datetime.utcnow,
                           onupdate=datetime.utcnow, nullable=False)

    vai_tros = relationship(
        "VaiTro", secondary=tai_khoan_vai_tro, backref="tai_khoans")


class VaiTro(Base):
    __tablename__ = "vai_tro"
    id = Column(Integer, primary_key=True, index=True)
    ma_vai_tro = Column(String(50), unique=True, nullable=False)
    ten_vai_tro = Column(String(100), nullable=False)
    mo_ta = Column(String(500))

    quyens = relationship("Quyen", secondary=vai_tro_quyen, backref="vai_tros")


class Quyen(Base):
    __tablename__ = "quyen"
    id = Column(Integer, primary_key=True, index=True)
    ma_quyen = Column(String(100), unique=True, nullable=False)
    ten_quyen = Column(String(150), nullable=False)
    module = Column(String(50), nullable=False)
    hanh_dong = Column(String(30), nullable=False)
