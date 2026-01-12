import plotly.express as px
import streamlit as st

from utils import load_data, render_sidebar

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(page_title="Geographic Trends", page_icon="🗺️", layout="wide")

# -----------------------------
# Global Dark UI (CSS)
# -----------------------------
st.markdown(
    """
<style>
/* App background */
.stApp {
    background: radial-gradient(1200px 600px at 20% 0%, #0B1220 0%, #070B14 45%, #05070E 100%);
    color: #E6EDF7;
}

/* Typography */
h1, h2, h3, span, div, label {
    color: #E6EDF7;
}

/* Subtle divider */
hr { border-color: rgba(255,255,255,0.10); }

/* Make select / multiselect match dark */
div[data-baseweb="select"] > div {
    background-color: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    border-radius: 12px !important;
}

/* Plotly card wrapper */
div[data-testid="stPlotlyChart"] > div {
    border-radius: 18px;
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.10);
    box-shadow: 0 18px 55px rgba(0,0,0,0.45);
    padding: 14px;
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

# -----------------------------
# Data
# -----------------------------
df_raw = load_data()

# Header
st.markdown(
    """
<div style="margin-bottom: 30px;">
    <h1 style="color: white; font-size: 2.5rem; margin-bottom: 0;">Geographic Distribution</h1>
    <p style="color: #94A3B8; margin-top: 10px; font-size: 1.1rem;">
        Regional intensity and submission channel preferences
    </p>
</div>
""",
    unsafe_allow_html=True,
)

df = render_sidebar(df_raw)
if df.empty:
    st.stop()

# -----------------------------
# Regional Heatmap (USA States)
# -----------------------------
st.subheader("Regional Heatmap")

state_counts = df["state"].value_counts().reset_index()
state_counts.columns = ["State", "Complaints"]

# A deeper finance-ish blue scale for dark UI
blue_scale = [
    [0.00, "#0B1220"],
    [0.15, "#0B2A3F"],
    [0.35, "#0B4A6A"],
    [0.55, "#0EA5E9"],
    [0.75, "#38BDF8"],
    [1.00, "#E0F2FE"],
]

fig_map = px.choropleth(
    state_counts,
    locations="State",
    locationmode="USA-states",
    color="Complaints",
    scope="usa",
    color_continuous_scale=blue_scale,
    labels={"Complaints": "Volume"},
)

fig_map.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    margin=dict(t=0, l=0, r=0, b=0),
    font=dict(family="Inter, Roboto, Arial", color="#E6EDF7", size=12),
    geo=dict(
        bgcolor="rgba(0,0,0,0)",
        lakecolor="rgba(20, 70, 110, 0.35)",
        landcolor="rgba(255,255,255,0.02)",
        subunitcolor="rgba(255,255,255,0.16)",
        countrycolor="rgba(255,255,255,0.16)",
        showlakes=True,
        showcountries=True,
        projection_type="albers usa",
    ),
    coloraxis_colorbar=dict(
        title="Volume",
        thickness=14,
        len=0.72,
        bgcolor="rgba(10, 15, 25, 0.75)",
        bordercolor="rgba(255,255,255,0.12)",
        borderwidth=1,
        tickfont=dict(size=10, color="#D7E2F2"),
        x=1.02,
    ),
)

fig_map.update_traces(
    marker_line_color="rgba(255,255,255,0.35)",
    marker_line_width=1.1,
    hoverlabel=dict(bgcolor="rgba(12, 18, 30, 0.95)", font=dict(color="#E6EDF7", size=12)),
    hovertemplate="<b>%{location}</b><br>Complaints: %{z:,}<extra></extra>",
)

st.plotly_chart(fig_map, use_container_width=True)

# -----------------------------
# Submission Channels
# -----------------------------
st.markdown("---")
st.subheader("Submission Channels")

available_channels = sorted(df["submitted_via"].dropna().unique().tolist())
selected_channels = st.multiselect(
    "Filter Channels:",
    options=available_channels,
    default=available_channels,
)

df_channel_filtered = df[df["submitted_via"].isin(selected_channels)]

if df_channel_filtered.empty:
    st.stop()

channel_counts = df_channel_filtered["submitted_via"].value_counts().reset_index()
channel_counts.columns = ["Channel", "Count"]

# Use a single strong color (cleaner + more readable on dark UI)
fig_ch = px.bar(
    channel_counts,
    x="Count",
    y="Channel",
    orientation="h",
    text="Count",
)

fig_ch.update_traces(
    marker=dict(
        color="rgba(56, 189, 248, 0.92)",
        line=dict(color="rgba(255,255,255,0.18)", width=1),
    ),
    texttemplate="%{x:,}",
    textposition="outside",
    textfont=dict(size=12, family="Inter, Roboto, Arial", color="#E6EDF7"),
    hovertemplate="<b>%{y}</b><br>Count: %{x:,}<extra></extra>",
    hoverlabel=dict(bgcolor="rgba(12, 18, 30, 0.95)", font=dict(color="#E6EDF7", size=12)),
)

fig_ch.update_layout(
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

st.plotly_chart(fig_ch, use_container_width=True)
