from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import joblib
import os

# ✅ Correct imports
from api.schemas import Transaction
from alerts.alert import send_alert

# -------------------------------------------------
# App initialization
# -------------------------------------------------
app = FastAPI(
    title="Mobile Fraudulent Payment Detection",
    description="Real-time fraud detection for mobile banking transactions",
    version="1.0"
)

# -------------------------------------------------
# Enable CORS (for website / frontend)
# -------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------------------------
# Load ML Model (ABSOLUTE PATH - Windows safe)
# -------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "model", "fraud_model.pkl")

try:
    model = joblib.load(MODEL_PATH)
    print("✅ Fraud detection model loaded successfully")
except Exception as e:
    print("❌ Error loading model:", e)
    model = None


# -------------------------------------------------
# Health Check API
# -------------------------------------------------
@app.get("/")
def home():
    return {
        "status": "running",
        "message": "Mobile Fraud Detection API is live"
    }


# -------------------------------------------------
# Fraud Detection API
# -------------------------------------------------
@app.post("/transaction")
def detect_fraud(txn: Transaction):
    if model is None:
        return {
            "fraud": False,
            "message": "Model not loaded"
        }

    # Convert transaction to ML features
    features = np.array([[
        txn.amount,
        txn.hour,
        txn.location_change,
        txn.device_change,
        txn.txn_count_1h
    ]])

    # Run ML prediction
    score = model.decision_function(features)[0]
    prediction = model.predict(features)[0]   # -1 = fraud, 1 = normal

    # Fraud case
    if prediction == -1:
        send_alert(txn.dict())
        return {
            "fraud": True,
            "risk_score": float(score),
            "message": "🚨 Fraud detected. Transaction blocked."
        }

    # Normal case
    return {
        "fraud": False,
        "risk_score": float(score),
        "message": "✅ Transaction approved"
    }
