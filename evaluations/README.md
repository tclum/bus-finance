# Daily Market Hypothesis Evaluations

> Autonomous system scanning the US equity market and financial news twice per trading day, generating CFO-grade analytical hypotheses.  
> See [system spec](../docs/hypothesis-generator-spec.md) for design.

## Latest memo — April 30, 2026 — Close

The tape is bifurcating sharply on AI capital allocation: QCOM rallied 15.12% on 3.57× volume while META fell 8.55% on 2.95× volume, both on heavy institutional participation. The divergence centers on whether AI infrastructure spending is shifting from hyperscaler capex (cloud training) toward edge inference (smartphones, IoT). Oil's move to $125/bbl — a four-year high — is compressing consumer discretionary margins while lifting energy and industrials, but the sector rotation is incomplete: XLE led at +4.69% over five days, yet energy names are underrepresented in today's top gainers relative to their sector weight. The CFO should prioritize the QCOM/META split and the oil pass-through question; both have direct implications for our capital allocation and cost structure over the next two quarters.

[Read full memo →](2026/04/2026-04-30-2049.md)

## Operational metrics

![Run cost](charts/cost_trend.svg)

![Token usage](charts/token_usage.svg)

## This week

![Weekly rollup](charts/weekly_rollup.svg)

## Recent runs

| Date | Session | Hypotheses | Cost | Link |
|---|---|---:|---:|---|
| 2026-04-30 20:49Z | Close | 4 | $0.0740 | [memo](2026/04/2026-04-30-2049.md) |
| 2026-04-30 12:36Z | Pre-market | 4 | $0.0693 | [memo](2026/04/2026-04-30-1236.md) |
| 2026-04-29 20:50Z | Close | 4 | $0.0718 | [memo](2026/04/2026-04-29-2050.md) |
| 2026-04-29 12:37Z | Pre-market | 4 | $0.0664 | [memo](2026/04/2026-04-29-1237.md) |
| 2026-04-28 20:53Z | Close | 4 | $0.0665 | [memo](2026/04/2026-04-28-2053.md) |
| 2026-04-28 12:40Z | Pre-market | 4 | $0.0702 | [memo](2026/04/2026-04-28-1240.md) |
| 2026-04-27 20:49Z | Close | 4 | $0.0738 | [memo](2026/04/2026-04-27-2049.md) |
| 2026-04-27 12:37Z | Pre-market | 4 | $0.0777 | [memo](2026/04/2026-04-27-1237.md) |
| 2026-04-24 20:48Z | Close | 4 | $0.0760 | [memo](2026/04/2026-04-24-2048.md) |
| 2026-04-24 20:37Z | Close | 4 | $0.0736 | [memo](2026/04/2026-04-24-2037.md) |

## How this runs

See the main [README](../README.md#daily-market-hypothesis-generator) for the schedule, manual trigger command, and a short description of each stage.
