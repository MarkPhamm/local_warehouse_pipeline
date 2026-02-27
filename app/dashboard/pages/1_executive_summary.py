"""
Executive Summary Page - High-level KPIs and trends.
Displays total complaint volume, timely response rate, top products/issues,
and visualizes trends over time with resolution type distribution.
"""

import streamlit as st
from chart_factory import ChartFactory
from components import UIComponents
from config import COLORS
from data_utils import DataTransformations

from utils import (
    EXECUTIVE_SUMMARY,
    apply_styling,
    header_for_pages,
    load_duckdb_data,
    render_sidebar,
)

# ==========================================
# PAGE CONFIGURATION
# ==========================================
st.set_page_config(page_title="Executive Summary", page_icon="📊", layout="wide")

apply_styling()

# ==========================================
# DATA LOADING
# ==========================================
df_raw = load_duckdb_data(EXECUTIVE_SUMMARY)

if df_raw.empty:
    st.error("No data could be loaded. Please check the database connection.")
    st.stop()

# Apply sidebar filters
df = render_sidebar(df_raw)

# ==========================================
# PAGE HEADER
# ==========================================
header_for_pages(
    "Executive Summary", "High-level overview of complaint volume and resolution health metrics."
)

# ==========================================
# KPI CALCULATIONS
# ==========================================
total_complaints = len(df)

# Calculate timely response rate as percentage
timely_rate = (df["is_timely_response"].mean() * 100) if total_complaints > 0 else 0

# Find most common product and issue
top_product = df["product"].mode()[0] if not df.empty else "N/A"
top_issue = df["issue"].mode()[0] if not df.empty else "N/A"

# ==========================================
# KPI CARDS SECTION
# ==========================================
# Create 4-column layout for KPI cards
c1, c2, c3, c4 = st.columns(4)

with c1:
    UIComponents.kpi_card("Total Volume", f"{total_complaints:,}", "📈")

with c2:
    # Color-code timely response rate: green if >90%, yellow otherwise
    color = COLORS["success"] if timely_rate > 90 else COLORS["warning"]
    val_html = f"<span style='color:{color}'>{timely_rate:.1f}%</span>"
    UIComponents.kpi_card("Timely Response", val_html, "⏱️")

with c3:
    # Use adaptive text sizing for long product names
    UIComponents.kpi_card(
        "Top Product",
        UIComponents.adaptive_text(top_product),
        "🏆",
        tooltip=top_product,  # Full text on hover
    )

with c4:
    # Use adaptive text sizing for long issue descriptions
    UIComponents.kpi_card(
        "Top Issue", UIComponents.adaptive_text(top_issue), "🎯", tooltip=top_issue
    )

st.markdown("---")

# ==========================================
# CHARTS SECTION
# ==========================================
col_left, col_right = st.columns((2, 1), gap="large")

# ==========================================
# CHART 1: VOLUME TREND OVER TIME (LEFT)
# ==========================================
with col_left:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown("### Complaint Volume Over Time")

    # Resample data to monthly frequency
    df_trend = DataTransformations.resample_timeseries(df, date_column="date_received", freq="M")

    # Create area chart with factory
    fig_trend = ChartFactory.create_area_chart(df_trend, x="date_received", y="count")

    st.plotly_chart(fig_trend, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# CHART 2: RESOLUTION TYPES (RIGHT)
# ==========================================
with col_right:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown("### Resolution Types")

    # Get value counts for company responses
    resp_counts = DataTransformations.value_counts_df(
        df, column="company_response", column_names=["Response", "Count"]
    )

    # Create donut chart with center text showing total
    fig_donut = ChartFactory.create_donut_chart(
        resp_counts, values="Count", names="Response", center_text=f"{len(df):,}"
    )

    st.plotly_chart(fig_donut, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
