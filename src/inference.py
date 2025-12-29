import torch
import torch.nn.functional as F
from PIL import Image
import os

from .model import SkinNet
from .config import DEVICE, CLASS_NAMES, DISEASE_MAP, MODEL_PATH
from .transforms import get_transforms

class MedicalAnalyzer:
    def __init__(self, model_path=MODEL_PATH):
        self.device = DEVICE
        print(f"--> Đang load model từ: {model_path}")
        
        self.model = SkinNet()
        
        if os.path.exists(model_path):
            state_dict = torch.load(model_path, map_location=self.device)
            self.model.load_state_dict(state_dict)
            self.model.to(self.device)
            self.model.eval()
            print("--> Model đã sẵn sàng!")
        else:
            raise FileNotFoundError(f"Không tìm thấy file model tại {model_path}")
            
        self.transform = get_transforms()

    def _process_metadata(self, meta_dict):
        gender_str = str(meta_dict.get('gender', '')).upper()
        itch_str   = str(meta_dict.get('itch', '')).upper()
        grew_str   = str(meta_dict.get('grew', '')).upper()
        bleed_str  = str(meta_dict.get('bleed', '')).upper()

        # Quy đổi sang 1.0 hoặc 0.0
        gen_val   = 1.0 if gender_str in ['MALE', 'NAM', 'TRAI', '1'] else 0.0
        itch_val  = 1.0 if itch_str   in ['YES', 'CÓ', 'TRUE', '1'] else 0.0
        grew_val  = 1.0 if grew_str   in ['YES', 'CÓ', 'TRUE', '1'] else 0.0
        bleed_val = 1.0 if bleed_str  in ['YES', 'CÓ', 'TRUE', '1'] else 0.0

        #Xử lý Age 
        try:
            raw_age = meta_dict.get('age')
            # Nếu không có tuổi hoặc chuỗi rỗng -> lấy mặc định 30
            if raw_age is None or str(raw_age).strip() == "":
                age_val = 30.0
            else:
                age_val = float(raw_age)
        except ValueError:
            print(f"Cảnh báo: Tuổi không hợp lệ '{raw_age}', dùng mặc định 30.0")
            age_val = 30.0

        input_data = [age_val, gen_val, itch_val, grew_val, bleed_val]
        
        # Tạo Tensor shape [1, 5] (Batch size = 1)
        return torch.tensor([input_data], dtype=torch.float32).to(self.device)

    def analyze(self, image_source, patient_data):
        # 1. Xử lý ảnh
        try:
            if isinstance(image_source, str):
                image = Image.open(image_source).convert("RGB")
            else:
                image = image_source.convert("RGB") 
            
            img_tensor = self.transform(image).unsqueeze(0).to(self.device)
        except Exception as e:
            return {"error": f"Lỗi ảnh: {str(e)}"}

        # 2. Xử lý thông tin
        meta_tensor = self._process_metadata(patient_data)

        # 3. Dự đoán
        with torch.no_grad():
            outputs = self.model(img_tensor, meta_tensor)
            probs = F.softmax(outputs, dim=1)[0]

        # 4. Trả kết quả JSON
        sorted_idx = probs.argsort(descending=True)
        top_idx = sorted_idx[0].item()
        top_label = CLASS_NAMES[top_idx]
        confidence = probs[top_idx].item() * 100

        return {
            "status": "success",
            "diagnosis": {
                "code": top_label,
                "name": DISEASE_MAP.get(top_label, top_label),
                "confidence": round(confidence, 2)
            },
            "patient_info": patient_data
        }