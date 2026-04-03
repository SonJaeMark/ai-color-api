from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from config import setup_cors
from utils import generate_palette_v2


app = FastAPI()
setup_cors(app)

class ColorInput(BaseModel):
    primary: str
    secondary: Optional[str] = None
    mode: Optional[str] = None  # "light" or "dark"

@app.get("/")
def root():
    return {"message": "AI Color Generator API v2 🚀"}

@app.post("/generate")
def generate(data: ColorInput):
    result = generate_palette_v2(
        primary=data.primary,
        secondary=data.secondary,
        mode=data.mode
    )
    return result