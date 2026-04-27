# Daily Market Hypothesis Evaluations

> Autonomous system scanning the US equity market and financial news twice per trading day, generating CFO-grade analytical hypotheses.  
> See [system spec](../docs/hypothesis-generator-spec.md) for design.

## Latest memo — April 27, 2026 — Close

The tape is bifurcating on oil-driven margin pressure: memory semiconductors rallied sharply (MU +5.60%, NVDA +4.00%) while consumer-facing names with high energy exposure sold off (MCD -3.06%, WMT -1.79%). Brent crude surpassed $108/barrel on Iran storage capacity concerns per Reuters and MarketWatch, creating a clear profitability stress test for companies that cannot pass through input costs. The most actionable cross-reference is the simultaneous strength in financials (XLF +0.76%, led by SCHW +2.55% and money-center banks) against weakness in telecom infrastructure (TMUS -3.71%, CCI -3.36%, T -2.60%), suggesting a sector rotation driven by rate expectations embedded in the oil shock rather than broad risk-off behavior.

[Read full memo →](2026/04/2026-04-27-2049.md)

## Operational metrics

![Run cost](charts/cost_trend.svg)

![Token usage](charts/token_usage.svg)

## This week

![Weekly rollup](charts/weekly_rollup.svg)

## Recent runs

| Date | Session | Hypotheses | Cost | Link |
|---|---|---:|---:|---|
| 2026-04-27 20:49Z | Close | 4 | $0.0738 | [memo](2026/04/2026-04-27-2049.md) |
| 2026-04-27 12:37Z | Pre-market | 4 | $0.0777 | [memo](2026/04/2026-04-27-1237.md) |
| 2026-04-24 20:48Z | Close | 4 | $0.0760 | [memo](2026/04/2026-04-24-2048.md) |
| 2026-04-24 20:37Z | Close | 4 | $0.0736 | [memo](2026/04/2026-04-24-2037.md) |
| 2026-04-24 20:10Z | Close | 4 | $0.0696 | [memo](2026/04/2026-04-24-2010.md) |

## How this runs

See the main [README](../README.md#daily-market-hypothesis-generator) for the schedule, manual trigger command, and a short description of each stage.
