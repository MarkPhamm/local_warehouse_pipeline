"""
Shared Utilities - Database connection, data loading, and common UI elements.
This module provides core functionality used across all dashboard pages.
"""

import duckdb
import pandas as pd
import streamlit as st

# Database configuration
DB_PATH = "database/cfpb_complaints.duckdb"

# ==========================================
# SQL QUERIES
# ==========================================

# Filter for companies with significant complaint volume (10,000+)
# This ensures we focus analysis on major institutions
TOP_COMPANIES_FILTER = """
    from marts.fct_complaints
    where company in (
        select company
        from marts.fct_complaints
        group by company
        having count(*) >= 10000
        order by count(*) desc
    )
"""

# Page-specific queries - each selects only needed columns
EXECUTIVE_SUMMARY = f"""
    select
        date_received,
        company,
        product,
        issue,
        company_response,
        is_timely_response
    {TOP_COMPANIES_FILTER}
"""

COMPANY_PERFORMANCE = f"""
    select
        date_received,
        company,
        product,
        is_timely_response
    {TOP_COMPANIES_FILTER}
"""

PRODUCT_ISSUES = f"""
    select
        date_received,
        company,
        product,
        sub_product,
        issue
    {TOP_COMPANIES_FILTER}
"""

GEOGRAPHIC_TRENDS = f"""
    select
        date_received,
        company,
        product,
        state,
        submitted_via
    {TOP_COMPANIES_FILTER}
"""

# ==========================================
# DATA LOADING
# ==========================================


@st.cache_data(ttl=3600)
def load_duckdb_data(query_string):
    """
    Loads data from DuckDB database with caching.
    Cache expires after 1 hour to balance performance and freshness.

    Args:
        query_string (str): SQL query to execute

    Returns:
        DataFrame: Query results with preprocessing applied
    """
    try:
        con = duckdb.connect(DB_PATH, read_only=True)
        df = con.execute(query_string).df()
        con.close()

        # Convert boolean is_timely_response to numeric (1/0)
        # This simplifies aggregation operations
        if "is_timely_response" in df.columns:
            df["is_timely_response"] = df["is_timely_response"].apply(lambda x: 1 if x else 0)
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()


# ==========================================
# STYLING
# ==========================================


def apply_styling():
    """
    Applies global CSS styling to the Streamlit app.
    This includes dark theme, card styles, animations, and component overrides.
    Should be called at the top of every page.
    """
    st.markdown(
        """
        <style>
            /* ========================================
               1. MAIN LAYOUT & BACKGROUND
               ======================================== */

            /* Dark gradient background */
            [data-testid="stAppViewContainer"] {
                background: linear-gradient(to bottom, #020617 0%, #0F172A 50%, #1E293B 100%);
                background-attachment: fixed;
                color: #F1F5F9;
                font-family: 'Inter', sans-serif;
            }

            /* Remove default header background */
            [data-testid="stHeader"] {
                background-color: rgba(0,0,0,0);
            }

            /* Import modern font */
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

            html, body, [class*="css"] {
                font-family: 'Roboto', sans-serif;
                color: #1F2937;
            }

            /* ========================================
               2. SIDEBAR STYLING
               ======================================== */

            /* Navy gradient sidebar */
            section[data-testid="stSidebar"] {
                background: linear-gradient(180deg, #00395D 0%, #002B4A 50%, #001F35 100%);
                box-shadow: 4px 0 20px rgba(0, 57, 93, 0.15);
            }

            /* White text in sidebar */
            section[data-testid="stSidebar"] h1,
            section[data-testid="stSidebar"] h2,
            section[data-testid="stSidebar"] h3,
            section[data-testid="stSidebar"] span,
            section[data-testid="stSidebar"] label {
                color: #FFFFFF !important;
                text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
            }

            /* Frosted glass effect on sidebar widgets */
            section[data-testid="stSidebar"] .stMultiSelect,
            section[data-testid="stSidebar"] .stDateInput {
                background-color: rgba(255, 255, 255, 0.1);
                border-radius: 8px;
                padding: 5px;
                backdrop-filter: blur(10px);
            }

            /* ========================================
               3. HEADERS & TYPOGRAPHY
               ======================================== */

            h1, h2, h3 {
                color: #00395D;
                font-weight: 700;
                letter-spacing: -0.5px;
            }

            /* H1 with bottom accent line */
            h1 {
                background: linear-gradient(90deg, #00AEEF 0%, #0090C8 100%);
                background-size: 100% 4px;
                background-repeat: no-repeat;
                background-position: left bottom;
                padding-bottom: 12px;
                display: inline-block;
                text-shadow: 0 2px 4px rgba(0, 57, 93, 0.1);
            }

            /* H2 with left border accent */
            h2 {
                border-left: 4px solid #00AEEF;
                padding-left: 12px;
                margin-left: -12px;
            }

            /* ========================================
               4. CARD COMPONENTS
               ======================================== */

            /* 3D elevated cards with layered shadows */
            div.css-card {
                background: linear-gradient(145deg, #FFFFFF 0%, #F8FAFB 100%);
                border-radius: 16px;
                padding: 24px 20px;
                box-shadow:
                    0 2px 4px rgba(0, 57, 93, 0.05),
                    0 8px 16px rgba(0, 57, 93, 0.08),
                    0 16px 32px rgba(0, 57, 93, 0.06);
                border: 1px solid rgba(0, 174, 239, 0.1);
                border-left: 5px solid #00AEEF;
                position: relative;
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                overflow: hidden;
            }

            /* Top accent line (hidden by default) */
            div.css-card::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                height: 3px;
                background: linear-gradient(90deg, #00AEEF 0%, #00C9FF 100%);
                opacity: 0;
                transition: opacity 0.3s ease;
            }

            /* Card hover effects */
            div.css-card:hover {
                transform: translateY(-6px) scale(1.02);
                box-shadow:
                    0 4px 8px rgba(0, 57, 93, 0.08),
                    0 12px 24px rgba(0, 57, 93, 0.12),
                    0 24px 48px rgba(0, 57, 93, 0.1),
                    0 0 0 1px rgba(0, 174, 239, 0.3);
                border-left-width: 6px;
            }

            div.css-card:hover::before {
                opacity: 1;
            }

            /* ========================================
               5. KPI CARDS
               ======================================== */

            .kpi-card {
                background: linear-gradient(145deg, #0F172A, #0B1120);
                border-left: 4px solid #00AEEF;
                border-radius: 12px;
                padding: 20px 24px;
                box-shadow: 0 4px 15px rgba(0,0,0,0.3);
                margin-bottom: 20px;
                transition: transform 0.2s;
            }

            .kpi-card:hover {
                transform: translateY(-5px);
                box-shadow: 0 8px 25px rgba(0, 174, 239, 0.15);
            }

            .kpi-label {
                font-size: 0.85rem;
                color: #94A3B8;
                text-transform: uppercase;
                letter-spacing: 1px;
                font-weight: 600;
                margin-bottom: 5px;
            }

            .kpi-value {
                font-size: 2rem;
                font-weight: 700;
                color: #F8FAFC;
            }

            .kpi-icon {
                float: right;
                font-size: 1.5rem;
                color: #00AEEF;
                opacity: 0.8;
            }

            /* ========================================
               6. METRIC COMPONENTS
               ======================================== */

            .metric-label {
                font-size: 0.85rem;
                color: #6B7280;
                text-transform: uppercase;
                letter-spacing: 1.5px;
                font-weight: 600;
                margin-bottom: 8px;
                display: block;
            }

            .metric-value {
                font-size: 1.8rem;
                font-weight: 800;
                background: linear-gradient(135deg, #00395D 0%, #005A8C 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                white-space: normal;
                overflow: hidden;
                display: -webkit-box;
                -webkit-line-clamp: 2;
                -webkit-box-orient: vertical;
                line-height: 1.25;
                max-width: 100%;
            }

            /* Icon decoration for cards */
            .metric-icon {
                position: absolute;
                top: 20px;
                right: 20px;
                width: 48px;
                height: 48px;
                background: linear-gradient(135deg, rgba(0, 174, 239, 0.1) 0%, rgba(0, 174, 239, 0.05) 100%);
                border-radius: 12px;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 24px;
                opacity: 0.6;
                transition: all 0.3s ease;
            }

            div.css-card:hover .metric-icon {
                opacity: 1;
                transform: rotate(10deg) scale(1.1);
                background: linear-gradient(135deg, rgba(0, 174, 239, 0.2) 0%, rgba(0, 174, 239, 0.1) 100%);
            }

            /* ========================================
               7. ANIMATIONS
               ======================================== */

            @keyframes fadeInUp {
                from {
                    opacity: 0;
                    transform: translateY(20px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }

            .css-card {
                animation: fadeInUp 0.6s ease-out;
            }

            /* Stagger animation for multiple cards */
            .css-card:nth-child(1) { animation-delay: 0.1s; }
            .css-card:nth-child(2) { animation-delay: 0.2s; }
            .css-card:nth-child(3) { animation-delay: 0.3s; }
            .css-card:nth-child(4) { animation-delay: 0.4s; }

            /* ========================================
               8. FORM CONTROLS
               ======================================== */

            /* Multiselect tags */
            span[data-baseweb="tag"] {
                background-color: #00AEEF !important;
                border: 1px solid #00AEEF !important;
            }
            span[data-baseweb="tag"] span {
                color: #000000 !important;
            }

            /* Select/multiselect dropdowns */
            div[data-baseweb="select"] > div {
                background-color: rgba(255,255,255,0.05) !important;
                border: 1px solid rgba(255,255,255,0.12) !important;
                border-radius: 12px !important;
            }

            /* Radio buttons */
            div[data-testid="stRadio"] > div {
                background-color: rgba(0, 174, 239, 0.15) !important;
                border: 2px solid #00AEEF !important;
                border-radius: 12px !important;
                padding: 12px !important;
            }

            /* Selectbox */
            div[data-testid="stSelectbox"] > div {
                background-color: rgba(0, 174, 239, 0.15) !important;
                border: 2px solid #00AEEF !important;
                border-radius: 12px !important;
            }

            div[data-testid="stSelectbox"] span {
                color: #00AEEF !important;
            }

            /* ========================================
               9. CHART CONTAINERS
               ======================================== */

            /* Plotly chart wrapper */
            div[data-testid="stPlotlyChart"] > div {
                border-radius: 18px;
                background: rgba(255,255,255,0.04);
                border: 1px solid rgba(255,255,255,0.10);
                box-shadow: 0 18px 55px rgba(0,0,0,0.45);
                padding: 14px;
            }

            /* ========================================
               10. ALERT BOXES
               ======================================== */

            div[data-testid="stAlert"] p {
                color: #E0E7FF !important;
                font-weight: 500;
            }
        </style>
    """,
        unsafe_allow_html=True,
    )


# ==========================================
# SHARED COMPONENTS
# ==========================================


def render_sidebar(df):
    """
    Renders the sidebar filter panel and returns filtered DataFrame.
    This is used on all dashboard pages to provide consistent filtering.

    Args:
        df (DataFrame): Raw data to filter

    Returns:
        DataFrame: Filtered data based on user selections
    """
    # Ensure styling is applied
    apply_styling()

    # Additional styling for select/multiselect in sidebar
    st.markdown(
        """
        <style>
            div[data-baseweb="select"] > div {
                background-color: rgba(255,255,255,0.05) !important;
                border: 1px solid rgba(255,255,255,0.12) !important;
                border-radius: 12px !important;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.sidebar.markdown("<br>", unsafe_allow_html=True)
    st.sidebar.header("🔍 Filter Data")

    if df.empty:
        return df

    # ==========================================
    # 1. DATE RANGE FILTER
    # ==========================================
    min_date = df["date_received"].min()
    max_date = df["date_received"].max()

    st.sidebar.subheader("📅 Date Range")

    col1, col2 = st.sidebar.columns(2)

    with col1:
        start_date = st.date_input(
            "Start Date", value=min_date, min_value=min_date, max_value=max_date
        )

    with col2:
        end_date = st.date_input("End Date", value=max_date, min_value=min_date, max_value=max_date)

    # ==========================================
    # 2. COMPANY FILTER
    # ==========================================
    st.sidebar.subheader("🏢 Select Company")

    # Show top 50 companies by complaint volume
    top_companies = df["company"].value_counts().nlargest(50).index.tolist()
    selected_companies = st.sidebar.multiselect(
        "Select Company", options=top_companies, label_visibility="collapsed"
    )

    # ==========================================
    # 3. PRODUCT FILTER
    # ==========================================
    st.sidebar.subheader("📦 Select Product")
    all_products = df["product"].unique().tolist()
    selected_products = st.sidebar.multiselect(
        "Select Product", options=all_products, label_visibility="collapsed"
    )

    # ==========================================
    # APPLY FILTERS
    # ==========================================
    # Use boolean indexing with conditional logic
    mask = (
        (df["date_received"].dt.date >= start_date)
        & (df["date_received"].dt.date <= end_date)
        & (df["company"].isin(selected_companies) if selected_companies else True)
        & (df["product"].isin(selected_products) if selected_products else True)
    )

    return df[mask]


def header_for_pages(header, text):
    """
    Renders a consistent page header with title and description.

    Args:
        header (str): Page title
        text (str): Page description/subtitle
    """
    st.markdown(
        f"""
    <div style="margin-bottom: 30px;">
        <h1 style="color: white; font-size: 2.5rem; margin-bottom: 0;">{header}</h1>
        <p style="color: #94A3B8; margin-top: 10px; font-size: 1.1rem;">
            {text}
        </p>
    </div>
    """,
        unsafe_allow_html=True,
    )
