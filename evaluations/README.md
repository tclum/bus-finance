# Daily Market Hypothesis Evaluations

> Autonomous system scanning the US equity market and financial news twice per trading day, generating CFO-grade analytical hypotheses.  
> See [system spec](../docs/hypothesis-generator-spec.md) for design.

## Latest memo — May 8, 2026 — Pre-market

The tape is showing a sharp divergence between semiconductor winners and losers that cannot be explained by sector rotation alone. QCOM, NOW, and enterprise software rallied 3–5% while AMAT, AMD, AVGO, INTC, and MU sold off 3–4% despite all five having posted strong 5-day gains of +4% to +25%. This is not a broad tech selloff — XLK is only down 20 bps and NVDA is up 1.77%. The most likely explanation is a rotation within semis from manufacturing/memory exposure toward AI-inference and enterprise-software beneficiaries, possibly triggered by Sony's disclosure of memory-price-surge headwinds and concerns about capex sustainability. Separately, energy's 6.2% five-day decline with elevated volume suggests the market is pricing in demand destruction from higher gas prices, which Bank of America's consumer-spending data corroborates. The CFO should prioritize the semiconductor hypothesis — if capex is peaking, our own IT budget assumptions for FY27 may need revision.

[Read full memo →](2026/05/2026-05-08-1233.md)

## Operational metrics

![Run cost](charts/cost_trend.svg)

![Token usage](charts/token_usage.svg)

## This week

![Weekly rollup](charts/weekly_rollup.svg)

## Recent runs

| Date | Session | Hypotheses | Cost | Link |
|---|---|---:|---:|---|
| 2026-05-08 12:33Z | Pre-market | 4 | $0.0707 | [memo](2026/05/2026-05-08-1233.md) |
| 2026-05-07 20:53Z | Close | 4 | $0.0702 | [memo](2026/05/2026-05-07-2053.md) |
| 2026-05-07 12:42Z | Pre-market | 4 | $0.0706 | [memo](2026/05/2026-05-07-1242.md) |
| 2026-05-06 20:56Z | Close | 4 | $0.0743 | [memo](2026/05/2026-05-06-2056.md) |
| 2026-05-06 12:42Z | Pre-market | 4 | $0.0667 | [memo](2026/05/2026-05-06-1242.md) |
| 2026-05-05 20:50Z | Close | 4 | $0.0704 | [memo](2026/05/2026-05-05-2050.md) |
| 2026-05-05 12:30Z | Pre-market | 4 | $0.0712 | [memo](2026/05/2026-05-05-1230.md) |
| 2026-05-04 20:53Z | Close | 4 | $0.0748 | [memo](2026/05/2026-05-04-2053.md) |
| 2026-05-04 12:38Z | Pre-market | 4 | $0.0716 | [memo](2026/05/2026-05-04-1238.md) |
| 2026-05-01 20:48Z | Close | 4 | $0.0687 | [memo](2026/05/2026-05-01-2048.md) |

## How this runs

See the main [README](../README.md#daily-market-hypothesis-generator) for the schedule, manual trigger command, and a short description of each stage.
