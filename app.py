import joblib
import pandas as pd
import numpy as np
from fastapi import FastAPI
from pydantic import BaseModel
import time

app = FastAPI(title="Credit Card Fraud Detection API", description="Real-time inference API for fraud detection")

print("Loading XGBoost Model...")
model = joblib.load('models/xgboost_fraud_model.pkl')
try:
    with open('models/threshold.txt', 'r') as f:
        threshold = float(f.read().strip())
except FileNotFoundError:
    threshold = 0.5
print(f"Model loaded successfully. Optimal prediction threshold in use: {threshold}")

# Define the expected JSON payload mapping to our features
class Transaction(BaseModel):
    Time: float
    V1: float
    V2: float
    V3: float
    V4: float
    V5: float
    V6: float
    V7: float
    V8: float
    V9: float
    V10: float
    V11: float
    V12: float
    V13: float
    V14: float
    V15: float
    V16: float
    V17: float
    V18: float
    V19: float
    V20: float
    V21: float
    V22: float
    V23: float
    V24: float
    V25: float
    V26: float
    V27: float
    V28: float
    Amount: float

@app.post("/predict")
async def predict_fraud(transaction: Transaction):
    start_time = time.time()
    
    # Fast approximated RobustScaling (median and interquartile range from EDA)
    # Using true values from EDA. Amount Median = 22.0, IQR = 77.165 - 5.6 = 71.565
    scaled_amount = (transaction.Amount - 22.0) / 71.565
    # Dummy robust scaling for Time as well. IQR derived from dataset time spread.
    scaled_time = (transaction.Time - 84692.5) / 85277.5
    
    features = [
        scaled_amount, scaled_time,
        transaction.V1, transaction.V2, transaction.V3, transaction.V4, transaction.V5,
        transaction.V6, transaction.V7, transaction.V8, transaction.V9, transaction.V10,
        transaction.V11, transaction.V12, transaction.V13, transaction.V14, transaction.V15,
        transaction.V16, transaction.V17, transaction.V18, transaction.V19, transaction.V20,
        transaction.V21, transaction.V22, transaction.V23, transaction.V24, transaction.V25,
        transaction.V26, transaction.V27, transaction.V28
    ]
    
    # We construct the exact columns the model expects
    input_df = pd.DataFrame([features], columns=[
        'scaled_amount', 'scaled_time',
        'V1', 'V2', 'V3', 'V4', 'V5', 'V6', 'V7', 'V8', 'V9', 'V10',
        'V11', 'V12', 'V13', 'V14', 'V15', 'V16', 'V17', 'V18', 'V19', 'V20',
        'V21', 'V22', 'V23', 'V24', 'V25', 'V26', 'V27', 'V28'
    ])
    
    # Inference
    prob = model.predict_proba(input_df)[0][1]
    is_fraud = int(prob >= threshold)
    
    latency_ms = (time.time() - start_time) * 1000
    
    return {
        "is_fraud": bool(is_fraud),
        "fraud_probability": float(prob),
        "latency_ms": latency_ms
    }
