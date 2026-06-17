# Hệ thống Quản lý Tài liệu Điện tử (DMS)
Dự án DMS chuẩn Nghị định 30/2020/NĐ-CP. Được xây dựng bằng FastAPI và PostgreSQL.

## 1. Yêu cầu cài đặt (Prerequisites)
- [Python 3.10+](https://www.python.org/downloads/)
- [PostgreSQL](https://www.postgresql.org/download/) & pgAdmin 4
- [Node.js](https://nodejs.org/) (Phiên bản LTS - Bắt buộc để chạy giao diện)
- VS Code (Khuyên dùng)

## 2. Hướng dẫn cài đặt và chạy dự án (Setup)

**Bước 1: Cài đặt Database**
- Mở pgAdmin 4, tạo một cơ sở dữ liệu mới tên là: `document_management`
- Dùng file init.sql để tạo bảng

**Bước 2: Cài đặt môi trường ảo & Thư viện**
- Mở Terminal tại thư mục dự án, chạy các lệnh sau:
  ```bash
  python -m venv venv
  venv\Scripts\activate      # Dành cho Windows
  pip install -r requirements.txt

Bước 3: Cấu hình biến môi trường

    Copy file .env.example và đổi tên thành .env.
    Mở file .env lên, sửa lại phần YOUR_PASSWORD thành mật khẩu PostgreSQL trên máy của bạn.

Bước 4: Khởi động Server

    Chạy lệnh sau để khởi động hệ thống:
    uvicorn main:app --reload

    Mở trình duyệt và vào: http://localhost:8000/docs để xem giao diện Swagger UI và Test API.
    (Lưu ý: Ngay khi Server chạy lần đầu, SQLAlchemy sẽ tự động soi các file Models và xây dựng toàn bộ các bảng trong CSDL document_management cho bạn).

## 3. Cài đặt và chạy Frontend (ReactJS)
1. Lịch sử khởi tạo dự án (Dành cho báo cáo/giảng viên)
    Dự án được khởi tạo từ con số 0 bằng Vite và các thư viện UI, Call API:

    Bash
    # Tạo khung dự án React
    npm create vite@latest frontend -- --template react

    # Di chuyển vào thư mục và cài đặt các thư viện lõi
    cd frontend
    npm install antd axios react-router-dom

    2. Dành cho thành viên nhóm (Khi clone code về máy)
    Các thành viên KHÔNG chạy lại lệnh khởi tạo ở trên, chỉ cần di chuyển vào thư mục và cài đặt các gói (packages) đã có sẵn:

    cd frontend
    npm install

    3. Khởi động Giao diện

    Chạy lệnh:
    npm run dev

## 4. Cấu trúc thư mục (Project Structure)
    app/models/: Chứa các bản vẽ cấu trúc Database (Entity).
    app/schemas/: Chứa các Pydantic model để kiểm tra dữ liệu đầu vào/đầu ra.
    app/routes/: Chứa các logic xử lý API (Controllers).
    config/: Chứa cấu hình kết nối Database.
    uploads/: Nơi lưu trữ các file PDF, Word người dùng tải lên.
    frontend/: Chứa toàn bộ mã nguồn giao diện ReactJS
    docs/: Chứa tài liệu đặc tả hệ thống (API Spec, Screen Spec, Workflow)