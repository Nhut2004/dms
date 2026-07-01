import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Nạp biến môi trường từ file .env
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# Khởi tạo bộ máy kết nối (Engine)
engine = create_engine(DATABASE_URL)

# Tạo phiên làm việc (Session) để thao tác với database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base model để các bảng khác kế thừa
Base = declarative_base()

# Hàm dependency dùng cho FastAPI sau này
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()