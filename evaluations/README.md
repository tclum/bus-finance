# Daily Market Hypothesis Evaluations

> Autonomous system scanning the US equity market and financial news twice per trading day, generating CFO-grade analytical hypotheses.  
> See [system spec](../docs/hypothesis-generator-spec.md) for design.

## Latest memo — May 4, 2026 — Pre-market

The tape is pricing two divergent narratives: a tech-led AI infrastructure rally (XLK +1.49%, ORCL +6.47%, INTC +5.44%) and rising geopolitical risk premium in energy (oil headlines on Iran-US tensions, XLE -1.34% despite crude strength). The cross-reference between Oracle's surge on below-average volume and Intel's continued 5-day rally (+20.69%) suggests sector rotation within tech rather than broad risk-on sentiment — VIX rose +4.59% even as NASDAQ gained +0.89%. The CFO should prioritize understanding whether the semiconductor capex cycle has genuinely re-accelerated or whether this is positioning ahead of earnings, because our own IT infrastructure budget and supplier lead times depend on the same capacity constraints now driving INTC and MU.

[Read full memo →](2026/05/2026-05-04-1238.md)

## Operational metrics

![Run cost](charts/cost_trend.svg)

![Token usage](charts/token_usage.svg)

## This week

![Weekly rollup](charts/weekly_rollup.svg)

## Recent runs

| Date | Session | Hypotheses | Cost | Link |
|---|---|---:|---:|---|
| 2026-05-04 12:38Z | Pre-market | 4 | $0.0716 | [memo](2026/05/2026-05-04-1238.md) |
| 2026-05-01 20:48Z | Close | 4 | $0.0687 | [memo](2026/05/2026-05-01-2048.md) |
| 2026-05-01 12:24Z | Pre-market | 4 | $0.0638 | [memo](2026/05/2026-05-01-1224.md) |
| 2026-04-30 20:49Z | Close | 4 | $0.0740 | [memo](2026/04/2026-04-30-2049.md) |
| 2026-04-30 12:36Z | Pre-market | 4 | $0.0693 | [memo](2026/04/2026-04-30-1236.md) |
| 2026-04-29 20:50Z | Close | 4 | $0.0718 | [memo](2026/04/2026-04-29-2050.md) |
| 2026-04-29 12:37Z | Pre-market | 4 | $0.0664 | [memo](2026/04/2026-04-29-1237.md) |
| 2026-04-28 20:53Z | Close | 4 | $0.0665 | [memo](2026/04/2026-04-28-2053.md) |
| 2026-04-28 12:40Z | Pre-market | 4 | $0.0702 | [memo](2026/04/2026-04-28-1240.md) |
| 2026-04-27 20:49Z | Close | 4 | $0.0738 | [memo](2026/04/2026-04-27-2049.md) |

## How this runs

See the main [README](../README.md#daily-market-hypothesis-generator) for the schedule, manual trigger command, and a short description of each stage.
