from config.database import engine, Base
# Import toàn bộ model để SQLAlchemy nhận diện được các bảng
from app.models import auth, core, document

print("Đang dọn dẹp và xóa toàn bộ bảng cũ trong PostgreSQL...")
Base.metadata.drop_all(bind=engine)

print("Đang khởi tạo lại cấu trúc bảng mới chuẩn xịn...")
Base.metadata.create_all(bind=engine)

print("Hoàn tất! Database đã được dọn sạch và cập nhật cấu trúc thành công.")
