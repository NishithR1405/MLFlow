from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib

model = joblib.load("model.pkl")

app = FastAPI()

class StudentInput(BaseModel):
    hours: float

@app.get("/")
def home():
    return {"message": "Student Score Prediction API"}

@app.post("/predict")
def predict(data: StudentInput):
    if data.hours < 0:
        raise HTTPException(
            status_code=400,
            detail="Hours cannot be negative"
        )

    prediction = model.predict([[data.hours]])

    return {
        "hours_studied": data.hours,
        "predicted_score": round(prediction[0], 2)
    }