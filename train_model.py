import pandas as pd
import numpy as np
import re
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
import joblib


dataset_path = "V:\\mini_extension\\dataset.csv"   # change if needed


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


df = pd.read_csv(dataset_path)


# Remove Duplicate Rows

df.drop_duplicates(inplace=True)
print("✅ Duplicates removed")


# Convert URLs → Features

urls = df.iloc[:, 0]      # first column = URL
y = df.iloc[:, -1]        # last column = label

X = [extract_features(url) for url in urls]

# -----------------------------
# 🔹 Train-Test Split
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# -----------------------------
# 🔹 Scaling
# -----------------------------
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# -----------------------------
# 🔹 Model Training
# -----------------------------
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# -----------------------------
# 🔹 Evaluation
# -----------------------------
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print("✅ Accuracy:", accuracy)

# -----------------------------
# 🔹 Save Model & Scaler
# -----------------------------
joblib.dump(model, "phishing_model.pkl")
joblib.dump(scaler, "scaler.pkl")

print("✅ Model & Scaler saved successfully!")