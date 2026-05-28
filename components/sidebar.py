# ============================================================
# LBOEngine - Sidebar Component
# All user input controls live here
# Completely separate from the main app
# ============================================================

import streamlit as st
from data.assumptions import (
    DEFAULT_COMPANY_NAME,
    DEFAULT_SECTOR,
    DEFAULT_ENTRY_EBITDA_MULTIPLE,
    DEFAULT_LTM_EBITDA,
    DEFAULT_DEBT_PERCENTAGE,
    DEFAULT_INTEREST_RATE,
    DEFAULT_DEBT_TERM,
    DEFAULT_REVENUE_GROWTH,
    DEFAULT_EBITDA_MARGIN,
    DEFAULT_DA_PCT,
    DEFAULT_CAPEX_PCT,
    DEFAULT_NWC_PCT,
    DEFAULT_TAX_RATE,
    DEFAULT_EXIT_EBITDA_MULTIPLE,
    DEFAULT_HOLD_PERIOD,
    CURRENCY_SYMBOL,
    CURRENCY_UNIT
)

def render_sidebar():
    # ============================================================
    # This function renders all sidebar inputs and
    # returns them as a dictionary for use in app.py
    # ============================================================

    st.sidebar.markdown("## ⚙️ LBO Assumptions")
    st.sidebar.markdown("---")

    # COMPANY DETAILS
    st.sidebar.markdown("### 🏢 Target Company")

    company_name = st.sidebar.text_input(
        "Company Name",
        value=DEFAULT_COMPANY_NAME
    )

    sector = st.sidebar.text_input(
        "Sector",
        value=DEFAULT_SECTOR
    )

    ltm_ebitda = st.sidebar.number_input(
        f"LTM EBITDA ({CURRENCY_SYMBOL} {CURRENCY_UNIT})",
        min_value=10.0,
        max_value=100000.0,
        value=DEFAULT_LTM_EBITDA,
        step=10.0,
        help="Last Twelve Months EBITDA of the target company"
    )

    st.sidebar.markdown("---")

    # ACQUISITION STRUCTURE
    st.sidebar.markdown("### 💰 Acquisition Structure")

    entry_multiple = st.sidebar.slider(
        "Entry EV/EBITDA Multiple",
        min_value=4.0,
        max_value=25.0,
        value=DEFAULT_ENTRY_EBITDA_MULTIPLE,
        step=0.5,
        help="How many times EBITDA we pay for the company"
    )

    debt_percentage = st.sidebar.slider(
        "Debt Financing %",
        min_value=30.0,
        max_value=80.0,
        value=DEFAULT_DEBT_PERCENTAGE,
        step=1.0,
        help="What % of purchase price is financed by debt"
    )

    interest_rate = st.sidebar.slider(
        "Interest Rate %",
        min_value=5.0,
        max_value=20.0,
        value=DEFAULT_INTEREST_RATE,
        step=0.5,
        help="Annual interest rate on LBO debt"
    )

    st.sidebar.markdown("---")

    # OPERATING ASSUMPTIONS
    st.sidebar.markdown("### 📈 Operating Assumptions")

    revenue_growth = st.sidebar.slider(
        "Annual Revenue Growth %",
        min_value=1,
        max_value=50,
        value=int(DEFAULT_REVENUE_GROWTH),
        help="Expected annual revenue growth under PE ownership"
    )

    ebitda_margin = st.sidebar.slider(
        "EBITDA Margin %",
        min_value=1,
        max_value=60,
        value=int(DEFAULT_EBITDA_MARGIN),
        help="EBITDA as % of revenue"
    )

    tax_rate = st.sidebar.slider(
        "Tax Rate %",
        min_value=1,
        max_value=40,
        value=int(DEFAULT_TAX_RATE)
    )

    da_pct = st.sidebar.slider(
        "D&A as % of Revenue",
        min_value=1,
        max_value=20,
        value=int(DEFAULT_DA_PCT)
    )

    capex_pct = st.sidebar.slider(
        "CapEx as % of Revenue",
        min_value=1,
        max_value=30,
        value=int(DEFAULT_CAPEX_PCT)
    )

    nwc_pct = st.sidebar.slider(
        "Change in NWC as % of Revenue",
        min_value=1,
        max_value=10,
        value=int(DEFAULT_NWC_PCT)
    )

    st.sidebar.markdown("---")

    # EXIT ASSUMPTIONS
    st.sidebar.markdown("### 🚪 Exit Assumptions")

    exit_multiple = st.sidebar.slider(
        "Exit EV/EBITDA Multiple",
        min_value=4.0,
        max_value=25.0,
        value=DEFAULT_EXIT_EBITDA_MULTIPLE,
        step=0.5,
        help="What multiple we sell the company at after hold period"
    )

    hold_period = st.sidebar.selectbox(
        "Hold Period (Years)",
        options=[3, 4, 5, 6, 7],
        index=2,
        help="How many years PE firm holds the company"
    )

    st.sidebar.markdown("---")
    st.sidebar.markdown("""
        <p style='color: #8b8fa8; font-size: 11px; text-align: center;'>
            LBOEngine © 2024<br>
            Built by Pavas Kaushal<br>
            MBA Finance · TMT Strategy
        </p>
    """, unsafe_allow_html=True)

    # Return all inputs as a dictionary
    return {
        "company_name": company_name,
        "sector": sector,
        "ltm_ebitda": ltm_ebitda,
        "entry_multiple": entry_multiple,
        "debt_percentage": debt_percentage,
        "interest_rate": interest_rate,
        "revenue_growth": revenue_growth,
        "ebitda_margin": ebitda_margin,
        "tax_rate": tax_rate,
        "da_pct": da_pct,
        "capex_pct": capex_pct,
        "nwc_pct": nwc_pct,
        "exit_multiple": exit_multiple,
        "hold_period": hold_period
    }