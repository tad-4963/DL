import torch
import os

# Tự động nhận diện thiết bị
# DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
DEVICE = "cpu"
# Các thông số cố định
IMAGE_SIZE = 224
NUM_CLASSES = 6

# Danh sách nhãn 
CLASS_NAMES = ['ACK', 'BCC', 'MEL', 'NEV', 'SCC', 'SEK']

# Bản đồ tên bệnh chi tiết
DISEASE_MAP = {
    'ACK': 'Dày sừng quang hóa (Actinic Keratosis)',
    'BCC': 'Ung thư biểu mô tế bào đáy (Basal Cell Carcinoma)',
    'MEL': 'U hắc tố (Melanoma) - NGUY HIỂM',
    'NEV': 'Nốt ruồi lành tính (Nevus)',
    'SCC': 'Ung thư biểu mô tế bào vảy (Squamous Cell Carcinoma)',
    'SEK': 'Dày sừng tiết bã (Seborrheic Keratosis)'
}

# Đường dẫn mặc định đến model 
MODEL_PATH = os.path.join("artifacts", "best_skinnet.pth")