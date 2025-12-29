import sys
import os

# Thêm thư mục gốc vào path để import được module src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi import FastAPI, File, UploadFile, Form
from src.inference import MedicalAnalyzer
from PIL import Image
import io
import uvicorn

app = FastAPI()

# Load model 1 lần duy nhất khi khởi động server
analyzer = MedicalAnalyzer()

@app.post("/analyze")
async def analyze_skin(
    age: float = Form(...),
    gender: str = Form(...),
    itch: str = Form(...),
    grew: str = Form(...),
    bleed: str = Form(...),
    file: UploadFile = File(...)
):
    contents = await file.read()
    image = Image.open(io.BytesIO(contents))
    
    patient_data = {
        "age": age, "gender": gender, 
        "itch": itch, "grew": grew, "bleed": bleed
    }
    
    return analyzer.analyze(image, patient_data)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)