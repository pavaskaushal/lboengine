# ============================================================
# LBOEngine - Charts Component
# All Plotly charts live here
# ============================================================

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import streamlit as st
from data.assumptions import CURRENCY_SYMBOL, CURRENCY_UNIT

# Chart theme settings
PLOT_BG = "#1e2130"
PAPER_BG = "#1e2130"
FONT_COLOR = "#ffffff"
GRID_COLOR = "#2d3148"
ACCENT_COLOR = "#f59e0b"

def render_sources_uses_chart(results):
    # ============================================================
    # SOURCES & USES CHART
    # Classic IB chart showing how the deal is financed
    # ============================================================

    st.markdown("<div class='section-header'>🏗️ Sources & Uses of Funds</div>",
        unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        # Sources pie chart
        fig_sources = go.Figure(go.Pie(
            labels=["Debt", "Equity"],
            values=[results["total_debt"], results["equity_invested"]],
            hole=0.4,
            marker_colors=["#ff6b6b", "#00d4aa"]
        ))
        fig_sources.update_layout(
            title="Sources of Funds",
            plot_bgcolor=PLOT_BG,
            paper_bgcolor=PAPER_BG,
            font=dict(color=FONT_COLOR),
            legend=dict(bgcolor=PLOT_BG)
        )
        st.plotly_chart(fig_sources, use_container_width=True)

    with col2:
        # Waterfall chart showing EV buildup
        fig_waterfall = go.Figure(go.Waterfall(
            name="EV Bridge",
            orientation="v",
            measure=["absolute", "relative", "total"],
            x=["Entry EV", "Value Creation", "Exit EV"],
            y=[
                results["purchase_price"],
                results["exit_ev"] - results["purchase_price"],
                0
            ],
            connector=dict(line=dict(color="#ffffff")),
            decreasing=dict(marker=dict(color="#ff6b6b")),
            increasing=dict(marker=dict(color="#00d4aa")),
            totals=dict(marker=dict(color=ACCENT_COLOR))
        ))
        fig_waterfall.update_layout(
            title="Enterprise Value Bridge",
            plot_bgcolor=PLOT_BG,
            paper_bgcolor=PAPER_BG,
            font=dict(color=FONT_COLOR),
            yaxis=dict(
                gridcolor=GRID_COLOR,
                tickprefix=CURRENCY_SYMBOL
            ),
            xaxis=dict(gridcolor=GRID_COLOR)
        )
        st.plotly_chart(fig_waterfall, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)


def render_operating_model_chart(df_operations):
    # ============================================================
    # OPERATING MODEL CHART
    # Shows revenue and EBITDA growth over hold period
    # ============================================================

    st.markdown("<div class='section-header'>📊 Operating Model</div>",
        unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        fig_rev = go.Figure()

        fig_rev.add_trace(go.Bar(
            x=df_operations["Year"],
            y=df_operations["Revenue"],
            name="Revenue",
            marker_color=ACCENT_COLOR
        ))

        fig_rev.add_trace(go.Bar(
            x=df_operations["Year"],
            y=df_operations["EBITDA"],
            name="EBITDA",
            marker_color="#00d4aa"
        ))

        fig_rev.update_layout(
            title="Revenue & EBITDA Growth",
            barmode="group",
            plot_bgcolor=PLOT_BG,
            paper_bgcolor=PAPER_BG,
            font=dict(color=FONT_COLOR),
            legend=dict(bgcolor=PLOT_BG),
            xaxis=dict(gridcolor=GRID_COLOR),
            yaxis=dict(
                gridcolor=GRID_COLOR,
                tickprefix=CURRENCY_SYMBOL
            )
        )

        st.plotly_chart(fig_rev, use_container_width=True)

    with col2:
        fig_debt = go.Figure()

        fig_debt.add_trace(go.Scatter(
            x=df_operations["Year"],
            y=df_operations["Debt Balance"],
            name="Debt Balance",
            line=dict(color="#ff6b6b", width=3),
            mode="lines+markers",
            fill="tozeroy",
            fillcolor="rgba(255, 107, 107, 0.1)"
        ))

        fig_debt.add_trace(go.Scatter(
            x=df_operations["Year"],
            y=df_operations["FCFE"],
            name="Free Cash Flow",
            line=dict(color="#00d4aa", width=3),
            mode="lines+markers"
        ))

        fig_debt.update_layout(
            title="Debt Paydown & Free Cash Flow",
            plot_bgcolor=PLOT_BG,
            paper_bgcolor=PAPER_BG,
            font=dict(color=FONT_COLOR),
            legend=dict(bgcolor=PLOT_BG),
            xaxis=dict(gridcolor=GRID_COLOR),
            yaxis=dict(
                gridcolor=GRID_COLOR,
                tickprefix=CURRENCY_SYMBOL
            )
        )

        st.plotly_chart(fig_debt, use_container_width=True)

    # Full operating model table
    st.markdown("#### 📋 Full Operating Model")
    display_cols = [
        "Year", "Revenue", "EBITDA", "EBIT",
        "Interest Expense", "Net Income", "FCFE",
        "Debt Repayment", "Debt Balance"
    ]
    st.dataframe(
        df_operations[display_cols],
        use_container_width=True,
        hide_index=True
    )

    st.markdown("<br>", unsafe_allow_html=True)


def render_sensitivity_tables(df_irr, df_moic):
    # ============================================================
    # SENSITIVITY ANALYSIS TABLES
    # Shows IRR and MOIC across different entry/exit multiples
    # This is the classic PE sensitivity table
    # ============================================================

    st.markdown("<div class='section-header'>🎯 Sensitivity Analysis</div>",
        unsafe_allow_html=True)

    st.markdown("""
        <p style='color: #8b8fa8; font-size: 13px;'>
        How do returns change with different entry and exit multiples?
        Green = meets IRR target. Red = below target.
        </p>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("##### IRR Sensitivity (%)")
        df_irr_display = df_irr.copy()
        df_irr_display.index.name = "Entry \\ Exit"
        df_irr_display = df_irr_display.reset_index()
        # Apply color only to numeric columns
        numeric_cols = [c for c in df_irr_display.columns if c != "Entry \\ Exit"]
        st.dataframe(
            df_irr_display.style.background_gradient(
                cmap="RdYlGn",
                vmin=0,
                vmax=40,
                subset=numeric_cols
            ),
            use_container_width=True,
            hide_index=True
        )

    with col2:
        st.markdown("##### MOIC Sensitivity (x)")
        df_moic_display = df_moic.copy()
        df_moic_display.index.name = "Entry \\ Exit"
        df_moic_display = df_moic_display.reset_index()
        numeric_cols = [c for c in df_moic_display.columns if c != "Entry \\ Exit"]
        st.dataframe(
            df_moic_display.style.background_gradient(
                cmap="RdYlGn",
                vmin=0,
                vmax=5,
                subset=numeric_cols
            ),
            use_container_width=True,
            hide_index=True
        )

    st.markdown("<br>", unsafe_allow_html=True)


def render_returns_chart(results, hold_period):
    # ============================================================
    # RETURNS SUMMARY CHART
    # Visual summary of equity invested vs exit value
    # ============================================================

    st.markdown("<div class='section-header'>💰 Returns Summary</div>",
        unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        fig_returns = go.Figure(go.Bar(
            x=["Equity Invested", "Exit Equity Value"],
            y=[results["equity_invested"], results["exit_equity_value"]],
            marker_color=["#ff6b6b", "#00d4aa"],
            text=[
                CURRENCY_SYMBOL + f"{results['equity_invested']:,.0f}",
                CURRENCY_SYMBOL + f"{results['exit_equity_value']:,.0f}"
            ],
            textposition="outside"
        ))

        fig_returns.update_layout(
            title=f"Equity Value Creation over {hold_period} Years",
            plot_bgcolor=PLOT_BG,
            paper_bgcolor=PAPER_BG,
            font=dict(color=FONT_COLOR),
            xaxis=dict(gridcolor=GRID_COLOR),
            yaxis=dict(
                gridcolor=GRID_COLOR,
                tickprefix=CURRENCY_SYMBOL
            )
        )

        st.plotly_chart(fig_returns, use_container_width=True)

    with col2:
        # IRR vs Target gauge chart
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=results["irr"],
            delta={"reference": 20, "suffix": "%"},
            title={"text": "IRR vs 20% Target"},
            gauge={
                "axis": {"range": [0, 50]},
                "bar": {"color": "#00d4aa" if results["meets_irr_target"] else "#ff6b6b"},
                "steps": [
                    {"range": [0, 20], "color": "#2b1515"},
                    {"range": [20, 50], "color": "#0d2b1f"}
                ],
                "threshold": {
                    "line": {"color": ACCENT_COLOR, "width": 4},
                    "thickness": 0.75,
                    "value": 20
                }
            },
            number={"suffix": "%"}
        ))

        fig_gauge.update_layout(
            plot_bgcolor=PLOT_BG,
            paper_bgcolor=PAPER_BG,
            font=dict(color=FONT_COLOR)
        )

        st.plotly_chart(fig_gauge, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)