from fastapi import FastAPI
from pydantic import BaseModel
from utils import generate_palette

app = FastAPI()

class ColorInput(BaseModel):
    primary: str

@app.get("/")
def root():
    return {"message": "AI Color Generator API is running 🚀"}

@app.post("/generate")
def generate(data: ColorInput):
    result = generate_palette(data.primary)
    return result