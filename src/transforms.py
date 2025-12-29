from torchvision import transforms
from .config import IMAGE_SIZE

def get_transforms():
    # Chỉ cần transform cho việc dự đoán (Validation)
    return transforms.Compose([
        transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])