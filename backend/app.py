from fastapi import FastAPI
from pydantic import BaseModel
import joblib
from config import THRESHOLD, MODEL_PATH
import pandas as pd

# Load pipeline
pipeline = joblib.load(MODEL_PATH)

app = FastAPI(title="Customer Churn Prediction API")

# -------- Input Schema --------
class CustomerData(BaseModel):
    gender: str
    SeniorCitizen: int
    Partner: str
    Dependents: str
    tenure: int
    PhoneService: str
    MultipleLines: str
    InternetService: str
    OnlineSecurity: str
    OnlineBackup: str
    DeviceProtection: str
    TechSupport: str
    StreamingTV: str
    StreamingMovies: str
    Contract: str
    PaperlessBilling: str
    PaymentMethod: str
    MonthlyCharges: float
    TotalCharges: float


@app.get("/")
def root():
    return {"status": "FastAPI running"}


@app.post("/predict")
def predict_churn(data: CustomerData):
    df = pd.DataFrame([data.model_dump()])

    prob = pipeline.predict_proba(df)[:, 1][0]
    prediction = int(prob >= THRESHOLD)

    return {
        "churn_probability": round(prob, 3),
        "churn_prediction": prediction
    }
