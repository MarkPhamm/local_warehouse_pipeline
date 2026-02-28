"""
Company Performance Page - Efficiency analysis across institutions.
Visualizes company performance in a volume vs. timeliness matrix,
allowing identification of high-volume efficient companies and underperformers.
"""

import streamlit as st
from chart_factory import ChartFactory
from data_utils import DataTransformations

from utils import (
    COMPANY_PERFORMANCE,
    apply_styling,
    header_for_pages,
    load_duckdb_data,
    render_sidebar,
)

# ==========================================
# PAGE CONFIGURATION
# ==========================================
st.set_page_config(page_title="Company Performance", page_icon="🏢", layout="wide")

apply_styling()

# ==========================================
# PAGE HEADER
# ==========================================
header_for_pages("Company Performance", "Efficiency Analysis: Volume vs. Timeliness Matrix")

# ==========================================
# DATA LOADING
# ==========================================
df_raw = load_duckdb_data(COMPANY_PERFORMANCE)

# Apply sidebar filters
df = render_sidebar(df_raw)

if df.empty:
    st.warning("No data available for the selected filters.")
    st.stop()

# ==========================================
# DATA AGGREGATION
# ==========================================
# Calculate company statistics using utility function
company_stats = DataTransformations.calculate_company_stats(df)

# ==========================================
# LAYOUT: SCATTER PLOT + LEADERBOARD
# ==========================================
col_chart, col_table = st.columns([2.5, 1])

# ==========================================
# PERFORMANCE MATRIX SCATTER PLOT
# ==========================================
with col_chart:
    st.subheader("Performance Matrix")

    # Calculate average values for reference lines
    avg_vol = company_stats["Total_Complaints"].mean()
    avg_time = company_stats["Timely_Rate"].mean()

    # Create scatter plot with factory
    fig_scatter = ChartFactory.create_scatter_chart(
        company_stats,
        x="Total_Complaints",
        y="Timely_Rate",
        hover_name="company",
        size="Total_Complaints",
        color="Timely_Rate",
        labels={"Total_Complaints": "Volume", "Timely_Rate": "Timeliness (%)"},
    )

    # Add reference lines for benchmarking
    # These create quadrants: low/high volume × low/high timeliness
    fig_scatter = ChartFactory.add_reference_lines(
        fig_scatter, avg_x=avg_vol, avg_y=avg_time, x_label="Avg Volume", y_label="Avg Timeliness"
    )

    st.plotly_chart(fig_scatter, use_container_width=True)

# ==========================================
# LEADERBOARD TABLE
# ==========================================
with col_table:
    st.subheader("Leaderboard")

    # Get top 10 companies by complaint volume
    top_performers = company_stats.sort_values(by="Total_Complaints", ascending=False).head(10)

    # Display styled dataframe with gradient backgrounds
    # Green gradient for timeliness (higher is better)
    # Blue gradient for volume (shows relative scale)
    st.dataframe(
        top_performers.reset_index(drop=True)
        .style.background_gradient(
            subset=["Timely_Rate"],
            cmap="RdYlGn",  # Red-Yellow-Green scale
            vmin=0,
            vmax=100,
        )
        .background_gradient(subset=["Total_Complaints"], cmap="Blues")
        .format({"Timely_Rate": "{:.1f}%", "Total_Complaints": "{:,}"}),
        use_container_width=True,
        height=500,
    )
