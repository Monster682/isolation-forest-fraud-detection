from pydantic import BaseModel

class Transaction(BaseModel):
    user_id: int
    amount: float
    hour: int
    location_change: int
    device_change: int
    txn_count_1h: int
