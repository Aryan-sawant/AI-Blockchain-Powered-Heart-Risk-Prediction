import streamlit as st
import requests
from web3 import Web3
import json
import os
import pandas as pd
import plotly.express as px
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Blockchain connection
ALCHEMY_API_KEY = os.getenv("ALCHEMY_API_KEY")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
CONTRACT_ADDRESS = "0x9829FBEA9637244823A89384108662C654E50E5c"

# Connect to Polygon Amoy Testnet
w3 = Web3(Web3.HTTPProvider(f"https://polygon-amoy.g.alchemy.com/v2/{ALCHEMY_API_KEY}"))

# Load contract ABI
with open("HeartRiskPredictionABI.json") as f:
    contract_abi = json.load(f)

contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=contract_abi)

# --- Gemini API Setup ---
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash')  # Use 'gemini-pro'


# --- Streamlit Page Configuration for Full Width ---
st.set_page_config(layout="wide")

# --- Custom CSS for Styling (Major UI/UX Improvements) ---
st.markdown(
    """
<style>
/* Root Element */
:root {
  --primary-color: #e91e63; /* Pink */
  --secondary-color: #9c27b0; /* Purple */
  --background-color: #f8f9fa; /* Lighter gray */
  --text-color: #4a4a4a; /* Darker gray */
  --font-main: 'Roboto', sans-serif; /* Main font */
  --font-headers: 'Playfair Display', serif; /* Header font */
  --font-accent: 'Montserrat', sans-serif; /* Accent font */
}


/* Background Image */
.stApp {
    background-image: url('https://img.freepik.com/free-vector/pastel-gradient-2_78370-257.jpg'); /*  Replace with a high-res, relevant image */
    background-size: cover;
    background-repeat: no-repeat;
    background-attachment: fixed; /* Keeps the background fixed during scroll */
    font-family: var(--font-main);
    color: var(--text-color);
}

/* Main Title (3D-ish, Animated) */
.main-title {
    color: white;
    text-align: center;
    padding: 30px 0;
    font-size: 5.5em;
    font-weight: bold;
    text-shadow: 4px 4px 6px rgba(0, 0, 0, 0.6); /* Stronger, more 3D-like shadow */
    background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
    border-radius: 20px;
    margin-bottom: 40px;
    box-shadow: 0 10px 20px rgba(0, 0, 0, 0.5);
    animation: pulse-animation 2s infinite alternate, color-change 5s infinite alternate; /* Pulse and color change */
    transition: all 0.3s ease;
    position: relative; /* For pseudo-element */
    overflow: hidden;   /* Hide overflowing pseudo-element */
    font-family: var(--font-headers); /* Header font */
}

/* Animated Gradient Background (Subtle) */
.main-title::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 200%; /* Double the width */
    height: 100%;
    background: linear-gradient(135deg, rgba(255,255,255,0.2) 0%, rgba(255,255,255,0) 50%, rgba(255,255,255,0.2) 100%);
    z-index: -1;
    animation: shine 5s linear infinite;
}

@keyframes shine {
    0% { transform: translateX(-100%); }
    100% { transform: translateX(100%); }
}


@keyframes pulse-animation {
    0% { transform: scale(1); }
    100% { transform: scale(1.04); }
}

@keyframes color-change {
    0% { background: linear-gradient(135deg, var(--primary-color), var(--secondary-color)); }
    100% { background: linear-gradient(135deg, var(--secondary-color), var(--primary-color)); }
}

.main-title:hover {
    transform: scale(1.02) translateY(-5px); /* More lift on hover */
    box-shadow: 0 12px 24px rgba(0, 0, 0, 0.6);
}

/* Subheaders */
.st-emotion-cache-r421ms {
    color: var(--text-color);
    padding-top: 25px;
    font-weight: bold;
    font-size: 2.2em; /* Increased size */
    text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.2); /* Subtle text shadow */
    font-family: var(--font-headers); /* Header font */
    letter-spacing: -0.02em; /* Slightly reduce letter spacing for elegance */
}

/* Input Labels and Radio/Selectbox Labels */
.st-emotion-cache-16txtl3,
.st-eb-zF,
.streamlit-expanderHeader {
    color: #555;
    font-weight: 600; /* Slightly bolder */
    font-family: var(--font-accent); /* Accent font */
    font-size: 1.2em; /* Slightly larger */
}

/* Input Fields (Slightly more styling)*/
.st-emotion-cache-1vbkxwb, .st-emotion-cache-1iqg59j, .st-emotion-cache-1b76d8j{
    border: 1px solid #ccc;
    border-radius: 8px;
    padding: 12px; /* Increased padding */
    background-color: rgba(255, 255, 255, 0.8); /* Slightly transparent white */
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    transition: border-color 0.3s ease, box-shadow 0.3s ease;
    font-size: 1.1em; /* Slightly larger input text */
}
/* Hover effect for input fields */
.st-emotion-cache-1vbkxwb:hover, .st-emotion-cache-1iqg59j:hover, .st-emotion-cache-1b76d8j:hover,
.st-emotion-cache-1vbkxwb:focus-within, .st-emotion-cache-1iqg59j:focus-within, .st-emotion-cache-1b76d8j:focus-within {
    border-color: var(--primary-color);
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

/* Buttons (More 3D and Animated) */
.stButton>button {
    background-color: var(--primary-color);
    color: white !important;
    border: none;
    padding: 16px 32px;
    border-radius: 15px;
    cursor: pointer;
    transition: all 0.3s ease;
    margin-top: 15px;
    margin-bottom: 15px;
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3);  /* More pronounced shadow */
    font-weight: bold;
    font-size: 1.2rem;
    font-family: var(--font-accent); /* Accent font for buttons */
    text-transform: uppercase;
    position: relative; /* For 3D effect */
    overflow: hidden;   /* Hide overflowing pseudo-element */
    letter-spacing: 0.05em; /* Slight letter spacing for buttons */
}

.stButton>button::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(255, 255, 255, 0.2); /* Light overlay */
    z-index: 1;
    border-radius: 15px;
    opacity: 0; /* Hidden by default */
    transition: opacity 0.3s ease;
}

.stButton>button:hover {
    background-color: #d81b60;
    transform: translateY(-4px) scale(1.03); /* 3D lift and scale */
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.4);
}
.stButton>button:hover::before {
    opacity: 1; /* Show overlay on hover */
}

.stButton>button:active {
    background-color: #c2185b;
    transform: translateY(2px) scale(0.98); /* Smaller on press */
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
}

/* Prediction Boxes (More Distinct) */
.prediction-box-heart-disease {
    background-color: #fde0e6;
    color: var(--secondary-color) !important;
    padding: 25px;  /* More padding */
    border-radius: 20px;
    margin-top: 20px;
    border: 3px solid var(--primary-color);
    font-weight: bold;
    font-size: 1.4em; /* Increased font size */
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
    animation: border-pulse 2s infinite alternate; /* Subtle border animation */
    text-align: center; /* Center text */
}

@keyframes border-pulse {
    0% { border-color: var(--primary-color); }
    100% { border-color: #ff5c8d; } /* Lighter pink */
}

.prediction-box-no-heart-disease {
    background-color: #e8f5e9;
    color: #43a047 !important;
    padding: 25px;
    border-radius: 20px;
    margin-top: 20px;
    border: 3px solid #4caf50;
    font-weight: bold;
    font-size: 1.4em; /* Increased font size */
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
    animation: border-pulse-green 2s infinite alternate;
    text-align: center; /* Center text */
}

@keyframes border-pulse-green {
    0% { border-color: #4caf50; }
    100% { border-color: #81c784; } /* Lighter green */
}



/* Info Box */
.info-box {
    background-color: #e3f2fd;
    color: #3f51b5;
    padding: 20px;
    border-radius: 15px;
    margin-top: 20px;
    border: 2px solid #3f51b5;
    font-weight: 500; /* Slightly bolder */
    font-size: 1.15em;
    line-height: 1.7; /* Improved line height for readability */
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
    font-family: var(--font-main); /* Main font */
}

/* Error/Warning Boxes */
.error-box, .warning-box {
    padding: 15px;
    border-radius: 10px;
    margin-top: 15px;
    font-weight: bold;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    font-family: var(--font-main); /* Main font */
}

.error-box {
    background-color: #ffebee;
    color: #b71c1c;
    border: 2px solid #f44336;
}
.warning-box {
    background-color: #fffde7;
    color: #827717;
    border: 2px solid #ffeb3b;
}

/* Dataframe Styling (Enhanced) */
.dataframe {
    border: 2px solid #dee2e6;
    border-radius: 15px;
    padding: 20px;
    margin-top: 20px;
    background-color: white;
    font-weight: 500; /* Reduced font weight */
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    overflow-x: auto;
    font-size: 1.05em; /* Slightly larger dataframe text */
    font-family: var(--font-main); /* Main font */
}

.dataframe th {
    color: var(--primary-color) !important;
    background-color: #fce4ec;
    font-size: 1.1em;
    text-align: left;
    padding: 12px 18px;
    border-bottom: 3px solid var(--primary-color);
    font-weight: 600; /* Bolder header text */
}

.dataframe td {
    padding: 12px 18px;
    border-bottom: 1px solid #dee2e6;
}

.dataframe tr:nth-child(even) {
    background-color: #f8f9fa;
}

/* Plotly Chart Styling */
.plotly-chart {
  background-color: #f0f0f0;
  border-radius: 15px;       /* More rounded corners */
  padding: 20px;            /* More padding */
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.25);  /* Stronger shadow */
  margin-bottom: 30px;      /* More margin */
  border: 2px solid #CC0000;
  overflow: hidden;         /* Ensures content doesn't overflow */
  transition: transform 0.3s ease; /* Smooth transition for hover */
}

.plotly-chart:hover {
  transform: scale(1.03);   /* Slight zoom on hover */
}


.plotly-chart .Plotlyjs-div > .plotly > .svg-container > .svg > g > .axeslayer-below > .xy > .ytick > text,
.plotly-chart .Plotlyjs-div > .plotly > .svg-container > .svg > g > .axeslayer-below > .xy > .xtick > text,
.plotly-chart .Plotlyjs-div > .plotly > .svg-container > .svg > g > .infolayer > .g-gtitle > .gtitle > text {
    font-weight: 600 !important; /* Bolder chart text */
    font-size: 1.05em !important; /* Slightly larger chart text */
    font-family: var(--font-accent) !important; /* Accent font for chart text */
}


</style>
""",
    unsafe_allow_html=True,
)

st.markdown('<p class="main-title">❤️ Heart Risk Prediction Using Blockchain 🩺</p>', unsafe_allow_html=True) # Reduced title and removed blockchain chain icon

# User input form
st.subheader("Enter Your Medical Details")

col1, col2 = st.columns(2)

with col1:
    age = st.number_input(label="Age (Years)", min_value=1, max_value=100, step=1, label_visibility="visible", help="Enter your age in whole years.")
    sex = st.radio("Gender", ["Female", "Male"], label_visibility="visible", help="Select your gender.")
    cp_options = {0: "Typical Angina", 1: "Atypical Angina", 2: "Non-Anginal Pain", 3: "Asymptomatic"}
    cp = st.selectbox("Type of Chest Pain", options=list(cp_options.keys()), format_func=lambda x: cp_options[x], label_visibility="visible", help="Describe your chest pain: Typical angina is heart-related, atypical angina is probably not, non-anginal pain is not heart-related, asymptomatic means no chest pain.")
    trestbps = st.number_input(label="Resting Blood Pressure (mmHg)", min_value=80, max_value=200, step=1, label_visibility="visible", help="Your blood pressure when resting, measured in mmHg (millimeters of mercury).")
    chol = st.number_input(label="Cholesterol Level (mg/dl)", min_value=100, max_value=600, step=1, label_visibility="visible", help="Your cholesterol level in mg/dl (milligrams per deciliter).")
    fbs = st.radio("Fasting Blood Sugar > 120 mg/dl?", ["No", "Yes"], label_visibility="visible",  help="Have you been told your fasting blood sugar is higher than 120 mg/dl?", index=0)

with col2:
    restecg_options = {0: "Normal", 1: "ST-T Wave Abnormality", 2: "Left Ventricular Hypertrophy"}
    restecg = st.selectbox("Resting ECG Results", options=list(restecg_options.keys()), format_func=lambda x: restecg_options[x], label_visibility="visible", help="Results from a resting electrocardiogram (ECG), a test that measures your heart's electrical activity.")
    thalach = st.number_input(label="Maximum Heart Rate Achieved (bpm)", min_value=60, max_value=250, step=1, label_visibility="visible", help="The highest heart rate you achieved during exercise, in beats per minute (bpm).")
    exang = st.radio("Exercise-Induced Chest Pain?", ["No", "Yes"], label_visibility="visible", help="Do you experience chest pain when you exercise?", index=0)
    oldpeak = st.number_input(label="ST Depression During Exercise (mm)", min_value=0.0, max_value=7.0, step=0.1, label_visibility="visible", help="ST depression measured on an ECG during exercise, in millimeters.  This reflects changes in your heart's electrical activity during exertion.")
    slope_options = {0: "Upsloping", 1: "Flat", 2: "Downsloping"}
    slope = st.selectbox("Slope of ST Segment (Exercise)", options=list(slope_options.keys()), format_func=lambda x: slope_options[x], label_visibility="visible", help="The slope of the ST segment on your ECG during peak exercise. It describes the direction of heart's electrical recovery.")
    ca = st.selectbox("Number of Major Vessels Colored by Fluoroscopy", [0, 1, 2, 3, 4], label_visibility="visible", help="Number of major blood vessels around your heart that show narrowing during a fluoroscopy (an imaging test).")
    thal_options = {0: "Normal", 1: "Fixed Defect", 2: "Reversable Defect", 3: "Thalassemia"}
    thal = st.selectbox("Thalassemia Status", options=list(thal_options.keys()), format_func=lambda x: thal_options[x], label_visibility="visible", help="Thalassemia is a blood disorder.  Select your status if known.")

# Convert user input into API format
user_data = {
    "age": age,
    "sex": 1 if sex == "Male" else 0,
    "cp": cp,
    "trestbps": trestbps,
    "chol": chol,
    "fbs": 1 if fbs == "Yes" else 0,
    "restecg": restecg,
    "thalach": thalach,
    "exang": 1 if exang == "Yes" else 0,
    "oldpeak": int(oldpeak * 10),  # Back to integer for API
    "slope": slope,
    "ca": ca,
    "thal": thal,
}

positive_heart_disease_advice_prompt = f"""
Based on the POSITIVE heart disease risk prediction from our AI model, provide DETAILED, ACTIONABLE, and URGENT advice. Focus on the seriousness of the situation, but maintain a supportive and encouraging tone.

**Medical Profile:** ... (rest of prompt as before)
"""

negative_heart_disease_advice_prompt = f"""
Based on the NEGATIVE heart disease risk prediction from our AI model, provide detailed and encouraging advice to maintain excellent heart health and prevent future problems. The AI indicates **no current indication of heart disease.**

Focus on reinforcing healthy habits and suggesting preventative measures. Avoid any language that suggests the user has heart disease or needs urgent action.

**Provide advice in the following clearly structured sections:** ... (rest of prompt as before)
"""


def generate_health_advice(user_data, prediction_text, prediction_numeric): # Added prediction_numeric
    """Generates tailored health advice using Gemini, based on prediction_numeric."""

    if prediction_numeric == 1: # Use prediction_numeric directly
        prompt = positive_heart_disease_advice_prompt
    else:
        prompt = negative_heart_disease_advice_prompt

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating advice: {str(e)}"



# Button to get AI prediction (Updated UI)
predict_button, blockchain_button, past_predictions_button = st.columns(3) # Horizontal buttons

if predict_button.button("Predict Heart Disease Risk"):
    ai_api_url = "http://127.0.0.1:5000/predict"
    response = requests.post(ai_api_url, json=user_data)

    if response.status_code == 200:
        result = response.json()
        prediction_text = result["prediction"]
        probability = result.get("probability", "N/A")

        prediction_numeric = 0 if prediction_text.lower() == "no heart disease" else 1
        st.session_state.prediction = prediction_numeric

        st.markdown(f'<div class="info-box">Prediction Probability: {probability}</div>', unsafe_allow_html=True)

        # Output Section - Centered (Below Buttons)
        if prediction_numeric == 1:
            st.markdown(f'<div class="prediction-box-heart-disease">AI Model Prediction: <b>Heart Disease</b></div>', unsafe_allow_html=True)
            advice_text = generate_health_advice(user_data, prediction_text, prediction_numeric) # Pass prediction_numeric
            st.subheader("Health Advice based on Prediction")
            st.markdown(f'<div class="info-box">{advice_text}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="prediction-box-no-heart-disease">AI Model Prediction: <b>No Heart Disease</b></div>', unsafe_allow_html=True)
            advice_text = generate_health_advice(user_data, prediction_text, prediction_numeric) # Pass prediction_numeric
            st.subheader("Health Advice based on Prediction")
            st.markdown(f'<div class="info-box">{advice_text}</div>', unsafe_allow_html=True)


# Store prediction on blockchain
if blockchain_button.button("Store on Blockchain") and "prediction" in st.session_state: # Added condition
    try:
        account = w3.eth.account.from_key(PRIVATE_KEY)
        nonce = w3.eth.get_transaction_count(account.address)

        tx = contract.functions.storePrediction(
            age, user_data["sex"], cp, trestbps, chol, user_data["fbs"], restecg, thalach, user_data["exang"],
            user_data["oldpeak"], slope, ca, thal, st.session_state.prediction
        ).build_transaction({
            "from": account.address,
            "gas": 300000,
            "maxFeePerGas": w3.to_wei("50", "gwei"),
            "maxPriorityFeePerGas": w3.to_wei("30", "gwei"),
            "nonce": nonce,
        })

        signed_tx = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        st.success(f"Stored on Blockchain! Transaction Hash: {w3.to_hex(tx_hash)}")
    except Exception as e:
        st.markdown(f'<div class="error-box">⚠️ Blockchain Transaction Failed: {str(e)}</div>', unsafe_allow_html=True)

# Fetch past predictions and visualize trends
if past_predictions_button.button("View Past Predictions & Trends"):
    try:
        account = w3.eth.account.from_key(PRIVATE_KEY)
        user_address = account.address
        prediction_count = contract.functions.getPredictionCount(user_address).call()

        if prediction_count > 0:
            st.subheader("Past Predictions")
            data = []

            for i in range(prediction_count):
                prediction_data = contract.functions.getPrediction(user_address, i).call()
                age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal, prediction, timestamp = prediction_data

                data.append({
                            "Age": age,
                            "Sex": "Male" if sex == 1 else "Female",
                            "Chest Pain Type": cp,
                            "Blood Pressure": trestbps,
                            "Cholesterol": chol,
                            "Fasting Blood Sugar": fbs,
                            "Resting ECG": restecg,
                            "Heart Rate": thalach,
                            "Exercise-Induced Angina": exang,
                            "ST Depression": oldpeak,
                            "Slope of Peak Exercise ST": slope,
                            "Number of Major Vessels": ca,
                            "Thalassemia Type": thal,
                            "Prediction": "Heart Disease" if prediction == 1 else "No Heart Disease",
                            "Timestamp": pd.to_datetime(timestamp, unit='s')
                            })

            df = pd.DataFrame(data)

            st.markdown('<div class="dataframe">', unsafe_allow_html=True)
            st.dataframe(df)
            st.markdown('</div>', unsafe_allow_html=True)


            df["Prediction"] = df["Prediction"].map({"No Heart Disease": 0, "Heart Disease": 1})
            df = df.sort_values(by='Timestamp')

            col_chart1, col_chart2 = st.columns(2)
            col_chart3, col_chart4 = st.columns(2)
            col_chart5, col_chart6 = st.columns(2) # Added more columns for charts
            col_chart7, col_chart8 = st.columns(2) # Added more columns for charts


             # Define a more vibrant color palette
            vibrant_colors = ['#e91e63', '#9c27b0', '#3f51b5', '#2196f3', '#03a9f4', '#00bcd4', '#009688', '#4caf50', '#8bc34a', '#cddc39']


            with col_chart1:
                fig_trend = px.line(df, x="Timestamp", y="Prediction", title="Risk Trend Over Time",
                                    markers=True, color_discrete_sequence=vibrant_colors)
                fig_trend.update_layout(title_font_size=20, paper_bgcolor='#f0f0f0', plot_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig_trend, use_container_width=True)

            with col_chart2:
                fig_pie = px.pie(df, names="Prediction", title="Prediction Distribution", color_discrete_sequence=vibrant_colors)
                fig_pie.update_layout(title_font_size=20, paper_bgcolor='#f0f0f0', plot_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig_pie, use_container_width=True)

            with col_chart3:
                fig_age = px.histogram(df, x="Age", title="Age Distribution", nbins=10, color_discrete_sequence=vibrant_colors)
                fig_age.update_layout(title_font_size=20, paper_bgcolor='#f0f0f0', plot_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig_age, use_container_width=True)

            with col_chart4:
                fig_chol = px.box(df, y="Cholesterol", title="Cholesterol Distribution", color_discrete_sequence=vibrant_colors)
                fig_chol.update_layout(title_font_size=20, paper_bgcolor='#f0f0f0', plot_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig_chol, use_container_width=True)

            col_chart5, col_chart6 = st.columns(2)

            with col_chart5:
                numerical_df = df.drop(columns=["Sex", "Prediction", "Timestamp"])
                fig_corr = px.imshow(numerical_df.corr(), text_auto=True, title="Feature Correlation Heatmap", color_continuous_scale=vibrant_colors)
                fig_corr.update_layout(title_font_size=20, paper_bgcolor='#f0f0f0', plot_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig_corr, use_container_width=True)

            with col_chart6:
                fig_bp = px.histogram(df, x="Blood Pressure", title="Blood Pressure Distribution", color_discrete_sequence=vibrant_colors)
                fig_bp.update_layout(title_font_size=20, paper_bgcolor='#f0f0f0', plot_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig_bp, use_container_width=True)

            col_chart7, col_chart8 = st.columns(2)

            with col_chart7:
                fig_cp = px.histogram(df, x="Chest Pain Type", title="Chest Pain Type Distribution", color_discrete_sequence=vibrant_colors)
                fig_cp.update_layout(title_font_size=20, paper_bgcolor='#f0f0f0', plot_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig_cp, use_container_width=True)

            with col_chart8:
                fig_restecg = px.histogram(df, x="Resting ECG", title="Resting ECG Distribution", color_discrete_sequence=vibrant_colors)
                fig_restecg.update_layout(title_font_size=20, paper_bgcolor='#f0f0f0', plot_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig_restecg, use_container_width=True)


        else:
            st.markdown(f'<div class="warning-box">No predictions found!</div>', unsafe_allow_html=True)
    except Exception as e:
        st.markdown(f'<div class="error-box">⚠️ Failed to fetch past predictions: {str(e)}</div>', unsafe_allow_html=True)