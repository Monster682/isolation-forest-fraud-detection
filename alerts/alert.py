def send_alert(txn):
    print("🚨 FRAUD ALERT 🚨")
    print(f"User: {txn['user_id']} | Amount: ₹{txn['amount']}")
