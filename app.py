from flask import Flask, request, jsonify
import joblib
import numpy as np
import re

app = Flask(__name__)

# Load model and scaler
model = joblib.load("phishing_model.pkl")
scaler = joblib.load("scaler.pkl")

# Feature extraction (same as your project)
def extract_features(url):
    features = []

    features.append(len(url))
    features.append(url.count('.'))
    features.append(url.count('-'))
    features.append(url.count('@'))
    features.append(1 if "https" in url else 0)
    features.append(url.count('/'))
    features.append(url.count('?'))
    features.append(url.count('='))
    features.append(1 if "www" in url else 0)

    ip_pattern = r'(\d{1,3}\.){3}\d{1,3}'
    features.append(1 if re.search(ip_pattern, url) else 0)

    return features

# API route
@app.route("/predict", methods=["POST"])
def predict():
    data = request.json
    url = data["url"]

    features = np.array([extract_features(url)])
    features = scaler.transform(features)

    prediction = model.predict(features)[0]

    result = "Phishing" if prediction == 1 else "Legitimate"

    return jsonify({"result": result})

if __name__ == "__main__":
    app.run(debug=True)