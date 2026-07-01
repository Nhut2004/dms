import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, inspect

# Nạp biến môi trường từ .env
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")


def check_database_schema():
    print("===  KIỂM TRA CẤU TRÚC CƠ SỞ DỮ LIỆU DMS ===\n")
    try:
        # Khởi tạo kết nối
        engine = create_engine(DATABASE_URL)
        inspector = inspect(engine)

        # Lấy danh sách tất cả các bảng
        tables = inspector.get_table_names()
        print(f" Tổng số bảng đang có trong hệ thống: {len(tables)} bảng\n")

        if len(tables) == 0:
            print(" CẢNH BÁO: Chưa có bảng nào được tạo. Hãy chạy server uvicorn trước!")
            return

        # Quét từng bảng để kiểm tra khóa ngoại (Foreign Keys)
        for table in tables:
            print(f" BẢNG: {table.upper()}")

            fks = inspector.get_foreign_keys(table)
            if not fks:
                print("   └── Không có khóa ngoại (Bảng danh mục gốc)")
            else:
                for fk in fks:
                    cot_hien_tai = ", ".join(fk['constrained_columns'])
                    bang_dich = fk['referred_table']
                    cot_dich = ", ".join(fk['referred_columns'])
                    print(
                        f"   └──  Liên kết: Cột [{cot_hien_tai}] ---> Bảng [{bang_dich.upper()}] (Cột: {cot_dich})")
            print("-" * 50)

        print("\n HOÀN TẤT KIỂM TRA!")
        print("Nếu bạn thấy các bảng như VAN_BAN_DEN, VAN_BAN_DI có các liên kết trỏ tới HO_SO_LUU_TRU, CO_QUAN_TO_CHUC... thì xin chúc mừng, hệ thống đã chuẩn 100%!")

    except Exception as e:
        print(f" Có lỗi xảy ra trong quá trình kết nối: {e}")


if __name__ == "__main__":
    check_database_schema()
