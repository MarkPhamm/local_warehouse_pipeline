import plotly.express as px
import streamlit as st

from utils import load_data, render_sidebar

st.set_page_config(page_title="Company Performance", page_icon="🏢", layout="wide")

st.markdown(
    """
<style>
    /* Global Background */
    [data-testid="stAppViewContainer"] {
        background-color: #020617; /* Dark Slate */
        color: #E2E8F0;
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

# HEADER
st.markdown(
    """
<div style="margin-bottom: 30px;">
    <h1 style="color: white; font-size: 2.5rem; margin-bottom: 0;">Company Performance</h1>
    <p style="color: #94A3B8; margin-top: 10px; font-size: 1.1rem;">
        Efficiency Analysis: Volume vs. Timeliness Matrix.
    </p>
</div>
""",
    unsafe_allow_html=True,
)


df_raw = load_data()

df = render_sidebar(df_raw)

if df.empty:
    st.warning("No data available for the selected filters.")
    st.stop()

# --- AGGREGATION ---
company_stats = (
    df.groupby("company")
    .agg(Total_Complaints=("product", "count"), Timely_Rate=("timely", "mean"))
    .reset_index()
)

company_stats = company_stats[company_stats["Total_Complaints"] > 0]
company_stats["Timely_Rate"] = company_stats["Timely_Rate"] * 100

# --- SCATTER PLOT ---
col_chart, col_table = st.columns([2, 1])

with col_chart:
    st.subheader("Performance Matrix")

    fig_scatter = px.scatter(
        company_stats,
        x="Total_Complaints",
        y="Timely_Rate",
        hover_name="company",
        size="Total_Complaints",
        color="Timely_Rate",
        color_continuous_scale=["#DC2626", "#F59E0B", "#10B981", "#00AEEF"],  # Red to Green to Blue
        labels={"Total_Complaints": "Volume", "Timely_Rate": "Timeliness (%)"},
        size_max=60,
    )

    avg_vol = company_stats["Total_Complaints"].mean()
    avg_time = company_stats["Timely_Rate"].mean()

    fig_scatter.add_hline(
        y=avg_time,
        line_dash="dot",
        line_color="#6B7280",
        line_width=2,
        annotation_text="Avg Timeliness",
        annotation_position="right",
        annotation_font=dict(size=11, color="#4B5563"),
    )
    fig_scatter.add_vline(
        x=avg_vol,
        line_dash="dot",
        line_color="#6B7280",
        line_width=2,
        annotation_text="Avg Volume",
        annotation_font=dict(size=11, color="#4B5563"),
    )

    fig_scatter.update_layout(
        plot_bgcolor="#FAFBFC",
        paper_bgcolor="white",
        xaxis_gridcolor="#E8EEF2",
        yaxis_gridcolor="#E8EEF2",
        xaxis_gridwidth=1,
        yaxis_gridwidth=1,
        margin=dict(t=30, l=20, r=20, b=20),
        font=dict(family="Roboto", color="#1F2937"),
        xaxis=dict(
            title_font=dict(color="#00395D", size=13),
            tickfont=dict(color="#4B5563", size=11),
            showline=True,
            linewidth=2,
            linecolor="#E8EEF2",
        ),
        yaxis=dict(
            title_font=dict(color="#00395D", size=13),
            tickfont=dict(color="#4B5563", size=11),
            showline=True,
            linewidth=2,
            linecolor="#E8EEF2",
        ),
        coloraxis_colorbar=dict(
            title="Timeliness %",
            thickness=15,
            len=0.7,
            bgcolor="rgba(255,255,255,0.9)",
            bordercolor="#E8EEF2",
            borderwidth=1,
            tickfont=dict(size=10, color="#4B5563"),
        ),
    )

    fig_scatter.update_traces(
        marker=dict(line=dict(width=2, color="white"), opacity=0.85),
        hovertemplate="<b>%{hovertext}</b><br>Volume: %{x:,}<br>Timeliness: %{y:.1f}%<extra></extra>",
    )

    st.plotly_chart(fig_scatter, use_container_width=True)

with col_table:
    st.subheader("Leaderboard")

    # Styled Dataframe
    top_performers = company_stats.sort_values(by="Total_Complaints", ascending=False).head(10)

    st.dataframe(
        top_performers.style.background_gradient(
            subset=["Timely_Rate"], cmap="RdYlGn", vmin=0, vmax=100
        )
        .background_gradient(subset=["Total_Complaints"], cmap="Blues")
        .format({"Timely_Rate": "{:.1f}%", "Total_Complaints": "{:,}"}),
        use_container_width=True,
        height=500,
    )
