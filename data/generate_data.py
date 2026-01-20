import pandas as pd
import numpy as np

np.random.seed(42)

N = 20000

data = {
    "user_id": np.random.randint(1, 5000, N),
    "amount": np.random.exponential(scale=2000, size=N),
    "hour": np.random.randint(0, 24, N),
    "location_change": np.random.randint(0, 2, N),
    "device_change": np.random.randint(0, 2, N),
    "txn_count_1h": np.random.poisson(2, N),
}

df = pd.DataFrame(data)

# Fraud logic (hidden)
df["is_fraud"] = (
    (df["amount"] > 10000) |
    (df["location_change"] == 1) |
    (df["device_change"] == 1) |
    (df["txn_count_1h"] > 5)
).astype(int)

df.to_csv("transactions.csv", index=False)
print("Dataset generated")
