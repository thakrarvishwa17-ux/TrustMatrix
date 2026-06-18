from flask import Flask, render_template, request, redirect, session
from model import predict_fraud

app = Flask(__name__)
app.secret_key = "trustmatrix2026"

VALID_USERNAME = "admin"
VALID_PASSWORD = "trust123"

@app.route("/", methods=["GET", "POST"])
def login():
    error = ""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username == VALID_USERNAME and password == VALID_PASSWORD:
            session["logged_in"] = True
            return redirect("/dashboard")
        else:
            error = "Invalid username or password"
    return render_template("login.html", error=error)

@app.route("/dashboard")
def dashboard():
    if not session.get("logged_in"):
        return redirect("/")

    # ML model predicting live risk
    result = predict_fraud(
        sim_changed=1,
        new_device=1,
        unusual_location=0,
        otp_failures=2,
        transaction_amount=50000
    )
    print("ML RESULT:", result)

    data = {
        "user": "Raj Kumar",
        "trust_score": result["trust_score"],
        "alerts_today": 2,
        "device": "iPhone 14 · iOS 17",
        "location": "Ahmedabad, GJ",
        "sim_status": "Changed recently",
        "risk_level": result["risk_level"],
        "auth_method": "Biometric + OTP",
        "is_fraud": result["is_fraud"],
        "fraud_probability": result["fraud_probability"],
        "scores": result["scores"],
        "alerts": [
            {"icon": "red", "icon_name": "ti-sim-card", "title": "SIM change detected", "desc": "New SIM registered on account", "time": "2m ago"},
            {"icon": "orange", "icon_name": "ti-device-mobile", "title": "New device login", "desc": "Unrecognized device · Mumbai", "time": "14m ago"},
            {"icon": "green", "icon_name": "ti-check", "title": "OTP verified", "desc": "Login confirmed successfully", "time": "18m ago"}
        ],
        "transactions": [
            {"icon": "green", "icon_name": "ti-check", "name": "HDFC Bank Transfer", "meta": "Today · 10:32 AM · Trusted device", "amount": "4,500", "color": "safe"},
            {"icon": "orange", "icon_name": "ti-alert-triangle", "name": "UPI — Unknown payee", "meta": "Today · 10:41 AM · New device", "amount": "12,000", "color": "warn"},
            {"icon": "red", "icon_name": "ti-x", "name": "Net Banking — Blocked", "meta": "Today · 10:44 AM · SIM anomaly", "amount": "50,000", "color": "danger"},
            {"icon": "green", "icon_name": "ti-check", "name": "Electricity Bill", "meta": "Yesterday · 6:10 PM · Trusted", "amount": "1,240", "color": "safe"}
        ]
    }

    return render_template("dashboard.html", data=data)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "_main_":
    app.run(debug=True)