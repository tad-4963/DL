import requests

# URL của server mình vừa chạy
url = "http://localhost:8000/analyze"

# Đường dẫn ảnh muốn test (Sửa lại tên file ảnh của bạn)
file_path = r"F:\CODE\DL\data\imgs_part_1\PAT_8_15_820.png" 

# Thông tin bệnh nhân giả định
payload = {
    "age": "45",
    "gender": "Male",
    "itch": "Yes",
    "grew": "Yes",
    "bleed": "No"
}

# Gửi request
try:
    with open(file_path, "rb") as f:
        files = {"file": f}
        print("Đang gửi ảnh đi phân tích...")
        response = requests.post(url, data=payload, files=files)
    
    # In kết quả
    if response.status_code == 200:
        print("\n--- KẾT QUẢ TỪ SERVER ---")
        print(response.json())
    else:
        print("Lỗi:", response.text)

except FileNotFoundError:
    print(f"Không tìm thấy file ảnh: {file_path}")
except Exception as e:
    print(f"Không kết nối được server: {e}")