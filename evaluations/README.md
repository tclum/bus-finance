# Daily Market Hypothesis Evaluations

> Autonomous system scanning the US equity market and financial news twice per trading day, generating CFO-grade analytical hypotheses.  
> See [system spec](../docs/hypothesis-generator-spec.md) for design.

## Latest memo — April 28, 2026 — Pre-market

The tape is bifurcating on AI infrastructure: memory and GPU leaders (MU +5.60%, NVDA +4.00%) continue rallying while AMD sold off -3.79% despite its strong 5-day performance, and semis broadly show elevated volume dispersion. This divergence coincides with Reuters reporting that Big Tech AI spending is set to hit $600 billion, but no guidance raises have been announced to confirm the capex acceleration the market is pricing. Meanwhile, Brent crude topped $111/barrel on Iran war escalation headlines, creating a margin-compression setup for consumer discretionary and industrials that has not yet fully expressed in sector performance. The CFO should prioritize the semiconductor inventory and capex investigation, as our own capital equipment orders share suppliers with hyperscaler demand.

[Read full memo →](2026/04/2026-04-28-1240.md)

## Operational metrics

![Run cost](charts/cost_trend.svg)

![Token usage](charts/token_usage.svg)

## This week

![Weekly rollup](charts/weekly_rollup.svg)

## Recent runs

| Date | Session | Hypotheses | Cost | Link |
|---|---|---:|---:|---|
| 2026-04-28 12:40Z | Pre-market | 4 | $0.0702 | [memo](2026/04/2026-04-28-1240.md) |
| 2026-04-27 20:49Z | Close | 4 | $0.0738 | [memo](2026/04/2026-04-27-2049.md) |
| 2026-04-27 12:37Z | Pre-market | 4 | $0.0777 | [memo](2026/04/2026-04-27-1237.md) |
| 2026-04-24 20:48Z | Close | 4 | $0.0760 | [memo](2026/04/2026-04-24-2048.md) |
| 2026-04-24 20:37Z | Close | 4 | $0.0736 | [memo](2026/04/2026-04-24-2037.md) |
| 2026-04-24 20:10Z | Close | 4 | $0.0696 | [memo](2026/04/2026-04-24-2010.md) |

## How this runs

See the main [README](../README.md#daily-market-hypothesis-generator) for the schedule, manual trigger command, and a short description of each stage.
