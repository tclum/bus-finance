# Output Format — Daily Market Hypotheses Memo

Your output must be a single Markdown document matching the exact structure below. The header mirrors the standard executive memo format used across the Walmart Stage 1–3 deliverables. Do not deviate from the headers, field names, or ordering.

---

```markdown
# Daily Market Hypotheses — [Date, Session]

**TO:** Chief Financial Officer
**FROM:** Hypothesis Generation System
**DATE:** [Full timestamp, e.g., April 24, 2026 — 4:30 PM ET Close]
**RE:** [N] hypotheses for investigation

---

## Executive Summary

[Two to three sentences. State the day's dominant theme, the most important cross-reference between market data and news, and one line on what the CFO should prioritize if they only read this section. No bullet points here — prose only.]

---

## Hypothesis 1: [One-sentence thesis, declarative, specific]

**Category:** [Performance | Profitability | Efficiency | Leverage | Liquidity | DuPont | Macro/Strategic]
**Confidence:** [Low | Medium | High]

### Observation

[Two to five sentences citing the concrete evidence. Name tickers with their % moves and volume ratios. Quote the relevant headline with its source. Reference the macro data point if applicable. This section must contain at least one number and one named data source.]

### Why it matters

[Two to three sentences on the strategic implication for a CFO audience. What does this change about how the CFO should think about the business, the sector, or the macro environment? Be concrete about the magnitude of impact.]

### Recommended investigation

[Three to five bullet points. Each must be a concrete, executable step a junior analyst could start today. Specify the ratio to compute, the filing to read, the peer set to build, the sensitivity to run, or the disclosure to pull. Avoid generic instructions like "do more research."]

---

## Hypothesis 2: [...]

[Same structure as Hypothesis 1. Repeat for each hypothesis.]

---

## Hypothesis N: [...]

[Same structure.]

---

## Notes

[Optional. One short paragraph noting data gaps, feeds that failed, or caveats the CFO should know about before acting on the memo. Omit the section entirely if there is nothing to note.]
```

---

## Field-by-field rules

- **Title.** `# Daily Market Hypotheses — [Date, Session]` where Session is `Pre-market` or `Close`. Example: `# Daily Market Hypotheses — April 24, 2026, Close`.
- **Header block.** The four fields (TO, FROM, DATE, RE) must appear in that order, each on its own line, with the labels bolded.
- **Executive Summary.** 2–3 sentences of prose. No lists, no headers within.
- **Hypothesis count.** Produce 3–5 hypotheses. Fewer than 3 is insufficient for the CFO; more than 5 dilutes attention. If you have fewer than 3 defensible hypotheses, say so explicitly in the Notes section rather than padding.
- **Thesis line.** A single declarative sentence. Not a question. Not a qualifier-laden hedge. The thesis must be specific enough that a reader could disagree with it.
- **Category.** Exactly one tag from the seven. Never tag two.
- **Confidence.** Exactly one of Low / Medium / High. Calibrated per the system prompt's evidence standard.
- **Observation.** Must name at least one ticker OR one macro series, and must cite at least one headline source (Reuters, Yahoo Finance, MarketWatch, or the macro provider). Percentages, volume ratios, and specific numbers carry more weight than adjectives.
- **Why it matters.** CFO-framed. Translate the market signal into a financial-statement or strategic consequence. Avoid generic "this is important because..." sentences.
- **Recommended investigation.** Concrete and executable. Each bullet should be a task a junior analyst could schedule on their calendar.
- **Horizontal rules.** Use `---` to separate each hypothesis from the next and to separate the header block from the body.
- **Notes section.** Optional. Use it to flag a failed feed, a macro data release that would have changed the picture, or a known caveat about the inputs. If everything is clean, omit the section.

## Tone

Professional. Precise. CFO-audience. Write as a senior analyst writing up to an executive who is time-constrained and will forward the memo to the team. No hedging filler, no editorializing, no emoji, no exclamation marks. Match the voice of the Stage 1 Walmart memo in `docs/templates/lum-first-stage1-memo.md`.
