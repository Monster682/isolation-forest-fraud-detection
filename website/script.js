function checkFraud() {
    const data = {
        user_id: Number(document.getElementById("user_id").value),
        amount: Number(document.getElementById("amount").value),
        hour: Number(document.getElementById("hour").value),
        location_change: Number(document.getElementById("location").value),
        device_change: Number(document.getElementById("device").value),
        txn_count_1h: Number(document.getElementById("count").value)
    };

    fetch("http://127.0.0.1:8000/transaction", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    })
    .then(res => res.json())
    .then(res => {
        const div = document.getElementById("result");
        if (res.fraud) {
            div.innerHTML = res.message;
            div.style.color = "red";
        } else {
            div.innerHTML = res.message;
            div.style.color = "green";
        }
    });
}
