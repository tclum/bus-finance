# Worked Examples — Strong vs. Weak Hypothesis

This file contains two worked examples drawn from the same hypothetical input day: one that meets the standard set in `system_prompt.md`, and one that commits multiple anti-patterns. Both use the same memo format defined in `hypothesis_format.md`. Read both before producing your own memo. When in doubt, compare your draft hypothesis to each and ask which it more closely resembles.

The date and input values below are illustrative; treat them as the inputs that would be assembled by `market_scan.py` and `news_scan.py` for a given session.

---

## Example A — Strong Hypothesis

> **One-line note on why this is strong:** Cross-references market data (three named tickers with volume ratios), news (two independent headlines from two outlets), and macro (DGS10) to triangulate a specific, falsifiable, CFO-actionable claim with honestly calibrated Medium confidence.

### Input snapshot (illustrative)

- Market: INTC +21.0% on 2.16× avg volume; AMD +13.5% on 1.87× avg volume; QCOM +10.4% on 1.69× avg volume; XLK +2.71% leading all sectors vs. S&P 500 +0.69%.
- News: Reuters, "US chipmakers hit record highs as Intel turbocharges AI rally." MarketWatch, "Why the party for Intel and other chip stocks could last a long time."
- Macro: DGS10 steady at ~4.20% (unchanged 1w); FEDFUNDS unchanged.

### Hypothesis output

## Hypothesis 1: The semiconductor tape is pricing in a re-acceleration of AI infrastructure capex that has not yet been confirmed in semicap guidance.

**Category:** Performance
**Confidence:** Medium

### Observation

INTC, AMD, and QCOM rallied 21.0%, 13.5%, and 10.4% respectively, each on 1.6×–2.2× average daily volume — the volume confirms the move is not thin-tape noise. XLK led all sector ETFs at +2.71%, roughly 4× the S&P 500's +0.69%. Reuters ("US chipmakers hit record highs as Intel turbocharges AI rally") and MarketWatch ("Why the party for Intel and other chip stocks could last a long time") both independently cite CPU AI-inference demand as the catalyst. The 10-year yield held at ~4.20% and FEDFUNDS was unchanged, so this is not a duration-driven rotation into long-duration tech — it is a fundamental-demand repricing.

### Why it matters

If the capex re-acceleration is real, the second-order beneficiaries — semicap equipment (AMAT, LRCX, KLAC) and AI-infrastructure software (NOW, which also moved +5.27% today) — should see order-book acceleration in the next 1–2 quarters. If instead the rally is sentiment-driven ahead of guidance, we should see it fade into earnings. The CFO needs to know whether competitor capex plans are inflecting, because that shapes our own capital-allocation pacing and any planned equipment orders that share suppliers with hyperscaler demand.

### Recommended investigation

- Pull INTC and AMD most recent quarterly capex guidance (10-Q or earnings release) and compare vs. trailing two quarters and consensus.
- Compute trailing-four-quarter inventory turnover and days-in-inventory for AMAT, LRCX, and KLAC, and compare to the 2021 and 2023 cycle peaks to gauge where we are in the capex cycle.
- Check sell-side price target revisions on the top five semis over the last five trading days; revisions are lagging but confirm whether the rally has institutional conviction behind it.
- Pull hyperscaler (MSFT, GOOGL, META, AMZN) most recent capex disclosures and compute the YoY change; this is the demand side of the same question.

---

## Example B — Weak Hypothesis

> **One-line note on why this is weak:** Vague directional claim, unfalsifiable prediction, single-source evidence, and over-tagged as Macro — commits four anti-patterns in one hypothesis. The confidence label is also inflated relative to the evidence.

### Input snapshot (same day, same inputs as Example A)

### Hypothesis output (DO NOT EMULATE)

## Hypothesis 2: Market sentiment is cautious ahead of the Fed meeting and volatility may increase.

**Category:** Macro/Strategic
**Confidence:** High

### Observation

The Fed meets next week and investors appear nervous. A Reuters headline noted "Wall St Week Ahead: Soaring US stocks face pivotal week of tech-led earnings, Fed meeting." Rates are uncertain. Volatility may pick up into the event.

### Why it matters

If volatility increases, it could affect markets. The CFO should be aware that macro conditions remain fluid and sentiment could shift.

### Recommended investigation

- Monitor the situation.
- Watch the Fed meeting.
- Review our exposure.

---

### Why Example B fails, itemized

1. **Vague directional claim.** "Sentiment is cautious" and "investors appear nervous" are narration, not analysis. Nothing in the observation supports the word "cautious" — in fact, Example A's inputs show the tape leading strongly higher, which contradicts "cautious."
2. **Unfalsifiable prediction.** "Volatility may increase" cannot be proven wrong. Any outcome — volatility up, down, or flat — is consistent with the word "may."
3. **Single-source evidence.** The only concrete input is one Reuters headline. There is no cross-reference to market data, no ticker named, no macro data point cited. Had the author looked at the actual tape, they would have seen the chip rally — which is far more interesting and specific than "sentiment."
4. **Over-tagged as Macro.** Every hypothesis this author could not pin down will end up in the Macro bucket. The memo loses signal when Macro becomes the default catch-all.
5. **Inflated confidence.** Labeled High with essentially one weak piece of evidence. The confidence label is a calibration tool for the CFO; inflating it poisons the triage signal.
6. **Non-actionable investigation steps.** "Monitor the situation," "review our exposure" — these are not tasks. A junior analyst reading this has no idea what to do on Monday morning.
