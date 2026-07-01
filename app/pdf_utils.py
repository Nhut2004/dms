import fitz  # PyMuPDF
from datetime import date

# Tạo tính năng Đóng Dấu Đỏ lên PDF
def dong_dau_van_ban_den(file_path: str, so_den: int, ngay_den: date):
    try:
        doc = fitz.open(file_path)
        if len(doc) == 0:
            return
            
        page = doc[0] # Đóng dấu ở trang đầu
        text = f"ĐẾN\nSố: {so_den}\nNgày: {ngay_den.strftime('%d/%m/%Y')}"
        
        # Tọa độ góc trên bên trái
        point = fitz.Point(50, 50)
        page.insert_text(point, text, fontsize=14, color=(1, 0, 0), fontname="helv", bold=True)
        
        doc.saveIncr()
        doc.close()
        print(f"Đã đóng dấu ĐẾN thành công cho file: {file_path}")
    except Exception as e:
        print(f"Lỗi khi đóng dấu PDF: {e}")