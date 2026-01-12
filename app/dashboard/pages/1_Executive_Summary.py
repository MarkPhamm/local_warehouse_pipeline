import plotly.express as px
import streamlit as st

from utils import load_data, render_sidebar

st.set_page_config(page_title="Executive Summary", page_icon="📊", layout="wide")

# ==========================================
# DARK THEME CSS
# ==========================================
st.markdown(
    """
<style>
    /* Global Background */
    [data-testid="stAppViewContainer"] {
        background-color: #020617; /* Dark Slate */
        color: #E2E8F0;
    }

    /* KPI Card Style */
    .kpi-card {
        background: linear-gradient(145deg, #0F172A, #0B1120);
        border-left: 4px solid #00AEEF; /* Barclays Cyan */
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

    /* Chart Container Style */
    .chart-container {
        background: #0B1120;
        border: 1px solid rgba(255,255,255,0.05);
        border-radius: 16px;
        padding: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
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

# ==========================================
# 2. DATA LOADING
# ==========================================
df_raw = load_data()
if df_raw.empty:
    st.error("No data could be loaded. Please check the database connection.")
    st.stop()

# Sidebar Filter
df = render_sidebar(df_raw)

# ==========================================
# HEADER
# ==========================================
st.markdown(
    """
<div style="margin-bottom: 30px;">
    <h1 style="color: white; font-size: 2.5rem; margin-bottom: 0;">Executive Summary</h1>
    <p style="color: #94A3B8; margin-top: 10px; font-size: 1.1rem;">
        High-level overview of complaint volume and resolution health metrics.
    </p>
</div>
""",
    unsafe_allow_html=True,
)

# ==========================================
# KPI SECTION (Custom HTML Cards)
# ==========================================
total_complaints = len(df)
timely_rate = (df["timely"].mean() * 100) if total_complaints > 0 else 0
top_product = df["product"].mode()[0] if not df.empty else "N/A"
top_issue = df["issue"].mode()[0] if not df.empty else "N/A"


# Shorten text for KPIs if too long
def truncate(text, length=20):
    return text[:length] + "..." if len(text) > length else text


# Layout
c1, c2, c3, c4 = st.columns(4)


def kpi_html(label, value, icon, tooltip=""):
    return f"""
    <div class="kpi-card" title="{tooltip}">
        <div class="kpi-icon">{icon}</div>
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
    </div>
    """


def adaptive_text(text):
    if len(text) > 19:
        return f"<span style='font-size:1.5rem'>{text}</span>"
    return f"<span style='font-size:2.2rem'>{text}</span>"


with c1:
    st.markdown(kpi_html("Total Volume", f"{total_complaints:,}", "📈"), unsafe_allow_html=True)
with c2:
    color = "#4ADE80" if timely_rate > 90 else "#FACC15"  # Green if >90%, else Yellow
    val_html = f"<span style='color:{color}'>{timely_rate:.1f}%</span>"
    st.markdown(kpi_html("Timely Response", val_html, "⏱️"), unsafe_allow_html=True)
with c3:
    st.markdown(
        kpi_html("Top Product", adaptive_text(top_product), "🏆", top_product),
        unsafe_allow_html=True,
    )
with c4:
    st.markdown(
        kpi_html("Top Issue", adaptive_text(top_issue), "🎯", top_issue), unsafe_allow_html=True
    )

st.markdown("<br>", unsafe_allow_html=True)

# ==========================================
# CHARTS SECTION (Dark Mode Plotly)
# ==========================================
col_left, col_right = st.columns((2, 1), gap="large")

# --- CHART 1: Volume Trend (Left) ---
with col_left:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown("### Complaint Volume Over Time")

    df_trend = df.set_index("date_received").resample("M").size().reset_index(name="count")

    fig_trend = px.area(
        df_trend,
        x="date_received",
        y="count",
        template="plotly_dark",  # Creates the dark base
    )

    fig_trend.update_traces(
        line_color="#00AEEF",  # Barclays Cyan
        fillcolor="rgba(0, 174, 239, 0.1)",  # Very subtle fill
        line_width=3,
    )

    fig_trend.update_layout(
        height=400,
        plot_bgcolor="rgba(0,0,0,0)",  # Transparent
        paper_bgcolor="rgba(0,0,0,0)",  # Transparent
        margin=dict(t=20, l=0, r=0, b=0),
        xaxis=dict(showgrid=False, title=None, tickfont=dict(color="#94A3B8")),
        yaxis=dict(
            showgrid=True,
            gridcolor="rgba(255,255,255,0.05)",  # Subtle grid
            title=None,
            tickfont=dict(color="#94A3B8"),
        ),
        hovermode="x unified",
    )
    st.plotly_chart(fig_trend, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# --- CHART 2: Resolution Types (Right) ---
with col_right:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown("### Resolution Types")

    resp_counts = df["company_response"].value_counts().reset_index()
    resp_counts.columns = ["Response", "Count"]

    # Custom Gradient Palette: Cyan -> Navy -> Slate
    colors = ["#00AEEF", "#0078B4", "#005A8C", "#00395D", "#475569"]

    fig_donut = px.pie(
        resp_counts, values="Count", names="Response", hole=0.64, color_discrete_sequence=colors
    )

    fig_donut.update_traces(
        textposition="inside",
        textinfo="percent",
        hoverinfo="label+percent+value",
        textfont=dict(color="white", weight="bold", size=16),
        # 👇 THIS CREATES THE GAP
        marker=dict(
            line=dict(
                color="#0B1120",  # Matches the card background color
                width=3.5,  # Thickness of the "gap"
            )
        ),
    )

    fig_donut.update_layout(
        height=400,
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.1,
            xanchor="center",
            x=0.5,
            font=dict(color="black", size=11),
        ),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(t=20, l=20, r=20, b=20),
        annotations=[
            dict(
                text=f"{len(df):,}", x=0.5, y=0.5, font_size=20, showarrow=False, font_color="black"
            )
        ],
    )

    st.plotly_chart(fig_donut, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
