# Mobile Fraudulent Payment Detection - AI Coding Agent Instructions

## Project Overview
Real-time fraud detection system for mobile payments using Isolation Forest anomaly detection. Transaction requests flow through a FastAPI endpoint, get scored by a pre-trained model, and trigger alerts for suspicious activity.

**Key insight**: The system is designed for rapid inference - model decisions must be sub-millisecond (production requirement for mobile payment processing).

## Architecture & Data Flow

### Components
1. **API Layer** (`api/`): FastAPI server with single POST endpoint `/transaction`
   - Input: Transaction object (user_id, amount, hour, location_change, device_change, txn_count_1h)
   - Output: JSON with fraud flag, risk_score, and message
   - Dependencies: joblib (model loading), pydantic (schema validation)

2. **ML Model** (`model/train.py`): Isolation Forest (300 estimators, 3% contamination)
   - Operates on 5 features: amount, hour, location_change, device_change, txn_count_1h
   - Prediction: -1 = anomaly/fraud, 1 = normal
   - Decision function: anomaly score (lower = more anomalous)

3. **Alerts** (`alerts/alert.py`): Simple stdout alerts (currently placeholder - intended for Slack/email)
   - Triggered on prediction == -1
   - Logs user_id, amount, block status

4. **Data Pipeline** (`data/generate_data.py`): Synthetic dataset generator
   - Creates 20K transactions with embedded fraud logic
   - Fraud triggers: amount > ₹10K OR location_change OR device_change OR txn_count_1h > 5

### Critical Integration Points
- **Model Loading**: `fraud_model.pkl` loaded on app startup (blocking operation - optimize for startup time)
- **Feature Extraction**: `main.py` manually constructs feature array from transaction - keep order synchronized with `train.py`
- **Alert Trigger**: Happens inside transaction endpoint - ensure non-blocking for production

## Development Workflows

### Running the System
```bash
# Terminal 1: Generate training data
python data/generate_data.py                    # Outputs: transactions.csv

# Terminal 2: Train model
python model/train.py                           # Outputs: fraud_model.pkl

# Terminal 3: Start API
uvicorn api.main:app --reload                   # Runs on http://localhost:8000
```

### Testing Transactions
```bash
curl -X POST "http://localhost:8000/transaction" \
  -H "Content-Type: application/json" \
  -d '{"user_id":123,"amount":15000,"hour":2,"location_change":1,"device_change":0,"txn_count_1h":3}'
```

### Key Debugging Patterns
- Model predictions: Use `model.predict()` for binary (-1/1), `decision_function()` for scores
- Feature order matters: `[amount, hour, location_change, device_change, txn_count_1h]` - any reorder breaks scoring
- Alert mock: Replace `send_alert()` in `alerts/alert.py` with actual integration (Slack webhook, email)

## Code Patterns & Conventions

### Pydantic Schemas
- Use `BaseModel` for all API inputs (see `schemas.Transaction`)
- Always validate numeric ranges if needed (hours: 0-23, binary fields: 0-1)

### ML Model Conventions
- IsolationForest: Prefer over One-Class SVM for 5-feature detection (fast, no kernel tuning)
- Contamination parameter (0.03) reflects expected fraud rate - tune from data analysis, not guesswork
- Always save model with joblib, not pickle (better versioning support)

### Error Handling (Currently Missing)
- No validation that features are in expected ranges (e.g., hour 0-23)
- No fallback if `fraud_model.pkl` not found - will crash on startup
- Alert failures won't surface to user

## Project-Specific Gotchas

1. **Feature Synchronization**: If training features change, manually update feature list in both `train.py` (line ~12) and `main.py` (lines ~16-21)
2. **Model Staleness**: No versioning system - retraining overwrites without backup
3. **Alert Integration**: Currently prints to stdout; production needs async task queue (Celery) to avoid blocking requests
4. **Risk Score Sign**: Anomaly score can be negative (more anomalous = more negative) - current code converts to float but doesn't explain semantics

## Next Priority Enhancements
- Add request/response logging with transaction_id for audit trails
- Implement model versioning (v1, v2) with automatic selection
- Make alert system async (use FastAPI background tasks or Celery)
- Add `/health` endpoint for deployment monitoring
- Implement feature range validation in Transaction schema
