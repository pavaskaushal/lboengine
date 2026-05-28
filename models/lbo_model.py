# ============================================================
# LBOEngine - Core LBO Model
# All financial calculations live here
# Completely separate from the UI
# ============================================================

import numpy as np
import pandas as pd
from data.assumptions import (
    MIN_IRR_TARGET,
    MIN_MOIC_TARGET
)

def calculate_lbo(
    company_name,
    ltm_ebitda,
    entry_multiple,
    debt_percentage,
    interest_rate,
    revenue_growth,
    ebitda_margin,
    da_pct,
    capex_pct,
    nwc_pct,
    tax_rate,
    exit_multiple,
    hold_period
):
    # ============================================================
    # STEP 1: TRANSACTION STRUCTURE
    # Calculate how much we pay and how we finance it
    # ============================================================

    # Enterprise Value = EBITDA x Entry Multiple
    # This is the total price we pay for the company
    purchase_price = ltm_ebitda * entry_multiple

    # Debt = Purchase Price x Debt Percentage
    # This is how much we borrow from banks
    total_debt = purchase_price * (debt_percentage / 100)

    # Equity = Purchase Price - Debt
    # This is how much the PE firm puts in from its fund
    equity_invested = purchase_price - total_debt

    # Convert rates to decimals
    interest_rate_dec = interest_rate / 100
    revenue_growth_dec = revenue_growth / 100
    ebitda_margin_dec = ebitda_margin / 100
    da_pct_dec = da_pct / 100
    capex_pct_dec = capex_pct / 100
    nwc_pct_dec = nwc_pct / 100
    tax_rate_dec = tax_rate / 100

    # ============================================================
    # STEP 2: 5 YEAR OPERATING MODEL
    # Project revenue, EBITDA and Free Cash Flow for each year
    # ============================================================

    # Starting revenue = EBITDA / EBITDA Margin
    base_revenue = ltm_ebitda / ebitda_margin_dec

    yearly_data = []
    debt_balance = total_debt
    cumulative_debt_repaid = 0

    for year in range(1, hold_period + 1):

        # Grow revenue each year
        revenue = base_revenue * (1 + revenue_growth_dec) ** year

        # Calculate EBITDA
        ebitda = revenue * ebitda_margin_dec

        # Calculate EBIT (EBITDA minus D&A)
        da = revenue * da_pct_dec
        ebit = ebitda - da

        # Interest expense on remaining debt
        interest_expense = debt_balance * interest_rate_dec

        # EBT = EBIT minus Interest
        ebt = ebit - interest_expense

        # Tax (only if profitable)
        tax = max(0, ebt * tax_rate_dec)

        # Net Income
        net_income = ebt - tax

        # Free Cash Flow to Equity
        # FCFE = Net Income + D&A - CapEx - Change in NWC
        capex = revenue * capex_pct_dec
        nwc_change = revenue * nwc_pct_dec
        fcfe = net_income + da - capex - nwc_change

        # Debt Repayment
        # Use all available free cash flow to repay debt
        debt_repayment = min(max(0, fcfe), debt_balance)
        debt_balance = max(0, debt_balance - debt_repayment)
        cumulative_debt_repaid += debt_repayment

        yearly_data.append({
            "Year": f"Year {year}",
            "Revenue": round(revenue, 1),
            "EBITDA": round(ebitda, 1),
            "EBITDA Margin %": round(ebitda_margin, 1),
            "D&A": round(da, 1),
            "EBIT": round(ebit, 1),
            "Interest Expense": round(interest_expense, 1),
            "EBT": round(ebt, 1),
            "Tax": round(tax, 1),
            "Net Income": round(net_income, 1),
            "CapEx": round(capex, 1),
            "FCFE": round(fcfe, 1),
            "Debt Repayment": round(debt_repayment, 1),
            "Debt Balance": round(debt_balance, 1),
        })

    df_operations = pd.DataFrame(yearly_data)

    # ============================================================
    # STEP 3: EXIT ANALYSIS
    # Calculate what we sell the company for after hold period
    # ============================================================

    # Exit EBITDA = Final year EBITDA
    exit_ebitda = df_operations.iloc[-1]["EBITDA"]

    # Exit Enterprise Value = Exit EBITDA x Exit Multiple
    exit_ev = exit_ebitda * exit_multiple

    # Equity Value at Exit = Exit EV - Remaining Debt
    exit_equity_value = exit_ev - debt_balance

    # ============================================================
    # STEP 4: RETURN CALCULATIONS
    # Calculate IRR and MOIC
    # ============================================================

    # MOIC = Money on Invested Capital
    # How many times did we multiply our money?
    moic = exit_equity_value / equity_invested

    # IRR = Internal Rate of Return
    # Annualised return on investment
    # We use numpy to solve for IRR
    # Cash flows: -equity invested at year 0, exit equity at end
    cash_flows = [-equity_invested] + [0] * (hold_period - 1) + [exit_equity_value]
    
    try:
        # numpy IRR calculation
        irr = np.irr(cash_flows) * 100
    except:
        # Fallback manual IRR calculation
        irr = ((exit_equity_value / equity_invested) ** (1 / hold_period) - 1) * 100

    # ============================================================
    # STEP 5: SENSITIVITY ANALYSIS
    # How do returns change with different exit multiples and
    # entry multiples?
    # ============================================================

    exit_multiples = [exit_multiple - 2, exit_multiple - 1,
                      exit_multiple, exit_multiple + 1, exit_multiple + 2]
    entry_multiples = [entry_multiple - 2, entry_multiple - 1,
                       entry_multiple, entry_multiple + 1, entry_multiple + 2]

    sensitivity_irr = []
    sensitivity_moic = []

    for em in entry_multiples:
        irr_row = []
        moic_row = []
        for xm in exit_multiples:
            pp = ltm_ebitda * em
            td = pp * (debt_percentage / 100)
            ei = pp - td
            db = td
            for y in range(1, hold_period + 1):
                rev = base_revenue * (1 + revenue_growth_dec) ** y
                eb = rev * ebitda_margin_dec
                d = rev * da_pct_dec
                eb_ebit = eb - d
                ie = db * interest_rate_dec
                ebt_s = eb_ebit - ie
                t = max(0, ebt_s * tax_rate_dec)
                ni = ebt_s - t
                cp = rev * capex_pct_dec
                nwc = rev * nwc_pct_dec
                fcf = ni + d - cp - nwc
                dr = min(max(0, fcf), db)
                db = max(0, db - dr)
            x_ebitda = base_revenue * (
                1 + revenue_growth_dec
            ) ** hold_period * ebitda_margin_dec
            x_ev = x_ebitda * xm
            x_eq = x_ev - db
            m = x_eq / ei if ei > 0 else 0
            cf = [-ei] + [0] * (hold_period - 1) + [x_eq]
            try:
                i = np.irr(cf) * 100
            except:
                i = ((x_eq / ei) ** (1 / hold_period) - 1) * 100 if ei > 0 else 0
            irr_row.append(round(i, 1))
            moic_row.append(round(m, 2))
        sensitivity_irr.append(irr_row)
        sensitivity_moic.append(moic_row)

    df_sensitivity_irr = pd.DataFrame(
        sensitivity_irr,
        index=[f"{m:.0f}x Entry" for m in entry_multiples],
        columns=[f"{m:.0f}x Exit" for m in exit_multiples]
    )

    df_sensitivity_moic = pd.DataFrame(
        sensitivity_moic,
        index=[f"{m:.0f}x Entry" for m in entry_multiples],
        columns=[f"{m:.0f}x Exit" for m in exit_multiples]
    )

    return {
        "purchase_price": round(purchase_price, 1),
        "total_debt": round(total_debt, 1),
        "equity_invested": round(equity_invested, 1),
        "debt_percentage": debt_percentage,
        "equity_percentage": round(100 - debt_percentage, 1),
        "exit_ev": round(exit_ev, 1),
        "exit_equity_value": round(exit_equity_value, 1),
        "remaining_debt": round(debt_balance, 1),
        "moic": round(moic, 2),
        "irr": round(irr, 1),
        "exit_ebitda": round(exit_ebitda, 1),
        "df_operations": df_operations,
        "df_sensitivity_irr": df_sensitivity_irr,
        "df_sensitivity_moic": df_sensitivity_moic,
        "meets_irr_target": irr >= MIN_IRR_TARGET,
        "meets_moic_target": moic >= MIN_MOIC_TARGET,
    }


def calculate_debt_schedule(
    total_debt,
    interest_rate,
    hold_period,
    annual_repayment
):
    # ============================================================
    # DEBT SCHEDULE
    # Shows how debt is paid down year by year
    # ============================================================

    schedule = []
    balance = total_debt
    interest_rate_dec = interest_rate / 100

    for year in range(1, hold_period + 1):
        interest = balance * interest_rate_dec
        repayment = min(annual_repayment, balance)
        closing_balance = max(0, balance - repayment)

        schedule.append({
            "Year": f"Year {year}",
            "Opening Balance": round(balance, 1),
            "Interest Expense": round(interest, 1),
            "Debt Repayment": round(repayment, 1),
            "Closing Balance": round(closing_balance, 1),
        })

        balance = closing_balance

    return pd.DataFrame(schedule)