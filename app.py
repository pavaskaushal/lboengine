# ============================================================
# LBOEngine - Main Application
# Built by Pavas Kaushal
# MBA Finance | TMT Strategy Consultant
# ============================================================

import streamlit as st
from models.lbo_model import calculate_lbo
from components.sidebar import render_sidebar
from components.metrics import (
    render_transaction_metrics,
    render_return_metrics,
    render_verdict
)
from components.charts import (
    render_sources_uses_chart,
    render_operating_model_chart,
    render_sensitivity_tables,
    render_returns_chart
)
from data.assumptions import CURRENCY_SYMBOL

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="LBOEngine | Leveraged Buyout Model",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
    <style>
    .main { background-color: #0f1117; }
    .kpi-card {
        background-color: #1e2130;
        border-radius: 10px;
        padding: 20px;
        border-left: 4px solid #f59e0b;
    }
    .kpi-value {
        font-size: 28px;
        font-weight: bold;
        color: #f59e0b;
    }
    .kpi-label {
        font-size: 14px;
        color: #8b8fa8;
        margin-bottom: 8px;
    }
    .section-header {
        font-size: 20px;
        font-weight: bold;
        color: #ffffff;
        padding: 10px 0;
        border-bottom: 2px solid #f59e0b;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# ============================================================
# DASHBOARD HEADER
# ============================================================

st.markdown("""
    <div style='text-align: center; padding: 20px 0;'>
        <h1 style='color: #f59e0b; font-size: 42px; font-weight: bold;'>
            💼 LBOEngine
        </h1>
        <p style='color: #8b8fa8; font-size: 18px;'>
            Leveraged Buyout Modelling & Returns Analysis
        </p>
        <p style='color: #8b8fa8; font-size: 14px;'>
            Private Equity | Investment Banking | TMT Sector
        </p>
        <p style='color: #ffffff; font-size: 15px; margin-top: 10px;'>
            Built by <span style='color: #f59e0b; font-weight: bold;'>
            Pavas Kaushal</span> · MBA Finance · TMT Strategy
        </p>
    </div>
""", unsafe_allow_html=True)

st.divider()

# ============================================================
# RENDER SIDEBAR AND GET INPUTS
# ============================================================

inputs = render_sidebar()

# ============================================================
# RUN LBO MODEL
# ============================================================

with st.spinner("Running LBO model..."):
    results = calculate_lbo(
        company_name=inputs["company_name"],
        ltm_ebitda=inputs["ltm_ebitda"],
        entry_multiple=inputs["entry_multiple"],
        debt_percentage=inputs["debt_percentage"],
        interest_rate=inputs["interest_rate"],
        revenue_growth=inputs["revenue_growth"],
        ebitda_margin=inputs["ebitda_margin"],
        da_pct=inputs["da_pct"],
        capex_pct=inputs["capex_pct"],
        nwc_pct=inputs["nwc_pct"],
        tax_rate=inputs["tax_rate"],
        exit_multiple=inputs["exit_multiple"],
        hold_period=inputs["hold_period"]
    )

# ============================================================
# RENDER INVESTMENT VERDICT
# ============================================================

render_verdict(results)

# ============================================================
# RENDER TRANSACTION METRICS
# ============================================================

render_transaction_metrics(results)

# ============================================================
# RENDER SOURCES & USES CHART
# ============================================================

render_sources_uses_chart(results)

# ============================================================
# RENDER RETURN METRICS
# ============================================================

render_return_metrics(results)

# ============================================================
# RENDER RETURNS CHART
# ============================================================

render_returns_chart(results, inputs["hold_period"])

# ============================================================
# RENDER OPERATING MODEL
# ============================================================

render_operating_model_chart(results["df_operations"])

# ============================================================
# RENDER SENSITIVITY TABLES
# ============================================================

render_sensitivity_tables(
    results["df_sensitivity_irr"],
    results["df_sensitivity_moic"]
)

# ============================================================
# FOOTER
# ============================================================

st.divider()
st.markdown("""
    <div style='text-align: center; color: #8b8fa8;
    font-size: 13px; padding: 20px;'>
        LBOEngine | Leveraged Buyout Modelling & Returns Analysis<br>
        Built by Pavas Kaushal · MBA Finance · TMT Strategy Consultant<br>
        Built with Python · NumPy · Pandas · Streamlit · Plotly<br>
        For educational purposes only · Not financial advice
    </div>
""", unsafe_allow_html=True)