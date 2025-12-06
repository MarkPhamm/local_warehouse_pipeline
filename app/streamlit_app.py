import streamlit as st
from response_predictor import ResponsePredictor  # Simple import now

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Consumer Complaint Predictor", 
    page_icon="⚖️", 
    layout="wide"
)

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
st.markdown("<p style='text-align: center; color: #bdc3c7;'>Predicting corporate responses using CatBoost</p>", unsafe_allow_html=True)
st.write("---")

# --- INPUT OPTIONS ---
# (Ideally, replace these with dynamic loads from your database)
product_opts = ['Checking or savings account', 'Credit card', 'Mortgage', 'Student loan', 'Vehicle loan', 'Debt collection'] 
sub_product_opts = ['General-purpose credit card', 'Conventional home mortgage', 'Other', 'I do not know']
issue_opts = ['Managing an account', 'Incorrect information on report', 'Trouble during payment process', 'Struggling to pay mortgage']
company_opts = ['Bank of America', 'Wells Fargo', 'JPMorgan Chase', 'Equifax', 'Experian', 'Citibank']
state_opts = ['CA', 'NY', 'TX', 'FL', 'IL', 'PA', 'OH', 'GA', 'NC', 'MI']
submitted_via_opts = ['Web', 'Referral', 'Phone', 'Postal mail', 'Fax', 'Email']
consent_opts = ['Consent provided', 'Consent not provided', 'Consent withdrawn', 'N/A', 'Other']

# --- FORM ---
with st.form(key='prediction_form'):
    col1, col2 = st.columns(2)

    with col1:
        with st.container(border=True):
            st.subheader("📝 Complaint Details")
            product = st.selectbox('Product Category', options=product_opts)
            sub_product = st.selectbox('Sub-Product', options=sub_product_opts)
            issue = st.selectbox('Specific Issue', options=issue_opts)
            submitted_via = st.selectbox('Submission Channel', options=submitted_via_opts)

    with col2:
        with st.container(border=True):
            st.subheader("🏢 Company & Context")
            company = st.selectbox('Company Name', options=company_opts)
            state = st.selectbox('State', options=state_opts)
            consent = st.selectbox('Consumer Consent', options=consent_opts)

    st.markdown("<br>", unsafe_allow_html=True)
    submit_button = st.form_submit_button(label='PREDICT RESPONSE')

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
        "consumer_consent_provided": consent
    }

    with st.spinner("Analyzing complaint patterns..."):
        try:
            result_label = predictor.predict(input_data)
            
            st.markdown("---")
            st.markdown(f"""
            <div style="text-align: center; padding: 20px; background-color: rgba(255,255,255,0.05); border-radius: 15px; border: 1px solid rgba(255,255,255,0.2);">
                <h3 style="margin:0; color: #ecf0f1; font-weight: 400;">Predicted Company Response</h3>
                <h1 style="margin:15px; color: #2ecc71; font-size: 2.5em; text-shadow: 0 0 15px rgba(46, 204, 113, 0.4);">{result_label}</h1>
                <p style="color: #bdc3c7;">Based on historical data for <b>{company}</b></p>
            </div>
            """, unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"Prediction Error: {e}")