import numpy as np
import joblib
import os
from sklearn.ensemble import IsolationForest

os.makedirs("model", exist_ok=True)

# -------- REALISTIC TRANSACTION DATA --------
n = 2000

amount = np.random.normal(2000, 1500, n).clip(50, 20000)
hour = np.random.randint(0, 24, n)
location_change = np.random.binomial(1, 0.1, n)
device_change = np.random.binomial(1, 0.05, n)
txn_count = np.random.poisson(2, n).clip(0, 10)

X = np.column_stack([
    amount,
    hour,
    location_change,
    device_change,
    txn_count
])

# -------- TRAIN MODEL --------
model = IsolationForest(
    n_estimators=300,
    contamination=0.05,   # 5% fraud assumption
    random_state=42
)

model.fit(X)

joblib.dump(model, "model/fraud_model.pkl")
print("✅ Model retrained with realistic data")
