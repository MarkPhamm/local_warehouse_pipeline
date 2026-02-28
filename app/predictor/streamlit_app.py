import json
from pathlib import Path

import streamlit as st

from app.predictor.response_predictor import ResponsePredictor

# --- PAGE CONFIG ---
st.set_page_config(page_title="Company Responses Predictor", page_icon="⚖️", layout="wide")


# --- STYLING (Dark Mode) ---
def apply_custom_styling():
    css = """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@400;600&display=swap');

        html, body, [class*="st-"] {
            font-family: 'Quicksand', sans-serif;
            color: #f0f0f0;
        }

        /* Gradient Background */
        .stApp {
            background-image: linear-gradient(to bottom, #2c3e50, #000000);
            background-attachment: fixed;
        }

        /* Glassmorphism Cards */
        [data-testid="stVerticalBlockBorderWrapper"] > div {
            background-color: rgba(255, 255, 255, 0.05);
            border-radius: 10px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            padding: 15px;
        }

        /* Inputs */
        .stSelectbox, .stTextInput {
            color: #ffffff;
        }

        /* Button */
        .stButton > button {
            background: linear-gradient(90deg, #ff8a00, #e52e71);
            color: white;
            font-weight: bold;
            border: none;
            border-radius: 25px;
            padding: 12px 25px;
            width: 100%;
            margin-top: 10px;
        }
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(229, 46, 113, 0.6);
        }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


apply_custom_styling()


# --- LOAD MODEL ---
@st.cache_resource
def get_predictor():
    return ResponsePredictor()


try:
    predictor = get_predictor()
except Exception as e:
    st.error(f"Error loading model artifacts: {e}")
    st.stop()

# --- UI LAYOUT ---
st.title("⚖️ Company Response Predictor")
st.markdown(
    "<p style='text-align: center; color: #bdc3c7;'>Predicting corporate responses using XGBoost</p>",
    unsafe_allow_html=True,
)
st.write("---")


# --- INPUT + LOAD OPTIONS ---
@st.cache_data
def load_options():
    # Project root: app/predictor/ -> parent.parent.parent
    options_path = Path(__file__).parent.parent.parent / "src" / "models" / "options.json"

    with open(options_path) as f:
        options = json.load(f)
    return options


try:
    options = load_options()
except FileNotFoundError:
    st.error("Could not find 'options.json'. Please run 'extract_options.py' first.")
    st.stop()

# --- INPUT FORM ---
st.markdown("## Submit a Complaint Detail")

with st.form(key="prediction_form"):
    col1, col2 = st.columns(2)

    with col1:
        with st.container(border=True):
            st.subheader("📝 Complaint Details")
            product = st.selectbox("Product Category", options=options.get("product", []))
            sub_product = st.selectbox("Sub-Product", options=options.get("sub_product", []))
            issue = st.selectbox("Specific Issue", options=options.get("issue", []))
            submitted_via = st.selectbox(
                "Submission Channel", options=options.get("submitted_via", [])
            )

    with col2:
        with st.container(border=True):
            st.subheader("🏢 Company & Context")
            company = st.selectbox("Company Name", options=options.get("company", []))
            state = st.selectbox("State", options=options.get("state", []))
            consent = st.selectbox(
                "Consumer Consent", options=options.get("consumer_consent_provided", [])
            )

    st.markdown("<br>", unsafe_allow_html=True)
    submit_button = st.form_submit_button(label="PREDICT RESPONSE")

# --- PREDICTION LOGIC ---
if submit_button:
    # Keys must match the columns expected by your preprocessor in encoding.ipynb
    input_data = {
        "product": product,
        "sub_product": sub_product,
        "issue": issue,
        "company": company,
        "state": state,
        "submitted_via": submitted_via,
        "consumer_consent_provided": consent,
    }

    with st.spinner("Analyzing complaint patterns..."):
        try:
            result_label = predictor.predict(input_data)

            st.markdown("---")
            st.markdown(
                f"""
            <div style="text-align: center; padding: 20px; background-color: rgba(255,255,255,0.05); border-radius: 15px; border: 1px solid rgba(255,255,255,0.2);">
                <h3 style="margin:0; color: #ecf0f1; font-weight: 400;">Predicted Company Response</h3>
                <h1 style="margin:15px; color: #2ecc71; font-size: 2.5em; text-shadow: 0 0 15px rgba(46, 204, 113, 0.4);">{result_label}</h1>
                <p style="color: #bdc3c7;">Based on historical data for <b>{company}</b></p>
            </div>
            """,
                unsafe_allow_html=True,
            )

        except Exception as e:
            st.error(f"Prediction Error: {e}")
