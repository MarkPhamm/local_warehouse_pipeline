"""
Home Page - Landing page with project overview and navigation.
Displays hero section, core analytical question, and navigation cards
for each dashboard module.
"""

import streamlit as st

from utils import apply_styling

# ==========================================
# PAGE CONFIGURATION
# ==========================================
st.set_page_config(page_title="CFPB Analysis", page_icon="🏦", layout="wide")

apply_styling()

# ==========================================
# CUSTOM CSS FOR HOME PAGE
# ==========================================
# Additional styling specific to landing page elements
st.markdown(
    """
<style>
    /* --- 1. GENERAL APP SETUP --- */
    /* Remove top padding to flush the hero section */
    .block-container {
        padding-top: 1rem;
        padding-bottom: 5rem;
    }

    /* Background Color Override */
    [data-testid="stAppViewContainer"] {
        background-color: #020617; /* Very Dark Slate */
    }

    /* --- 2. ANIMATIONS --- */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    @keyframes glowPulse {
        0% { box-shadow: 0 0 5px rgba(0, 174, 239, 0.2); }
        50% { box-shadow: 0 0 15px rgba(0, 174, 239, 0.5); }
        100% { box-shadow: 0 0 5px rgba(0, 174, 239, 0.2); }
    }

    /* --- 3. HERO SECTION STYLES --- */
    .hero-card {
        background: linear-gradient(135deg, #001E32 0%, #00395D 100%);
        border: 1px solid rgba(255,255,255,0.05);
        border-radius: 24px;
        padding: 60px 40px;
        position: relative;
        overflow: hidden;
        box-shadow: 0 20px 50px rgba(0,0,0,0.3);
        margin-bottom: 30px;
        animation: fadeIn 0.8s ease-out;
    }

    /* Subtle geometric overlay for hero */
    .hero-card::before {
        content: "";
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        background-image: radial-gradient(circle at 10% 20%, rgba(0, 174, 239, 0.08) 0%, transparent 20%),
                          radial-gradient(circle at 90% 80%, rgba(0, 174, 239, 0.08) 0%, transparent 20%);
        pointer-events: none;
    }

    /* --- 4. ANALYTICAL QUESTION BOX --- */
    .question-box {
        background: rgba(255, 255, 255, 0.03);
        border-left: 4px solid #00AEEF;
        border-radius: 0 12px 12px 0;
        padding: 30px;
        margin: 20px 0 40px 0;
        backdrop-filter: blur(10px);
        animation: fadeIn 1.0s ease-out;
    }

    /* --- 5. INSIGHT CARDS (Navigation Cards) --- */
    .insight-card {
        background: linear-gradient(145deg, #0F172A, #0B1120);
        border: 1px solid rgba(56, 189, 248, 0.1);
        border-radius: 16px;
        padding: 25px;
        height: 100%;
        transition: all 0.3s ease;
        cursor: default;
        position: relative;
        overflow: hidden;
    }

    /* Hover effects for navigation cards */
    .insight-card:hover {
        transform: translateY(-5px);
        border-color: rgba(56, 189, 248, 0.5);
        box-shadow: 0 10px 30px -10px rgba(0, 174, 239, 0.3);
    }

    /* Card icon styling */
    .card-icon {
        font-size: 1.8rem;
        margin-bottom: 15px;
        display: inline-block;
        background: rgba(0, 174, 239, 0.1);
        padding: 10px;
        border-radius: 10px;
    }

    /* Card title styling */
    .card-title {
        color: #E2E8F0;
        font-size: 1.2rem;
        font-weight: 600;
        margin-bottom: 8px;
    }

    /* Card description styling */
    .card-desc {
        color: #94A3B8;
        font-size: 0.9rem;
        line-height: 1.5;
    }

    /* --- 6. FOOTER/SIDEBAR NOTIFICATION --- */
    .sidebar-hint {
        margin-top: 40px;
        padding: 15px 25px;
        background: rgba(0, 174, 239, 0.1);
        border: 1px solid rgba(0, 174, 239, 0.2);
        border-radius: 50px;
        text-align: center;
        color: #38BDF8;
        font-weight: 500;
        font-size: 0.9rem;
        animation: glowPulse 3s infinite;
        width: fit-content;
        margin-left: auto;
        margin-right: auto;
    }

</style>
""",
    unsafe_allow_html=True,
)

# ==========================================
# HERO SECTION
# ==========================================
st.markdown(
    """
<div class="hero-card">
    <div style="display: flex; justify-content: space-between; align-items: start;">
        <div>
            <div style="
                background: rgba(0, 174, 239, 0.2);
                color: #38BDF8;
                padding: 5px 12px;
                border-radius: 20px;
                font-size: 0.75rem;
                font-weight: 700;
                display: inline-block;
                margin-bottom: 15px;
                text-transform: uppercase;
                letter-spacing: 1px;">
                Live Dashboard
            </div>
            <h1 style="margin: 0; font-size: 3rem; font-weight: 800; background: linear-gradient(90deg, #FFFFFF, #94A3B8); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                CFPB Complaints Analytics
            </h1>
            <p style="color: #CBD5E1; font-size: 1.1rem; margin-top: 15px; max-width: 700px; line-height: 1.6;">
                Financial institutions process millions of transactions daily, but
                <span style="color: #38BDF8; font-weight: 600;">customer friction</span>
                often reveals cracks in the system. This tool leverages Bureau data to deliver actionable intelligence.
            </p>
            <em style="font-size: 0.9rem; opacity: 0.8; color: #94A3B8;">
                    * This dashboard includes companies that received more than 10,000 complaints during the investigation period.
            </em>
        </div>
        <div style="font-size: 5rem; opacity: 0.1;">🏦</div>
    </div>
</div>
""",
    unsafe_allow_html=True,
)

# ==========================================
# CORE ANALYTICAL QUESTION
# ==========================================
st.markdown(
    """
<div class="question-box">
    <div style="color: #00AEEF; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 2px; font-weight: 700; margin-bottom: 8px;">
        Core Analytical Question
    </div>
    <div style="color: #FFFFFF; font-size: 1.6rem; font-weight: 500; line-height: 1.4;">
        "How effectively are financial institutions resolving consumer complaints,
        and where are the emerging friction points across products and regions?"
    </div>
</div>
""",
    unsafe_allow_html=True,
)

# ==========================================
# NAVIGATION CARDS
# ==========================================
# Two-column grid layout for navigation cards
col1, col2 = st.columns(2, gap="large")

with col1:
    # Card 1: Executive Summary
    st.markdown(
        """
    <div class="insight-card">
        <div class="card-icon">📊</div>
        <div class="card-title">Executive Summary</div>
        <div class="card-desc">
            High-level KPIs, volume trends, and year-over-year growth metrics.
            Start here for a macro view of institutional health.
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    st.markdown("<div style='height: 20px'></div>", unsafe_allow_html=True)

    # Card 3: Company Performance
    st.markdown(
        """
    <div class="insight-card">
        <div class="card-icon">🏢</div>
        <div class="card-title">Company Performance</div>
        <div class="card-desc">
            Analyze efficiency matrices, timely response rates, and company-specific
            benchmarking against industry averages.
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

with col2:
    # Card 2: Product Issues
    st.markdown(
        """
    <div class="insight-card">
        <div class="card-icon">⚠️</div>
        <div class="card-title">Product Issues</div>
        <div class="card-desc">
            Deep dive into specific product lines (Mortgages, Credit Cards)
            to identify root causes and emerging sub-issues.
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    st.markdown("<div style='height: 20px'></div>", unsafe_allow_html=True)

    # Card 4: Geographic Trends
    st.markdown(
        """
    <div class="insight-card">
        <div class="card-icon">🌎</div>
        <div class="card-title">Geographic Trends</div>
        <div class="card-desc">
            Interactive heatmaps revealing regional hotspots and localized
            complaint surges across the United States.
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

# ==========================================
# FOOTER / NAVIGATION INSTRUCTION
# ==========================================
st.markdown(
    """
<div class="sidebar-hint">
    👈 &nbsp; Select a module from the sidebar to begin analysis
</div>
""",
    unsafe_allow_html=True,
)

# Hidden anchor points for potential internal navigation
st.markdown('<div id="executive-summary"></div>', unsafe_allow_html=True)
st.markdown('<div id="company-performance"></div>', unsafe_allow_html=True)
st.markdown('<div id="product-issues"></div>', unsafe_allow_html=True)
st.markdown('<div id="geographic-trends"></div>', unsafe_allow_html=True)
