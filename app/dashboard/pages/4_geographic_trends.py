"""
Geographic Trends Page - Regional intensity analysis.
Displays complaint distribution across US states via heatmap,
and analyzes submission channel preferences.
"""

import streamlit as st
from chart_factory import ChartFactory
from data_utils import DataTransformations

from utils import (
    GEOGRAPHIC_TRENDS,
    apply_styling,
    header_for_pages,
    load_duckdb_data,
    render_sidebar,
)

# ==========================================
# PAGE CONFIGURATION
# ==========================================
st.set_page_config(page_title="Geographic Trends", page_icon="🗺️", layout="wide")

apply_styling()

# ==========================================
# DATA LOADING
# ==========================================
df_raw = load_duckdb_data(GEOGRAPHIC_TRENDS)

# ==========================================
# PAGE HEADER
# ==========================================
header_for_pages("Geographic Distribution", "Regional intensity and submission channel preferences")

# Apply sidebar filters
df = render_sidebar(df_raw)

if df.empty:
    st.stop()

# ==========================================
# REGIONAL HEATMAP (USA STATES)
# ==========================================
st.subheader("Regional Heatmap")

# Aggregate complaints by state
state_counts = DataTransformations.value_counts_df(
    df, column="state", column_names=["State", "Complaints"]
)

# Create choropleth map using factory
# Color intensity represents complaint volume
fig_map = ChartFactory.create_choropleth(
    state_counts, locations="State", color="Complaints", scope="usa"
)

st.plotly_chart(fig_map, use_container_width=True)

# ==========================================
# SUBMISSION CHANNELS SECTION
# ==========================================
st.markdown("---")
st.subheader("Submission Channels")

# Get all available submission channels
available_channels = sorted(df["submitted_via"].dropna().unique().tolist())

# Multi-select filter for channels
# Defaults to showing all channels
selected_channels = st.multiselect(
    "Filter Channels:",
    options=available_channels,
    default=available_channels,
)

# Filter data based on channel selection
df_channel_filtered = df[df["submitted_via"].isin(selected_channels)]

if df_channel_filtered.empty:
    st.stop()

# Aggregate by submission channel
channel_counts = DataTransformations.value_counts_df(
    df_channel_filtered, column="submitted_via", column_names=["Channel", "Count"]
)

# Create horizontal bar chart
# Shows relative popularity of each submission method
fig_ch = ChartFactory.create_horizontal_bar(channel_counts, x="Count", y="Channel", text="Count")

st.plotly_chart(fig_ch, use_container_width=True)
