"""
Product Issues Page - Root cause analysis across product categories.
Displays hierarchical treemap of complaints by product/sub-product,
and allows drilling down into specific issues for detailed investigation.
"""

import streamlit as st
from chart_factory import ChartFactory
from components import UIComponents
from data_utils import DataTransformations

from utils import PRODUCT_ISSUES, apply_styling, header_for_pages, load_duckdb_data, render_sidebar

# ==========================================
# PAGE CONFIGURATION
# ==========================================
st.set_page_config(page_title="Product Issues", page_icon="📦", layout="wide")

apply_styling()

# ==========================================
# PAGE HEADER
# ==========================================
header_for_pages("Product Friction Points", "Root cause analysis across product architecture")

# Override info box text color for better visibility
st.markdown(
    """
    <style>
    div[data-testid="stAlert"] p {
        color: #0B1220 !important;
        font-weight: 500;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ==========================================
# DATA LOADING
# ==========================================
df_raw = load_duckdb_data(PRODUCT_ISSUES)

# Apply sidebar filters
df = render_sidebar(df_raw)

if df.empty:
    st.stop()

# ==========================================
# TREEMAP SECTION
# ==========================================
st.subheader("Complaint Architecture")

# Layout: treemap (90%) + filter controls (10%)
col_treemap, col_filter = st.columns([9, 1])

with col_filter:
    # Filter selector for treemap granularity
    treemap_filter = UIComponents.info_filter(
        "Filter complaints", options=["All Products", "Top 5 Products", "Top 3 Products"]
    )

with col_treemap:
    # Prepare treemap data based on selected filter
    treemap_data = DataTransformations.prepare_treemap_data(
        df, filter_option=treemap_filter, product_col="product", sub_product_col="sub_product"
    )

    # Create treemap with factory
    # Shows hierarchy: Product → Sub-Product
    fig_tree = ChartFactory.create_treemap(
        treemap_data, path=["product", "sub_product"], values="count", color="count"
    )

    st.plotly_chart(fig_tree, use_container_width=True)

# ==========================================
# DRILL-DOWN SECTION
# ==========================================
st.markdown("---")
st.subheader("Root Cause Investigation")

# Layout: product selector (33%) + bar chart (67%)
col_select, col_graph = st.columns([1, 2])

with col_select:
    # Product selector for detailed issue analysis
    selected_product_drill = UIComponents.select_filter(
        "Select a product to view specific issues.",
        options=sorted(df["product"].dropna().unique().tolist()),
    )

# Filter to selected product
subset = df[df["product"] == selected_product_drill]

with col_graph:
    if subset.empty:
        st.info("No data for this selection.")
        st.stop()

    # Get top 10 issues for selected product
    top_issues = DataTransformations.value_counts_df(
        subset, column="issue", top_n=10, column_names=["Issue", "Count"]
    )

    # Create horizontal bar chart
    # Bars are sorted by count (ascending) for better readability
    fig_bar = ChartFactory.create_horizontal_bar(top_issues, x="Count", y="Issue", text="Count")

    st.plotly_chart(fig_bar, use_container_width=True)
