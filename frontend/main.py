import streamlit as st
import requests
import os

# =========================
# BACKEND CONFIG
# =========================
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
ENDPOINT = f"{BACKEND_URL}/predict"

st.set_page_config(
    page_title="Customer Churn Predictor",
    layout="centered"
)

st.title("📉 Customer Churn Prediction App")
st.markdown("Enter customer details to predict churn probability.")

# =========================
# INPUT FIELDS
# =========================

gender = st.selectbox("Gender", ["Male", "Female"])
SeniorCitizen = st.selectbox("Senior Citizen", [0, 1])
Partner = st.selectbox("Partner", ["Yes", "No"])
Dependents = st.selectbox("Dependents", ["Yes", "No"])
tenure = st.slider("Tenure (months)", 0, 72, 12)

PhoneService = st.selectbox("Phone Service", ["Yes", "No"])
MultipleLines = st.selectbox("Multiple Lines", ["Yes", "No", "No phone service"])
InternetService = st.selectbox("Internet Service", ["DSL", "Fiber optic", "No"])

OnlineSecurity = st.selectbox("Online Security", ["Yes", "No", "No internet service"])
OnlineBackup = st.selectbox("Online Backup", ["Yes", "No", "No internet service"])
DeviceProtection = st.selectbox("Device Protection", ["Yes", "No", "No internet service"])
TechSupport = st.selectbox("Tech Support", ["Yes", "No", "No internet service"])
StreamingTV = st.selectbox("Streaming TV", ["Yes", "No", "No internet service"])
StreamingMovies = st.selectbox("Streaming Movies", ["Yes", "No", "No internet service"])

Contract = st.selectbox("Contract", ["Month-to-month", "One year", "Two year"])
PaperlessBilling = st.selectbox("Paperless Billing", ["Yes", "No"])
PaymentMethod = st.selectbox(
    "Payment Method",
    [
        "Electronic check",
        "Mailed check",
        "Bank transfer (automatic)",
        "Credit card (automatic)"
    ]
)

MonthlyCharges = st.number_input(
    "Monthly Charges",
    min_value=0.0,
    max_value=200.0,
    value=70.0
)

TotalCharges = st.number_input(
    "Total Charges",
    min_value=0.0,
    max_value=10000.0,
    value=2000.0
)

# =========================
# PREDICTION
# =========================

if st.button("🔍 Predict Churn"):
    payload = {
        "gender": gender,
        "SeniorCitizen": SeniorCitizen,
        "Partner": Partner,
        "Dependents": Dependents,
        "tenure": tenure,
        "PhoneService": PhoneService,
        "MultipleLines": MultipleLines,
        "InternetService": InternetService,
        "OnlineSecurity": OnlineSecurity,
        "OnlineBackup": OnlineBackup,
        "DeviceProtection": DeviceProtection,
        "TechSupport": TechSupport,
        "StreamingTV": StreamingTV,
        "StreamingMovies": StreamingMovies,
        "Contract": Contract,
        "PaperlessBilling": PaperlessBilling,
        "PaymentMethod": PaymentMethod,
        "MonthlyCharges": MonthlyCharges,
        "TotalCharges": TotalCharges
    }

    try:
        response = requests.post(ENDPOINT, json=payload, timeout=5)

        if response.status_code == 200:
            res = response.json()

            # ✅ CORRECT KEYS FROM BACKEND
            prob = res.get("churn_probability", 0) * 100
            prediction = res.get("churn_prediction", 0)

            st.markdown(f"### 🔢 Churn Probability: **{prob:.2f}%**")

            if prediction == 1:
                st.error("❌ The customer is likely to churn")
            else:
                st.success("✅ The customer is likely to stay")

        else:
            st.error(f"Backend error: {response.status_code}")

    except requests.exceptions.ConnectionError:
        st.error("❌ Cannot connect to backend. Is FastAPI running?")
    except requests.exceptions.Timeout:
        st.error("⏱️ Backend timeout. Try again.")
    except Exception as e:
        st.error(f"Unexpected error: {e}")






