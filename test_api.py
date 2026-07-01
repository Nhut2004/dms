import requests

BASE_URL = "http://localhost:8000/api"


def run_tests():
    print("🚀 BẮT ĐẦU CHUỖI TEST TỰ ĐỘNG API...\n")

    # 1. TEST ĐĂNG NHẬP VÀ LẤY TOKEN
    print("1. Đang test API Đăng nhập...")
    login_data = {"username": "nva_ctu", "password": "123456"}
    response = requests.post(f"{BASE_URL}/auth/login", data=login_data)

    if response.status_code != 200:
        print("❌ Đăng nhập thất bại. Hãy chắc chắn bạn đã tạo tài khoản nva_ctu dưới DB.")
        return

    token = response.json().get("access_token")
    headers = {"Authorization": f"Bearer {token}"}
    print("✅ Đăng nhập thành công! Đã lấy được Token.\n")

    # 2. TEST TẠO CƠ QUAN
    print("2. Đang test API Tạo Cơ quan...")
    cq_data = {"ten_co_quan": "Khoa CNTT", "organ_id": "TEST.01"}
    r_cq = requests.post(f"{BASE_URL}/co-quan/", json=cq_data, headers=headers)
    cq_id = 1
    if r_cq.status_code == 200:
        cq_id = r_cq.json()["id"]
        print(f" Tạo Cơ quan thành công (ID: {cq_id})")
    else:
        print("⚠️", r_cq.json()["detail"])

    # 3. TEST TẠO DANH MỤC
    print("\n3. Đang test API Tạo Danh mục...")
    dm_data = {"ten_loai_vb": "Chỉ thị"}
    r_dm = requests.post(f"{BASE_URL}/danh-muc/",
                         json=dm_data, headers=headers)
    dm_id = 1
    if r_dm.status_code == 200:
        dm_id = r_dm.json()["id"]
        print(f" Tạo Danh mục thành công (ID: {dm_id})")
    else:
        print("⚠️", r_dm.json()["detail"])

    # 4. TEST TẠO VĂN BẢN ĐI (HỢP LỆ)
    print("\n4. Đang test API Tạo Văn bản đi (Hợp lệ)...")
    vb_data = {
        "so_ky_hieu": "999/CT-TEST",
        "trich_yeu": "Chỉ thị test hệ thống tự động",
        "don_vi_soan_thao_id": cq_id,
        "ma_loai_vb_id": dm_id
    }
    r_vb = requests.post(f"{BASE_URL}/van-ban-di/",
                         json=vb_data, headers=headers)
    if r_vb.status_code == 200:
        vb_id = r_vb.json()["id"]
        print(f" Tạo Văn bản đi thành công (ID: {vb_id})")

        # 5. TEST TẠO TỆP ĐÍNH KÈM CHO VĂN BẢN ĐÓ
        print("\n5. Đang test API Thêm Tệp đính kèm...")
        file_data = {
            "loai_van_ban": "VAN_BAN_DI",
            "van_ban_id": vb_id,
            "ten_file": "chi_thi_999.pdf",
            "duong_dan": "/uploads/2026/chi_thi_999.pdf",
            "dinh_dang": "pdf",
            "dung_luong": 2.5
        }
        r_file = requests.post(
            f"{BASE_URL}/tep-dinh-kem/", json=file_data, headers=headers)
        if r_file.status_code == 200:
            print(" Thêm Tệp đính kèm thành công!")
    else:
        print(" Lỗi tạo văn bản:", r_vb.json())

    # 6. TEST KHÓA NGOẠI (CỐ TÌNH LỖI)
    print("\n6. Đang test tính năng Khóa Ngoại (Chặn ID ảo)...")
    vb_data_loi = {
        "so_ky_hieu": "LỖI",
        "trich_yeu": "Văn bản này có ID Cơ quan không tồn tại",
        "don_vi_soan_thao_id": 99999,  # ID ảo
        "ma_loai_vb_id": dm_id
    }
    r_vb_loi = requests.post(
        f"{BASE_URL}/van-ban-di/", json=vb_data_loi, headers=headers)
    if r_vb_loi.status_code == 500 or r_vb_loi.status_code == 400:
        print(" THÀNH CÔNG: Database đã chặt đứt yêu cầu vì vi phạm Khóa Ngoại (ID 99999 không tồn tại)!")
    else:
        print(" CẢNH BÁO: Database đã cho lọt dữ liệu rác!")

    print("\n HOÀN TẤT CHUỖI TEST!")


if __name__ == "__main__":
    run_tests()
