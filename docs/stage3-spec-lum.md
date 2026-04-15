# Walmart Inc. Ratio Analysis — Technical Specification

**Created by:** Timothy Lum
**Updated by:** Timothy Lum
**Date Created:** April 15, 2026
**Date Updated:** April 15, 2026
**Version:** 1.0
**LLM Used:** Claude (Anthropic) — assisted with model build and data verification

**Role:** Financial Analyst / FP&A Analyst
**Audience:** CFO or Director of FP&A

**Purpose:** Provide a professional, quantitative specification documenting the Excel model's analytical structure for computing and interpreting 25+ accounting and performance ratios from Walmart Inc.'s FY2020 financial statements. This post-build specification captures what was built, what was learned, and how the model should be refined.

---

## 1. Problem Statement

Walmart Inc. (NYSE: WMT) is the world's largest retailer, operating hypermarkets, discount stores, and warehouse clubs across 27 countries under the Walmart U.S., Walmart International, and Sam's Club segments. This specification outlines the analytical framework for computing 25+ accounting and performance ratios from Walmart's FY2020 financial statements (fiscal year ended January 31, 2020), enabling management to assess financial health, operational efficiency, leverage, and value creation.

The analysis supports a CFO briefing on Walmart's financial position relative to its capital structure and operational model. Specific objectives are to determine whether Walmart generates returns exceeding its cost of capital, identify drivers of shareholder return via Du Pont decomposition, and flag any liquidity or leverage concerns warranting management attention.

---

## 2. Inputs (Known Variables)

All figures are in USD millions ($M) unless noted. Data sourced from Walmart Inc. Form 10-K, FY2020, filed March 20, 2020 (SEC EDGAR, CIK: 0000104169).

### Balance Sheet Items

| Variable | Description | Named Range | FY2020 | FY2019 |
|----------|-------------|-------------|--------|--------|
| Cash & cash equivalents | Liquid assets | `BAL_cash_marketable_securities_[year]` | 9,465 | 7,722 |
| Receivables, net | Accounts receivable | `BAL_receivables_[year]` | 6,284 | 6,283 |
| Inventories | Inventory balance | `BAL_inventories_[year]` | 44,435 | 44,269 |
| Total current assets | Sum of current assets | `BAL_assets_current_[year]` | 61,806 | 61,897 |
| Net PP&E | Property, plant & equipment net of depreciation | `BAL_fixed_assets_net_[year]` | 105,208 | 104,317 |
| Lease ROU assets | Operating + finance right-of-use assets | *(included in total assets)* | 21,841 | 7,078 |
| Goodwill | Intangible assets from acquisitions | *(included in total assets)* | 31,073 | 31,181 |
| Total assets | All assets | `BAL_assets_total_[year]` | 236,495 | 219,295 |
| Total current liabilities | Short-term obligations | `BAL_liabilities_current_[year]` | 77,790 | 76,477 |
| Long-term debt | Non-current borrowings | `BAL_debt_long_term_[year]` | 43,714 | 43,520 |
| Total liabilities | All liabilities | `BAL_liabilities_total_[year]` | 154,943 | 138,661 |
| Shareholders' equity | Walmart equity (excl. NCI) | `BAL_equity_shareholders_[year]` | 74,669 | 72,496 |

### Income Statement Items

| Variable | Description | Named Range | FY2020 |
|----------|-------------|-------------|--------|
| Net sales | Product and service revenue | `INC_sales` | 519,926 |
| Membership and other income | Sam's Club membership + other | `INC_income_other` | 4,038 |
| Cost of sales | Direct costs | `INC_cost_goods_sold` | 394,605 |
| SG&A expenses | Operating overhead | `INC_sga` | 108,791 |
| Depreciation & amortization | Non-cash charge (from CFS) | `INC_depreciation` | 10,987 |
| EBIT / Operating income | `Total revenues − COGS − SGA` | `INC_ebit` | 20,568 |
| Other gains (losses) | Unrealized investment gains (JD.com) | *(included in pretax)* | 1,958 |
| Interest expense, net | Net cost of debt financing | `INC_interest_expense` | 2,410 |
| Income taxes | Tax provision | `INC_taxes` | 4,915 |
| Net income (attributable to Walmart) | After NCI deduction of $320M | `INC_net` | 14,881 |
| Dividends | Cash distributions to shareholders | `INC_dividends` | 6,048 |

### Cash Flow Statement Items

| Variable | Description | Named Range | FY2020 |
|----------|-------------|-------------|--------|
| Cash from operations | Operating cash flow | `CASH_operating` | 25,255 |
| Cash from investments | Investing cash flow | `CASH_investments` | −9,128 |
| Cash from financing | Financing cash flow | `CASH_financing` | −14,299 |

### Market / Analyst Inputs

| Variable | Description | Named Range | Value |
|----------|-------------|-------------|-------|
| Share price | WMT closing price, Jan 31, 2020 | `share_price` | $117.39 |
| Shares outstanding | Total shares (millions) | `shares_outstanding` | 2,832 |
| Cost of capital | Estimated WACC | `cost_capital` | 5.7% |
| Tax rate | Effective rate (4,915 / 20,116) | `tax_rate` | 24.4% |

---

## 3. Assumptions & Constraints

- All figures in USD millions ($M) unless otherwise noted.
- Tax rate uses Walmart's effective rate of 24.4% (income taxes $4,915M ÷ pretax income $20,116M), not the 21% statutory rate, to reflect actual tax burden.
- Cost of capital estimated at 5.7% WACC, reflecting Walmart's investment-grade credit profile and stable cash flows (lower than typical retail peers).
- Depreciation and amortization ($10,987M) is embedded within Cost of Sales and SG&A in Walmart's P&L and does not appear as a separate income statement line. It is sourced from the Cash Flow Statement and stored in `INC_depreciation` solely for use in the Cash Coverage ratio.
- Shareholders' equity uses Walmart-attributable equity ($74,669M), excluding noncontrolling interest ($6,883M), consistent with the template's `BAL_equity_shareholders_[year]` convention.
- Walmart adopted ASC 842 (new lease standard) in FY2020, adding $21.8B in lease right-of-use assets and $15.1B in lease liabilities that were not on the FY2019 balance sheet. This makes direct FY2019–FY2020 balance sheet comparisons imperfect for lease-heavy line items.
- Total assets in FY2019 ($219,295M) include $7,078M in capital lease assets under the old standard; FY2020 ($236,495M) includes $21,841M in ROU assets under ASC 842. The year-over-year increase in assets reflects this accounting change, not purely business growth.
- Interest expense uses net interest ($2,410M = debt interest $2,262M + finance lease $337M − interest income $189M).
- Start-of-year values use the FY2019 Balance Sheet (January 31, 2019).
- No off-balance-sheet items or contingent liabilities are included.

---

## 4. Calculation Flow

### Step 1: Derived Inputs
1. `market_capitalization` = `share_price` × `shares_outstanding` = $117.39 × 2,832 = $332,448M
2. `currentYear_after_tax_operating_income` = `INC_net` + (1 − `tax_rate`) × `INC_interest_expense` = 14,881 + (0.756 × 2,410) = **$16,703M**
3. `currentYear_daily_sales_average` = `INC_sales` / 365 = 519,926 / 365 = **$1,424M/day**
4. `currentYear_cost_goods_sold_daily` = `INC_cost_goods_sold` / 365 = **$1,081M/day**
5. `currentYear_working_capital_net` = `BAL_assets_current_2020` − `BAL_liabilities_current_2020` = 61,806 − 77,790 = **−$15,984M**
6. `startYear_total_capitalization` = `BAL_debt_long_term_2019` + `BAL_equity_shareholders_2019` = 43,520 + 72,496 = **$116,016M**
7. `avg_equity` = AVERAGE(72,496; 74,669) = **$73,583M**
8. `avg_total_assets` = AVERAGE(219,295; 236,495) = **$227,895M**

### Step 2: Performance Ratios
- **MVA** = `market_capitalization` − `currentYear_equity` = 332,448 − 74,669 = **$257,779M**
- **Market-to-Book** = `market_capitalization` / `currentYear_equity` = **4.45x**
- **EVA** = `currentYear_after_tax_operating_income` − (`cost_capital` × `startYear_total_capitalization`) = 16,703 − (0.057 × 116,016) = **$10,090M**

### Step 3: Profitability Ratios
- **ROA** = `currentYear_after_tax_operating_income` / `startYear_total_assets` = **7.6%**
- **ROC** = `currentYear_after_tax_operating_income` / `startYear_total_capitalization` = **14.4%**
- **ROE** = `INC_net` / `startYear_equity` = **20.5%**
- *(Repeat with average denominators for AVG variants)*

### Step 4: Efficiency Ratios
- **Asset Turnover** = `INC_sales` / `startYear_total_assets` = **2.37x**
- **Receivables Turnover** = `INC_sales` / `startYear_receivables` = **82.8x**
- **Avg Collection Period** = `startYear_receivables` / `currentYear_daily_sales_average` = **4.4 days**
- **Inventory Turnover** = `INC_cost_goods_sold` / `startYear_inventory` = **8.9x**
- **Days in Inventory** = `startYear_inventory` / `currentYear_cost_goods_sold_daily` = **40.9 days**
- **Profit Margin** = `INC_net` / `INC_sales` = **2.9%**
- **Operating Profit Margin** = `currentYear_after_tax_operating_income` / `INC_sales` = **3.2%**

### Step 5: Leverage Ratios
- **Long-term Debt Ratio** = `currentYear_debt_long_term` / (`currentYear_debt_long_term` + `currentYear_equity`) = **36.9%**
- **Debt-Equity Ratio** = `currentYear_debt_long_term` / `currentYear_equity` = **0.59x**
- **Total Debt Ratio** = `currentYear_liabilities_total` / `currentYear_assets_total` = **65.5%**
- **Times Interest Earned** = `INC_ebit` / `INC_interest_expense` = **8.5x**
- **Cash Coverage** = (`INC_ebit` + `INC_depreciation`) / `INC_interest_expense` = **13.1x**
- **Debt Burden** = `INC_net` / `currentYear_after_tax_operating_income` = **0.89x**
- **Leverage Ratio** = `currentYear_assets_total` / `currentYear_equity` = **3.17x**

### Step 6: Liquidity Ratios
- **NWC-to-Assets** = `currentYear_working_capital_net` / `currentYear_assets_total` = **−6.8%**
- **Current Ratio** = `currentYear_assets_current` / `currentYear_liabilities_current` = **0.79x**
- **Quick Ratio** = (`currentYear_cash` + `BAL_receivables_2020`) / `currentYear_liabilities_current` = **0.20x**
- **Cash Ratio** = `currentYear_cash` / `currentYear_liabilities_current` = **0.12x**

### Step 7: Du Pont Decomposition
- **Du Pont ROA** = `RATIO_asset_turnover` × `RATIO_operating_profit_margin` = 2.37 × 3.21% = **7.6%** ✓ matches direct ROA
- **Du Pont ROE** = `RATIO_leverage` × `RATIO_asset_turnover` × `RATIO_operating_profit_margin` × `RATIO_debt_burden` = 3.17 × 2.37 × 3.21% × 0.89 = **21.5%** *(approximates direct ROE of 20.5%; minor difference due to start-of-year vs. blended denominators)*

---

## 5. Outputs

| Output | Description | Format | Purpose |
|--------|-------------|--------|---------|
| Balance Sheet | FY2020 and FY2019 side-by-side | Formatted table | Input source and year-over-year reference |
| Income Statement | Revenue through net income with % of sales | Formatted table | Input source and margin reference |
| Cash Flow Statement | Operating / investing / financing flows | Formatted table | Input source; supports cash coverage ratio |
| Ratio inputs section | All raw inputs with named ranges and source | Structured table | Auditability and formula traceability |
| Ratio outputs by category | 25+ ratios across 6 categories | Formatted table | Core analytical deliverable |
| Du Pont decomposition | ROA and ROE breakdown into component drivers | Table | Identifies where return is created or lost |
| Named range documentation | Formula in named-range notation per ratio | Column in ratios tab | Enables AI prompt and model reconstruction |
| Notes sheet | Assumptions, data sources, and caveats | Narrative | Supports Stage 3 and Stage 4 documentation |

---

## 7. Model Review — What Worked & What to Improve

**What worked well:**
- The named range convention (`INC_*`, `BAL_*`, `CASH_*`, `startYear_*`, `currentYear_*`) kept all ratio formulas readable and auditable. Any formula can be understood without opening the cell — e.g., `INC_net / startYear_equity` is immediately interpretable.
- The `INDIRECT()` function in the Ratios tab dynamically constructs named range references by year (e.g., `BAL_equity_shareholders_2020` vs. `_2019`), which elegantly handles the two-year requirement without duplicating formulas.
- Du Pont ROA matched the directly computed ROA exactly (7.62%), confirming internal consistency.
- Color coding (Yellow = inputs, Blue = assumptions, Green = formulas, Gray = outputs) made the model easy to audit at a glance.

**What required judgment calls and workarounds:**
- **Depreciation placement:** Walmart does not report D&A as a separate income statement line — it is embedded in Cost of Sales and SG&A. A workaround was used: a dedicated note row stores D&A ($10,987M sourced from the Cash Flow Statement) so it is accessible to `INC_depreciation` for the Cash Coverage ratio only. This is non-standard and should be clearly documented in any handoff.
- **Income statement structure:** Walmart's P&L includes three unusual items — membership income ($4,038M reported above operating income), other gains/losses ($1,958M from JD.com fair value changes), and noncontrolling interest deduction ($320M). These required careful staging to arrive at the correct net income figure of $14,881M attributable to Walmart. A simplified template structure risks understating net income by $12B if these lines are omitted.
- **ASC 842 lease standard:** The adoption in FY2020 added $14.8B to total assets with no FY2019 restatement. This inflates FY2020 total assets and makes start-of-year vs. current-year comparisons imperfect for total assets and total capitalization. A rigorous model would adjust FY2019 assets for comparability or flag the distortion explicitly.
- **Effective vs. statutory tax rate:** Walmart's effective rate (24.4%) is meaningfully higher than the 21% statutory rate, producing a materially different after-tax operating income. The effective rate was used here; this assumption should be revisited for multi-year analysis.

**What would improve the model:**
- Add a peer comparison tab benchmarking Walmart's ratios against Target (TGT) and Costco (COST) — the most natural competitors.
- Add a second year of data (FY2019) to enable trend analysis on all six ratio categories.
- Replace the D&A workaround with a proper reconciliation note and separate depreciation input cell at the top of the Ratios tab.
- Add a sensitivity table showing how EVA and ROE change under different WACC assumptions (e.g., 5%, 6%, 7%).

---

## 8. Limitations & Next Steps

This model does not incorporate industry peer comparisons, multi-year trend analysis, off-balance-sheet obligations beyond what ASC 842 requires on the balance sheet, or segment-level analysis (Walmart U.S. vs. International vs. Sam's Club). The lease accounting transition creates a structural discontinuity between FY2019 and FY2020 balance sheet data that should be disclosed in any executive presentation.

The next phase (Stage 4) will involve writing a structured AI prompt using this specification as the input blueprint, interpreting the ratio results in the context of Walmart's business model, and producing actionable recommendations for senior management. Key topics for the Stage 4 analysis include: the interpretation of negative NWC as a deliberate competitive advantage, the positive EVA ($10.1B) confirming value creation above cost of capital, and the thin profit margin (2.9%) offset by extremely high asset turnover (2.37x) as the defining Du Pont characteristic of Walmart's EDLP model.
