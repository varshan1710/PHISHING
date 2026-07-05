# Phishing URL Detector 🛡️

A machine learning-based phishing detection system that flags malicious URLs in real-time. This project features a Python Flask backend running a Random Forest Classifier, and a Chrome Extension (Manifest V3) that monitors tabs and warns users about phishing URLs.

---

## Project Structure

```text
├── phishing-extension/       # Chrome Extension (Manifest V3)
│   ├── background.js         # Service worker tracking tabs and making API calls
│   ├── manifest.json         # Extension manifest & configuration
│   ├── popup.html            # Simple extension pop-up interface
│   └── warning.html          # HTML warning page displayed for phishing URLs
├── app.py                    # Flask API for real-time URL prediction
├── train_model.py            # Model training and validation script
├── dataset.csv               # Dataset containing URLs and phishing labels
├── phishing_model.pkl        # Trained Random Forest classifier
├── scaler.pkl                # Fitted StandardScaler for URL features
└── README.md                 # Project documentation
```

---

## Features

1. **Feature Extraction**:
   - URL length
   - Dot, hyphen, @ symbol, slash, question mark, equals count
   - HTTPS presence check
   - "www" token check
   - IP address detection in URL
2. **Machine Learning Classifier**:
   - Random Forest model trained on historical phishing URL datasets.
   - Saves fitted `StandardScaler` to ensure features match the trained distribution during real-time inference.
3. **Chrome Extension (Manifest V3)**:
   - Tracks navigation in browser tabs.
   - Asynchronously queries the Flask API with the current URL.
   - Blocks/redirects user to a local `warning.html` page if the URL is classified as "Phishing".

---

## Getting Started

### 1. Backend Setup

First, ensure you have Python 3 installed. Then install the necessary dependencies:

```bash
pip install flask numpy pandas scikit-learn joblib
```

#### Run the Flask Server

Start the API backend:

```bash
python app.py
```

The Flask server will start running on `http://127.0.0.1:5000`.

*(Optional)* If you want to retrain the model, run:
```bash
python train_model.py
```

---

### 2. Chrome Extension Setup

1. Open Google Chrome.
2. Navigate to `chrome://extensions/`.
3. Enable **Developer mode** (toggle in the top-right corner).
4. Click on **Load unpacked** in the top-left corner.
5. Select the `phishing-extension` directory from this project workspace.
6. The extension is now active and will query your local Flask server on every page load.

---

## Prediction Endpoint

- **URL**: `http://127.0.0.1:5000/predict`
- **Method**: `POST`
- **Headers**: `Content-Type: application/json`
- **Body**:
  ```json
  {
    "url": "http://example-phishing-site.com"
  }
  ```
- **Response**:
  ```json
  {
    "result": "Phishing"  // Or "Legitimate"
  }
  ```
