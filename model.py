import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import MinMaxScaler

# Training data
# Features: [sim_changed, new_device, unusual_location, otp_failures, transaction_amount]
# Label: 1 = Fraud, 0 = Safe

X_train = np.array([
    [1, 1, 1, 3, 50000],  # fraud
    [1, 1, 0, 2, 30000],  # fraud
    [1, 0, 1, 3, 45000],  # fraud
    [0, 1, 1, 2, 40000],  # fraud
    [1, 1, 1, 2, 60000],  # fraud
    [1, 0, 0, 3, 55000],  # fraud
    [0, 1, 1, 3, 35000],  # fraud
    [1, 1, 0, 3, 70000],  # fraud
    [0, 0, 0, 0, 4500],   # safe
    [0, 0, 0, 0, 1200],   # safe
    [0, 0, 0, 1, 3000],   # safe
    [0, 1, 0, 0, 2000],   # safe
    [0, 0, 1, 0, 5000],   # safe
    [0, 0, 0, 0, 800],    # safe
    [0, 0, 0, 1, 1500],   # safe
    [0, 1, 0, 1, 4000],   # safe
])

y_train = np.array([1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0])

scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X_train)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_scaled, y_train)

def predict_fraud(sim_changed, new_device, unusual_location, otp_failures, transaction_amount):
    features = np.array([[sim_changed, new_device, unusual_location, otp_failures, transaction_amount]])
    features_scaled = scaler.transform(features)
    
    fraud_prob = model.predict_proba(features_scaled)[0][1]
    is_fraud = model.predict(features_scaled)[0]
    
    # Calculate trust score (inverse of fraud probability)
    trust_score = round((1 - fraud_prob) * 100)
    
    # Calculate component scores
    device_trust = 40 if new_device else 95
    sim_trust = 45 if sim_changed else 92
    behavior_trust = 50 if otp_failures > 1 else 97
    location_trust = 60 if unusual_location else 88
    
    return {
        "trust_score": trust_score,
        "is_fraud": bool(is_fraud),
        "fraud_probability": round(fraud_prob * 100),
        "risk_level": "High" if fraud_prob > 0.7 else "Medium" if fraud_prob > 0.3 else "Low",
        "scores": {
            "device_trust": device_trust,
            "sim_trust": sim_trust,
            "behavior": behavior_trust,
            "location": location_trust
        }
    }