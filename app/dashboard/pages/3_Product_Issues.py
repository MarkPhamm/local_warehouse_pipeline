import plotly.express as px
import streamlit as st

from utils import load_data, render_sidebar

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(page_title="Product Issues", page_icon="📦", layout="wide")

# -----------------------------
# Global Dark UI (CSS)
# -----------------------------
st.markdown(
    """
<style>
    /* Global Background */
    [data-testid="stAppViewContainer"] {
        background-color: #020617; /* Dark Slate */
        color: #E2E8F0;
    }

    /* Multiselect Tags */
    span[data-baseweb="tag"] {
        background-color: #00AEEF !important; /* Barclays Cyan Blue */
        border: 1px solid #00AEEF !important;
    }

    /* Optional: Text inside the tag */
    span[data-baseweb="tag"] span {
        color: #000000 !important; /* Black text usually contrasts best with this blue */
    }
</style>
""",
    unsafe_allow_html=True,
)

# Header
st.markdown(
    """
<div style="margin-bottom: 30px;">
    <h1 style="color: white; font-size: 2.5rem; margin-bottom: 0;">Product Friction Points</h1>
    <p style="color: #94A3B8; margin-top: 10px; font-size: 1.1rem;">
        Root cause analysis across product architecture
    </p>
</div>
""",
    unsafe_allow_html=True,
)


st.markdown(
    """
    <style>
    /* Override text color inside st.info */
    div[data-testid="stAlert"] p {
        color: #0B1220 !important;
        font-weight: 500;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
st.markdown(
    """
<style>
.stApp {
    background: radial-gradient(1200px 600px at 20% 0%, #0B1220 0%, #070B14 45%, #05070E 100%);
    color: #E6EDF7;
}
h1, h2, h3, span, div, label { color: #E6EDF7 !important; }
hr { border-color: rgba(255,255,255,0.10); }

/* Select / multiselect */
div[data-baseweb="select"] > div {
    background-color: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    border-radius: 12px !important;
}

/* Plotly card */
div[data-testid="stPlotlyChart"] > div {
    border-radius: 18px;
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.10);
    box-shadow: 0 18px 55px rgba(0,0,0,0.45);
    padding: 14px;
}
</style>
""",
    unsafe_allow_html=True,
)

# -----------------------------
# Data
# -----------------------------
df_raw = load_data()

df = render_sidebar(df_raw)
if df.empty:
    st.stop()

# -----------------------------
# TREEMAP
# -----------------------------
st.subheader("Complaint Architecture")

# Create layout with treemap on left and filter on right
col_treemap, col_filter = st.columns([9, 1])

with col_filter:
    st.markdown(
        """
    <style>
    div[data-testid="stRadio"] > div {
        background-color: rgba(0, 174, 239, 0.15) !important;
        border: 2px solid #00AEEF !important;
        border-radius: 12px !important;
        padding: 12px !important;
    }

    div[data-testid="stRadio"] label {
        color: #E6EDF7 !important;
        font-weight: 500;
    }

    div[role="radiogroup"] > div[aria-checked="true"] > div:first-child {
        background-color: #00AEEF !important;
        border-color: #00AEEF !important;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )

    st.info("Filter complaints")
    treemap_filter = st.radio(
        "View",
        options=["All Products", "Top 5 Products", "Top 3 Products"],
        label_visibility="collapsed",
    )

with col_treemap:
    # Apply filter logic
    if treemap_filter == "Top 5 Products":
        # Get top 5 products by count
        top_sub_products = df.groupby("product").size().nlargest(5).index
        treemap_data = (
            df[df["product"].isin(top_sub_products)]
            .groupby(["product", "sub_product"])
            .size()
            .reset_index(name="count")
        )
    elif treemap_filter == "Top 3 Products":
        # Get top 3 products by count
        top_sub_products = df.groupby("product").size().nlargest(3).index
        treemap_data = (
            df[df["product"].isin(top_sub_products)]
            .groupby(["product", "sub_product"])
            .size()
            .reset_index(name="count")
        )
    else:  # All Products
        treemap_data = df.groupby(["product", "sub_product"]).size().reset_index(name="count")

    # IMPORTANT: Scale that avoids "pure white" so text never disappears on dark UI
    # (Top end stops at a light-cyan instead of white)
    blue_scale_safe = [
        [0.00, "#071019"],  # near-bg navy
        [0.18, "#0B2A3F"],
        [0.38, "#0B4A6A"],
        [0.58, "#0EA5E9"],
        [0.78, "#38BDF8"],
        [1.00, "#7DD3FC"],  # NOT #E0F2FE to avoid white blocks
    ]

    fig_tree = px.treemap(
        treemap_data,
        path=["product", "sub_product"],
        values="count",
        color="count",
        color_continuous_scale=blue_scale_safe,
    )

    fig_tree.update_layout(
        margin=dict(t=10, l=10, r=10, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, Roboto, Arial", color="#E6EDF7", size=12),
        coloraxis_colorbar=dict(
            title="Volume",
            thickness=14,
            len=0.75,
            bgcolor="rgba(10, 15, 25, 0.75)",
            bordercolor="rgba(255,255,255,0.12)",
            borderwidth=1,
            tickfont=dict(size=10, color="#D7E2F2"),
        ),
    )

    # Make labels readable on any shade:
    # - Use slightly off-white text (not pure white)
    # - Add subtle border lines between tiles
    # - Dark hover box
    fig_tree.update_traces(
        textinfo="label",
        texttemplate="<b>%{label}</b>",
        textfont=dict(family="Inter, Roboto, Arial", size=17, color="rgba(248,250,252,0.95)"),
        marker=dict(line=dict(color="rgba(255,255,255,0.22)", width=1.2)),
        hoverlabel=dict(bgcolor="rgba(12, 18, 30, 0.95)", font=dict(color="#E6EDF7", size=13)),
        hovertemplate="<b>%{label}</b><br>Count: %{value:,}<br>%{percentParent}<extra></extra>",
    )

    st.plotly_chart(fig_tree, use_container_width=True)

# -----------------------------
# DRILL DOWN
# -----------------------------
st.markdown("---")
st.subheader("Root Cause Investigation")

col_select, col_graph = st.columns([1, 2])

with col_select:
    st.info("Select a product to view specific issues.")
    st.markdown(
        """
    <style>
    /* Target only this selectbox */
    div[data-testid="stSelectbox"] > div {
        background-color: rgba(0, 174, 239, 0.15) !important;
        border: 2px solid #00AEEF !important;
        border-radius: 12px !important;
    }

    /* Style the selected text */
    div[data-testid="stSelectbox"] span {
        color: #00AEEF !important;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )

    selected_product_drill = st.selectbox(
        "Product Category", sorted(df["product"].dropna().unique().tolist())
    )

subset = df[df["product"] == selected_product_drill]

with col_graph:
    if subset.empty:
        st.info("No data for this selection.")
        st.stop()

    top_issues = subset["issue"].value_counts().head(10).reset_index()
    top_issues.columns = ["Issue", "Count"]

    # Clean bar: single color (better readability)
    fig_bar = px.bar(
        top_issues,
        x="Count",
        y="Issue",
        orientation="h",
        text="Count",
    )

    fig_bar.update_traces(
        marker=dict(
            color="rgba(56, 189, 248, 0.92)",
            line=dict(color="rgba(255,255,255,0.18)", width=1),
        ),
        texttemplate="%{x:,}",
        textposition="outside",
        textfont=dict(size=12, family="Inter, Roboto, Arial", color="#E6EDF7"),
        hoverlabel=dict(bgcolor="rgba(12, 18, 30, 0.95)", font=dict(color="#E6EDF7", size=12)),
        hovertemplate="<b>%{y}</b><br>Count: %{x:,}<extra></extra>",
    )

    fig_bar.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(t=10, l=10, r=10, b=10),
        font=dict(family="Inter, Roboto, Arial", color="#E6EDF7"),
        xaxis=dict(
            showgrid=True,
            gridcolor="rgba(255,255,255,0.08)",
            zeroline=False,
            showline=False,
            tickfont=dict(color="rgba(230,237,247,0.85)", size=11),
            title=None,
        ),
        yaxis=dict(
            categoryorder="total ascending",
            tickfont=dict(color="rgba(230,237,247,0.92)", size=12),
            title=None,
        ),
        showlegend=False,
    )

    st.plotly_chart(fig_bar, use_container_width=True)
