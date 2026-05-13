# Daily Market Hypothesis Evaluations

> Autonomous system scanning the US equity market and financial news twice per trading day, generating CFO-grade analytical hypotheses.  
> See [system spec](../docs/hypothesis-generator-spec.md) for design.

## Latest memo — May 13, 2026 — Pre-market

The tape is pricing in a sharp inflation re-acceleration following this morning's PPI surprise (+1.4% MoM, largest jump in four years per MarketWatch), triggering a defensive rotation into healthcare and staples while punishing rate-sensitive tech. The semiconductor sector's violent reversal — QCOM -11.46%, INTC -6.82% after multi-day rallies — suggests profit-taking ahead of the Trump-Xi summit rather than fundamental deterioration, but the timing creates refinancing risk for leveraged chip names if the 10-year yield spikes further. The most actionable signal is the healthcare breakout: CVS +3.18% on 1.57× volume and UNH +3.11% leading XLV to +1.96%, the second-best sector performance, which may reflect institutional repositioning for margin defense in a stagflation scenario.

[Read full memo →](2026/05/2026-05-13-1248.md)

## Operational metrics

![Run cost](charts/cost_trend.svg)

![Token usage](charts/token_usage.svg)

## This week

![Weekly rollup](charts/weekly_rollup.svg)

## Recent runs

| Date | Session | Hypotheses | Cost | Link |
|---|---|---:|---:|---|
| 2026-05-13 12:48Z | Pre-market | 4 | $0.0697 | [memo](2026/05/2026-05-13-1248.md) |
| 2026-05-12 21:02Z | Close | 4 | $0.0715 | [memo](2026/05/2026-05-12-2102.md) |
| 2026-05-12 12:45Z | Pre-market | 4 | $0.0744 | [memo](2026/05/2026-05-12-1245.md) |
| 2026-05-11 21:02Z | Close | 4 | $0.0649 | [memo](2026/05/2026-05-11-2102.md) |
| 2026-05-11 13:04Z | Pre-market | 4 | $0.0766 | [memo](2026/05/2026-05-11-1304.md) |
| 2026-05-08 20:49Z | Close | 4 | $0.0728 | [memo](2026/05/2026-05-08-2049.md) |
| 2026-05-08 12:33Z | Pre-market | 4 | $0.0707 | [memo](2026/05/2026-05-08-1233.md) |
| 2026-05-07 20:53Z | Close | 4 | $0.0702 | [memo](2026/05/2026-05-07-2053.md) |
| 2026-05-07 12:42Z | Pre-market | 4 | $0.0706 | [memo](2026/05/2026-05-07-1242.md) |
| 2026-05-06 20:56Z | Close | 4 | $0.0743 | [memo](2026/05/2026-05-06-2056.md) |

## How this runs

See the main [README](../README.md#daily-market-hypothesis-generator) for the schedule, manual trigger command, and a short description of each stage.
