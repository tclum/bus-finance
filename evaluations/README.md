# Daily Market Hypothesis Evaluations

> Autonomous system scanning the US equity market and financial news twice per trading day, generating CFO-grade analytical hypotheses.  
> See [system spec](../docs/hypothesis-generator-spec.md) for design.

## Latest memo — May 6, 2026 — Pre-market

The semiconductor sector is repricing sharply on CPU-driven AI infrastructure demand, with INTC, MU, and QCOM up 11–13% on elevated volume while traditional AI leaders (NVDA, META) lag or decline. This divergence, combined with SpaceX's $55B chip fab filing and multiple capex announcements, suggests the market is pricing a second wave of AI infrastructure buildout that shifts from GPU-centric training to CPU-heavy inference and edge deployment. Separately, geopolitical risk premium is compressing across energy and defensives on reports of a U.S.-Iran peace deal, creating a potential liquidity rotation into cyclicals. The CFO should prioritize understanding whether competitor capex plans are inflecting and whether our own supply chain shares bottlenecks with this new wave of semiconductor demand.

[Read full memo →](2026/05/2026-05-06-1242.md)

## Operational metrics

![Run cost](charts/cost_trend.svg)

![Token usage](charts/token_usage.svg)

## This week

![Weekly rollup](charts/weekly_rollup.svg)

## Recent runs

| Date | Session | Hypotheses | Cost | Link |
|---|---|---:|---:|---|
| 2026-05-06 12:42Z | Pre-market | 4 | $0.0667 | [memo](2026/05/2026-05-06-1242.md) |
| 2026-05-05 20:50Z | Close | 4 | $0.0704 | [memo](2026/05/2026-05-05-2050.md) |
| 2026-05-05 12:30Z | Pre-market | 4 | $0.0712 | [memo](2026/05/2026-05-05-1230.md) |
| 2026-05-04 20:53Z | Close | 4 | $0.0748 | [memo](2026/05/2026-05-04-2053.md) |
| 2026-05-04 12:38Z | Pre-market | 4 | $0.0716 | [memo](2026/05/2026-05-04-1238.md) |
| 2026-05-01 20:48Z | Close | 4 | $0.0687 | [memo](2026/05/2026-05-01-2048.md) |
| 2026-05-01 12:24Z | Pre-market | 4 | $0.0638 | [memo](2026/05/2026-05-01-1224.md) |
| 2026-04-30 20:49Z | Close | 4 | $0.0740 | [memo](2026/04/2026-04-30-2049.md) |
| 2026-04-30 12:36Z | Pre-market | 4 | $0.0693 | [memo](2026/04/2026-04-30-1236.md) |
| 2026-04-29 20:50Z | Close | 4 | $0.0718 | [memo](2026/04/2026-04-29-2050.md) |

## How this runs

See the main [README](../README.md#daily-market-hypothesis-generator) for the schedule, manual trigger command, and a short description of each stage.
