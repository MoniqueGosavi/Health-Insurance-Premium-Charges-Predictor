from flask import Flask, render_template, request, jsonify
from utils import MedicalInsurance
import config
import streamlit as st
import requests
import base64

app = Flask(__name__)

# Flask API endpoint (make sure Flask app is running)
# API_URL = "http://127.0.0.1:5000/predict"

# For backend Flask operation
@app.route('/predict', methods = ["GET","POST"])


def prediction():
   
    
    data = request.form
        
    #print('data :',data)

    med_ins = MedicalInsurance(data)
    price = med_ins.get_predicted_price()
    print("The Predicted Premium",price)
    return jsonify({"The Predicted Premium Price in $:":price})

# for frontend Streamlit deployment


# Function to set background
def add_bg_from_local(IMAGE_FILE):
    with open(IMAGE_FILE, "rb") as f:
        data = f.read()
    encoded = base64.b64encode(data).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{encoded}");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

#Add background
# --- Function to set background ---
def add_bg_from_local(IMAGE_FILE):
    with open(IMAGE_FILE, "rb") as f:
        data = f.read()
    encoded = base64.b64encode(data).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{encoded}");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# --- Add background image ---
add_bg_from_local("image.jpg")

# --- Page config ---
st.set_page_config(page_title="Medical Insurance Premium Predictor", layout="wide")

# --- Title ---
st.markdown("<h1 style='text-align: center;'>🏥 Health Insurance Premium Predictor</h1>", unsafe_allow_html=True)

st.markdown(
    """
    <style>
    label[data-testid="stWidgetLabel"] > div[data-testid="stMarkdownContainer"] p {
        font-size:18px;
        font-weight:600;
        color: #000000;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- Input fields in center ---
col1, col2, col3 = st.columns([1, 1, 1])  # keep middle column wider
with col2:
    st.header("Enter Your Details")


    age = st.number_input("Age", min_value=1, max_value=120, step=1)
    gender = st.selectbox("Gender", ["male", "female"])
    bmi = st.number_input("BMI", min_value=10.0, max_value=60.0, step=0.1)
    children = st.number_input("Number of Children", min_value=0, max_value=10, step=1)
    discount_eligibility = st.selectbox("Discount Eligibility", ["yes", "no"])
    region = st.selectbox("Region", ["northeast", "northwest", "southeast", "southwest"])

# --- API URL ---
API_URL = "http://127.0.0.1:5000/predict"

    
# --- Centered Predict Button ---
col1, col2, col3 = st.columns([1, 0.5, 1])
with col2:
    predict = st.button("Predict Premium", use_container_width=True)

if predict:
    input_data = {
        "age": age,
        "gender": gender,
        "bmi": bmi,
        "children": children,
        "discount_eligibility": discount_eligibility,
        "region": region
    }

    try:
        response = requests.post(API_URL, data=input_data)
        if response.status_code == 200:
            result = response.json()
            premium = result.get("The Predicted Premium Price in $:", None) or result.get("predicted_premium_in_usd")

            # Convert INR → USD (1 USD ≈ 84 INR, adjust if needed)
            #premium_usd = float(premium) / 84  

            # --- Styled Premium Result ---
            col1, col2, col3 = st.columns([1, 1, 1])
            with col2:
                st.markdown(
                    f"""
                    <div style="
                        background-color: #f9f9f9;
                        #padding: 1px;
                        border-radius: 6px;
                        text-align: center;
                        box-shadow: 0px 2px 6px rgba(0,0,0,0.15);
                    ">
                        <p style="font-size:24px; font-weight:bold; color:#000;">
                            💰 Predicted Premium: $ {premium:,.2f}
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        else:
            st.error("Error in prediction. Please check API.")
    except Exception as e:
        st.error(f"Could not connect to API: {e}")

if __name__ == "__main__":
    app.run()