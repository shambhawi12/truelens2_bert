from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sys
import os

# Ensure the root directory is in Python's import path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import your prediction function from src
try:
    from src.predict import predict  # Adjust function name if it's different in predict.py
except ImportError:
    # Fallback if your predict.py function has a different name
    predict = None

app = FastAPI(title="TrueLens API")

# Enable CORS so your v0 React frontend can communicate with FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class NewsItem(BaseModel):
    text: str

@app.get("/")
def home():
    return {"status": "TrueLens API is running"}

@app.post("/predict")
def predict_news(item: NewsItem):
    if predict:
        result = predict(item.text)
        return {"result": result}
    return {"error": "Prediction function not loaded properly"}