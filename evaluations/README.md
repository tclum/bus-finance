# Daily Market Hypothesis Evaluations

> Autonomous system scanning the US equity market and financial news twice per trading day, generating CFO-grade analytical hypotheses.  
> See [system spec](../docs/hypothesis-generator-spec.md) for design.

## Latest memo — May 14, 2026 — Pre-market

The tape is pricing a two-speed economy: AI infrastructure demand is accelerating (CSCO +13.18% on record AI orders, NVDA +2.29%, MU +4.83% on 1.18× volume), while enterprise software and financial services are compressing (ACN -5.97% on 2.52× volume, XLF -1.14%, WFC -2.19%). The most important cross-reference is between Cisco's AI networking guidance and the US clearing H200 chip exports to 10 Chinese firms — if China demand is reopening, the capex cycle has a second leg that consensus has not priced. The CFO should prioritize understanding whether our own IT capex plans are exposed to the same supply constraints now driving Cisco's order backlog.

[Read full memo →](2026/05/2026-05-14-1241.md)

## Operational metrics

![Run cost](charts/cost_trend.svg)

![Token usage](charts/token_usage.svg)

## This week

![Weekly rollup](charts/weekly_rollup.svg)

## Recent runs

| Date | Session | Hypotheses | Cost | Link |
|---|---|---:|---:|---|
| 2026-05-14 12:41Z | Pre-market | 4 | $0.0681 | [memo](2026/05/2026-05-14-1241.md) |
| 2026-05-13 21:04Z | Close | 4 | $0.0712 | [memo](2026/05/2026-05-13-2104.md) |
| 2026-05-13 12:48Z | Pre-market | 4 | $0.0697 | [memo](2026/05/2026-05-13-1248.md) |
| 2026-05-12 21:02Z | Close | 4 | $0.0715 | [memo](2026/05/2026-05-12-2102.md) |
| 2026-05-12 12:45Z | Pre-market | 4 | $0.0744 | [memo](2026/05/2026-05-12-1245.md) |
| 2026-05-11 21:02Z | Close | 4 | $0.0649 | [memo](2026/05/2026-05-11-2102.md) |
| 2026-05-11 13:04Z | Pre-market | 4 | $0.0766 | [memo](2026/05/2026-05-11-1304.md) |
| 2026-05-08 20:49Z | Close | 4 | $0.0728 | [memo](2026/05/2026-05-08-2049.md) |
| 2026-05-08 12:33Z | Pre-market | 4 | $0.0707 | [memo](2026/05/2026-05-08-1233.md) |
| 2026-05-07 20:53Z | Close | 4 | $0.0702 | [memo](2026/05/2026-05-07-2053.md) |

## How this runs

See the main [README](../README.md#daily-market-hypothesis-generator) for the schedule, manual trigger command, and a short description of each stage.
