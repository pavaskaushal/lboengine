# ============================================================
# LBOEngine - Metrics Component
# All KPI cards live here
# ============================================================

import streamlit as st
from data.assumptions import (
    CURRENCY_SYMBOL,
    CURRENCY_UNIT,
    MIN_IRR_TARGET,
    MIN_MOIC_TARGET
)

def render_transaction_metrics(results):
    # ============================================================
    # TRANSACTION STRUCTURE CARDS
    # Shows purchase price, debt and equity
    # ============================================================

    st.markdown("<div class='section-header'>💼 Transaction Structure</div>",
        unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(
            "<div class='kpi-card'>"
            "<div class='kpi-label'>Purchase Price</div>"
            "<div class='kpi-value'>"
            + CURRENCY_SYMBOL + f"{results['purchase_price']:,.0f}" + "</div>"
            "<div style='color: #8b8fa8; font-size: 12px;'>"
            + CURRENCY_UNIT + " · Entry EV</div>"
            "</div>",
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            "<div class='kpi-card'>"
            "<div class='kpi-label'>Total Debt</div>"
            "<div class='kpi-value' style='color:#ff6b6b;'>"
            + CURRENCY_SYMBOL + f"{results['total_debt']:,.0f}" + "</div>"
            "<div style='color: #8b8fa8; font-size: 12px;'>"
            + f"{results['debt_percentage']:.0f}" + "% of Purchase Price</div>"
            "</div>",
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            "<div class='kpi-card'>"
            "<div class='kpi-label'>Equity Invested</div>"
            "<div class='kpi-value' style='color:#00d4aa;'>"
            + CURRENCY_SYMBOL + f"{results['equity_invested']:,.0f}" + "</div>"
            "<div style='color: #8b8fa8; font-size: 12px;'>"
            + f"{results['equity_percentage']:.0f}" + "% of Purchase Price</div>"
            "</div>",
            unsafe_allow_html=True
        )

    with col4:
        st.markdown(
            "<div class='kpi-card'>"
            "<div class='kpi-label'>Remaining Debt at Exit</div>"
            "<div class='kpi-value' style='color:#ff6b6b;'>"
            + CURRENCY_SYMBOL + f"{results['remaining_debt']:,.0f}" + "</div>"
            "<div style='color: #8b8fa8; font-size: 12px;'>After debt paydown</div>"
            "</div>",
            unsafe_allow_html=True
        )

    st.markdown("<br>", unsafe_allow_html=True)


def render_return_metrics(results):
    # ============================================================
    # RETURN METRICS CARDS
    # Shows IRR, MOIC and exit metrics
    # ============================================================

    st.markdown("<div class='section-header'>📈 Return Analysis</div>",
        unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    # IRR Card
    irr_color = "#00d4aa" if results["meets_irr_target"] else "#ff6b6b"
    irr_label = "✅ Above Target" if results["meets_irr_target"] else "❌ Below Target"

    with col1:
        st.markdown(
            "<div class='kpi-card'>"
            "<div class='kpi-label'>IRR</div>"
            "<div class='kpi-value' style='color:" + irr_color + ";'>"
            + f"{results['irr']:.1f}" + "%</div>"
            "<div style='color:" + irr_color + "; font-size: 12px;'>"
            + irr_label + f" ({MIN_IRR_TARGET:.0f}% min)</div>"
            "</div>",
            unsafe_allow_html=True
        )

    # MOIC Card
    moic_color = "#00d4aa" if results["meets_moic_target"] else "#ff6b6b"
    moic_label = "✅ Above Target" if results["meets_moic_target"] else "❌ Below Target"

    with col2:
        st.markdown(
            "<div class='kpi-card'>"
            "<div class='kpi-label'>MOIC</div>"
            "<div class='kpi-value' style='color:" + moic_color + ";'>"
            + f"{results['moic']:.2f}" + "x</div>"
            "<div style='color:" + moic_color + "; font-size: 12px;'>"
            + moic_label + f" ({MIN_MOIC_TARGET:.1f}x min)</div>"
            "</div>",
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            "<div class='kpi-card'>"
            "<div class='kpi-label'>Exit Enterprise Value</div>"
            "<div class='kpi-value'>"
            + CURRENCY_SYMBOL + f"{results['exit_ev']:,.0f}" + "</div>"
            "<div style='color: #8b8fa8; font-size: 12px;'>"
            + CURRENCY_UNIT + " · Exit EV</div>"
            "</div>",
            unsafe_allow_html=True
        )

    with col4:
        st.markdown(
            "<div class='kpi-card'>"
            "<div class='kpi-label'>Exit Equity Value</div>"
            "<div class='kpi-value' style='color:#00d4aa;'>"
            + CURRENCY_SYMBOL + f"{results['exit_equity_value']:,.0f}" + "</div>"
            "<div style='color: #8b8fa8; font-size: 12px;'>"
            + CURRENCY_UNIT + " · To PE Fund</div>"
            "</div>",
            unsafe_allow_html=True
        )

    st.markdown("<br>", unsafe_allow_html=True)


def render_verdict(results):
    # ============================================================
    # INVESTMENT VERDICT
    # Go or No Go recommendation
    # ============================================================

    meets_both = results["meets_irr_target"] and results["meets_moic_target"]

    if meets_both:
        st.markdown("""
            <div style='background-color: #0d2b1f; border-radius: 10px;
            padding: 20px; border-left: 6px solid #00d4aa; margin: 20px 0;'>
                <h3 style='color: #00d4aa; margin: 0;'>
                    ✅ INVESTMENT RECOMMENDATION: GO
                </h3>
                <p style='color: #ffffff; margin: 10px 0 0 0; font-size: 14px;'>
                    This deal meets both IRR and MOIC return thresholds.
                    The transaction delivers attractive risk-adjusted returns
                    and is recommended for Investment Committee approval.
                </p>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <div style='background-color: #2b0d0d; border-radius: 10px;
            padding: 20px; border-left: 6px solid #ff6b6b; margin: 20px 0;'>
                <h3 style='color: #ff6b6b; margin: 0;'>
                    ❌ INVESTMENT RECOMMENDATION: NO GO
                </h3>
                <p style='color: #ffffff; margin: 10px 0 0 0; font-size: 14px;'>
                    This deal does not meet minimum return thresholds.
                    Consider renegotiating the entry price or improving
                    the operating model before proceeding.
                </p>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)