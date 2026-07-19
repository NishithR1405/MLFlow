from fastapi import FastAPI
import pandas as pd

app = FastAPI()

df = pd.read_csv("weather.csv")

@app.get("/")
def home():
    return {"message": "Weather Prediction API Running"}

@app.get("/predict")
def predict(temp: float):
    if temp > 30:
        result = "Hot Weather"
    elif temp > 20:
        result = "Moderate Weather"
    else:
        result = "Cold Weather"
    return {"temperature": temp, "prediction": result}
