# Daily Market Hypothesis Generator — Project Specification

**Created by:** Timothy Lum
**Date Created:** April 22, 2026
**Version:** 1.0
**LLM Used:** Claude (Anthropic) — system runtime + Claude Code for the build

**Role:** Financial Analyst / FP&A Analyst
**Audience:** CFO or Director of FP&A

**Purpose:** Specification for an automated system that scans the U.S. equity market and financial news 2× per trading day and generates analytical hypotheses suitable for presentation to a CFO. Hypotheses are formatted in the same memo style as the Stage 1 Walmart analysis and mapped to the six-category ratio framework from the Stage 2 model.

---

## 1. Problem Statement

The Stage 1–3 work produced a rigorous one-time ratio analysis of a single company (WMT). This system extends that capability into ongoing market intelligence: rather than analyzing one company once, it scans the broad market continuously and surfaces 3–5 testable hypotheses per run that a CFO could direct an analyst team to investigate further.

A **hypothesis** in this context is a falsifiable analytical question grounded in observable market or news evidence. Examples:

- *"Retail sector inventory efficiency may be deteriorating sector-wide following the latest CPI surprise — investigate days-in-inventory for TGT, COST, WMT vs. their 5-year averages and check guidance language for inventory commentary."*
- *"Bank net interest margins likely compressed this quarter — pull NIM disclosures from JPM, BAC, WFC and compare to the prior cycle's response to a similar rate path."*
- *"Energy sector free cash flow is at risk if WTI sustains below $70 — XOM and CVX dividend coverage was 1.4× and 1.2× at last reported; model break-even at $65 and $70."*

Each hypothesis is tagged with one of the six ratio categories from the Stage 2 model, plus a **Macro/Strategic** category for top-down themes that don't fit the company-level lens.

---

## 2. Inputs (Data Sources)

### Market Data — `yfinance` (free, no API key)

| Group | Tickers |
|-------|---------|
| Indices | `^GSPC`, `^DJI`, `^IXIC`, `^RUT`, `^VIX` |
| Sector ETFs | `XLK`, `XLF`, `XLE`, `XLV`, `XLY`, `XLP`, `XLI`, `XLB`, `XLU`, `XLRE`, `XLC` |
| Top movers | Top 20 gainers + top 20 losers by % move within S&P 500 (configurable) |

For each ticker: 1-day % change, 5-day % change, volume vs. 30-day average.

### Macro Data — FRED API (free, requires free key)

- `FEDFUNDS` — Federal funds rate
- `DGS10` — 10-year Treasury yield
- `CPIAUCSL` — Most recent CPI release
- `UNRATE` — Most recent unemployment

### News — RSS aggregation (free)

- Reuters Business
- Yahoo Finance top stories
- MarketWatch top stories
- Filter window: last 12 hours
- Headlines + summaries only (full articles excluded to control token cost)

### Optional upgrades

- **NewsAPI** ($0–$449/mo) for richer multi-source coverage
- **Polygon.io** for intraday flow + options data
- **SEC EDGAR** API for fresh 8-K / 10-Q filings, enabling company-specific hypotheses

---

## 3. Architecture

```
bus-finance/
├── docs/                              # existing Stage 1–3 materials
├── evaluations/
│   └── 2026/04/2026-04-22-1630.md     # one memo per run, dated
├── src/
│   ├── __init__.py
│   ├── market_scan.py                 # pulls market + macro data
│   ├── news_scan.py                   # aggregates RSS feeds
│   ├── generate_hypotheses.py         # Anthropic API call + memo write
│   └── notify.py                      # Discord/email hooks (later stage)
├── prompts/
│   ├── system_prompt.md               # CFO analyst persona + ratio framework
│   └── hypothesis_format.md           # output template
├── config/
│   ├── config.yaml                    # cadence, scope, output toggles
│   └── universe.yaml                  # tickers, indices, sectors to scan
├── .github/workflows/
│   └── daily-evaluation.yml           # cron schedule
├── requirements.txt
├── README.md
└── .env.example                       # ANTHROPIC_API_KEY, FRED_API_KEY
```

---

## 4. Prompt Design

**System prompt** establishes Claude's role as a senior FP&A analyst preparing a briefing for a CFO. It explicitly references the six-category ratio framework from the Stage 2 model (Performance, Profitability, Efficiency, Leverage, Liquidity, DuPont) and instructs Claude to map each hypothesis to one of these categories — or to **Macro/Strategic** when the theme is top-down.

**User prompt** is assembled at runtime from: timestamp, market snapshot (formatted table), top movers, macro context, and the news digest. It closes with: *"Generate 3–5 hypotheses worth presenting to the CFO. Be skeptical, specific, and actionable."*

**Output format** requested by the prompt — mirrors the Stage 1 memo style:

```markdown
# Daily Market Hypotheses — [Date, Session]

**TO:** Chief Financial Officer
**FROM:** Hypothesis Generation System
**DATE:** [timestamp]
**RE:** [N] hypotheses for investigation

## Executive Summary
[2–3 sentence overview of the day's themes]

## Hypothesis 1: [One-sentence thesis]
**Category:** [Performance / Profitability / Efficiency / Leverage / Liquidity / DuPont / Macro]
**Confidence:** [Low / Medium / High]

### Observation
[Market and news evidence supporting the hypothesis]

### Why it matters
[Strategic implication for a CFO audience]

### Recommended investigation
[Concrete next steps — specific ratios to compute, comparisons to draw, filings to read]

---
```

---

## 5. Scheduling

GitHub Actions cron with two scheduled jobs:

| Run | Cron (UTC) | ET equivalent | Purpose |
|-----|------------|---------------|---------|
| Pre-market | `0 12 * * 1-5` | 8:00 AM ET (DST) | Set the day's context: overnight news, futures, what to watch |
| Close | `30 20 * * 1-5` | 4:30 PM ET (DST) | Day wrap: how the session played out, hypotheses for tomorrow |

Each run flow: pull data → assemble prompt → call Claude API → commit new memo to `evaluations/YYYY/MM/`.

---

## 6. Cost & Resource Estimate

| Item | Estimate |
|------|----------|
| Anthropic API (Sonnet 4.5) | ~10K input + 3K output tokens × 2 runs/day ≈ **$0.10/day ≈ $3/mo** |
| GitHub Actions minutes | ~2 min/run × 2 runs × 22 trading days ≈ **~90 min/mo** (free tier: 2,000) |
| Data sources | All free tier |
| **Total** | **~$3/mo** |

---

## 7. Build Stages

**Stage 1 — Local prototype.** Get `market_scan.py` and `news_scan.py` running locally. Print structured output and verify data quality. *(~1–2 hrs with Claude Code)*

**Stage 2 — Prompt engineering.** Iterate on `system_prompt.md` and `hypothesis_format.md` until memos read at CFO-briefing quality. Test across at least 3–4 different market days (calm, volatile, Fed day, earnings-heavy day). *(~2–4 hrs)*

**Stage 3 — Automation.** Wire up the GitHub Actions workflow. Store `ANTHROPIC_API_KEY` and `FRED_API_KEY` as repo secrets. Verify a few real runs commit cleanly to `evaluations/`.

**Stage 4 — Notifications (optional).** Add Discord webhook in `notify.py` so each run posts a summary + permalink to the markdown file.

**Stage 5 — Validation loop (future).** Auto-backtest hypotheses against subsequent market data; promote a "hit rate" metric over time so the system can be tuned.

---

## 8. Limitations & Next Steps

- Free RSS feeds may miss niche sector news; NewsAPI or Polygon are clean upgrade paths.
- `yfinance` is unofficial and rate-limited — Polygon is the production-grade fallback.
- Hypotheses are *generated*, not *validated* — Stage 5 above addresses this.
- Could be extended to pull fresh 10-Q / 8-K filings via SEC EDGAR for deeper company-specific hypotheses keyed off filing dates.
- Confidence labels are model self-assessments; over time these should be calibrated against backtested hit rates.

---

## 9. Acceptance Criteria

The first usable version is done when:

1. Running `python -m src.generate_hypotheses` locally produces a valid markdown memo with 3+ hypotheses, each tagged with a category and confidence level.
2. The memo references at least one specific ticker, one specific macro data point, and one specific news headline.
3. The GitHub Actions workflow runs on schedule and commits a new file to `evaluations/YYYY/MM/` without manual intervention.
4. Total monthly cost stays under $5.
