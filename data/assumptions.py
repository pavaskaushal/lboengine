# ============================================================
# LBOEngine - Default Assumptions
# These are the starting assumptions for the LBO model
# A PE analyst would adjust these based on the target company
# ============================================================

# COMPANY DETAILS
DEFAULT_COMPANY_NAME = "TechCo India Ltd"
DEFAULT_SECTOR = "B2B SaaS / TMT"

# ACQUISITION ASSUMPTIONS
# Entry multiple = how many times EBITDA we pay for the company
# 10-15x is typical for high quality SaaS businesses in India
DEFAULT_ENTRY_EBITDA_MULTIPLE = 12.0

# LTM EBITDA = Last Twelve Months EBITDA of the target
# This is the base profitability we are buying
DEFAULT_LTM_EBITDA = 500.0  # INR Crores

# DEBT STRUCTURE
# PE firms use debt to amplify returns
# Typical LBO uses 60-70% debt financing
DEFAULT_DEBT_PERCENTAGE = 65.0  # % of total acquisition price
DEFAULT_INTEREST_RATE = 9.5     # % annual interest rate
DEFAULT_DEBT_TERM = 5           # years to repay debt

# OPERATING ASSUMPTIONS
# How fast will the company grow under PE ownership
DEFAULT_REVENUE_GROWTH = 18.0   # % per year
DEFAULT_EBITDA_MARGIN = 28.0    # % of revenue
DEFAULT_DA_PCT = 5.0            # D&A as % of revenue
DEFAULT_CAPEX_PCT = 6.0         # CapEx as % of revenue
DEFAULT_NWC_PCT = 2.0           # Change in NWC as % of revenue
DEFAULT_TAX_RATE = 25.0         # Corporate tax rate %

# EXIT ASSUMPTIONS
# Exit multiple = what multiple we sell at after 5 years
# Usually assume same or lower than entry (conservative)
DEFAULT_EXIT_EBITDA_MULTIPLE = 11.0
DEFAULT_HOLD_PERIOD = 5         # years

# CURRENCY
CURRENCY_SYMBOL = "\u20b9"      # Indian Rupee symbol
CURRENCY_UNIT = "Crores"

# RETURN THRESHOLDS
# PE firms typically target these minimum returns
MIN_IRR_TARGET = 20.0           # % minimum acceptable IRR
MIN_MOIC_TARGET = 2.5           # minimum Money on Invested Capital