from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
import pickle
from sklearn.preprocessing import StandardScaler

app = Flask(__name__)

# Load trained model
with open("best_heart_disease_model.pkl", "rb") as f:
    model = pickle.load(f)

data = pd.read_csv("./heart.csv") 

# Handle missing values
data = data.dropna()  

X = data.iloc[:, :-1]

# Load scaler for consistent preprocessing
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)


@app.route("/", methods=["GET"])
def home():
    return "Heart Disease Prediction API is Running!"

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.json
        features = np.array([[
            data["age"], data["sex"], data["cp"], data["trestbps"], data["chol"],
            data["fbs"], data["restecg"], data["thalach"], data["exang"],
            data["oldpeak"], data["slope"], data["ca"], data["thal"]
        ]])
        
        # Standardize input
        features_scaled = scaler.transform(features)
        
        # Predict class and probability
        prediction = model.predict(features_scaled)[0]
        probability = model.predict_proba(features_scaled)[0][1]  # Probability of heart disease (class 1)
        
        return jsonify({
            "prediction": "No heart disease" if prediction == 0 else "Heart disease detected",
            "probability": round(probability * 100, 2)  # Convert to percentage
        })
    
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
