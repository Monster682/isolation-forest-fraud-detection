Mobile Payment Fraud Detection System

Overview
This project is an end-to-end real-time fraud detection system for mobile banking transactions.
It uses Machine Learning (Isolation Forest) to detect anomalous transactions and provides a
web-based interface to visually demonstrate whether a transaction is approved or blocked.

The system is designed to simulate how Small Finance Banks detect and prevent fraudulent
mobile payments in real time.

--------------------------------------------------------------------

Key Features
- Real-time fraud detection using anomaly detection
- Machine Learning model trained on realistic transaction data
- FastAPI backend for transaction scoring
- Interactive website to test transactions visually
- Fraud alerts triggered for suspicious transactions
- End-to-end working demo (ML + API + Website)

--------------------------------------------------------------------

Fraud Detection Logic
The system uses Isolation Forest, an unsupervised anomaly detection algorithm.

Instead of fixed rules, the model learns normal transaction behavior and flags
transactions that significantly deviate from normal patterns.

A transaction is evaluated using the following signals:
- Transaction amount
- Hour of transaction (0–23)
- Location change (same or new location)
- Device change (same or new device)
- Number of transactions in the last hour

Transactions that appear highly unusual are classified as fraudulent and blocked.

--------------------------------------------------------------------

Project Structure

Mobile-Payment-Fraud-Detection/
│
├── api/
│   ├── main.py          FastAPI application
│   ├── schemas.py       Request validation models
│   └── __init__.py
│
├── model/
│   ├── train_model.py   Model training script
│   └── fraud_model.pkl  Trained ML model
│
├── alerts/
│   ├── alert.py         Fraud alert handler
│   └── __init__.py
│
├── website/
│   ├── index.html       Frontend UI
│   ├── style.css        UI styling
│   └── script.js        Frontend logic
│
└── requirements.txt


--------------------------------------------------------------------

Technology Stack
Backend:
- Python
- FastAPI
- Scikit-learn
- Joblib

Machine Learning:
- Isolation Forest (Anomaly Detection)

Frontend:
- HTML
- CSS
- JavaScript

--------------------------------------------------------------------

How to Run the Project

Step 1: Create virtual environment
python -m venv venv
venv\Scripts\activate

Step 2: Install dependencies
pip install -r requirements.txt

Step 3: Train the ML model
python model/train_model.py

Step 4: Start backend server
python -m uvicorn api.main:app --reload

Step 5: Run the website
cd website
python -m http.server 5500

Open browser:
http://127.0.0.1:5500/index.html

--------------------------------------------------------------------

Demo Transaction Values

Normal Transaction (Approved)
User ID: 1
Amount: 500
Hour: 14
Location Change: 0
Device Change: 0
Txns Last 1 Hour: 1

Fraudulent Transaction (Blocked)
User ID: 9
Amount: 18000
Hour: 2
Location Change: 1
Device Change: 1
Txns Last 1 Hour: 6

--------------------------------------------------------------------

Use Case
This project demonstrates how banks can:
- Detect fraudulent payments in real time
- Reduce financial losses
- Alert users proactively
- Move beyond rule-based fraud detection

--------------------------------------------------------------------

Future Enhancements
- Risk score visualization
- Transaction history dashboard
- Hybrid ML + rule-based detection
- User authentication
- Cloud deployment (AWS)

--------------------------------------------------------------------

Author
Vaibhav Desai
AI / ML Engineer
